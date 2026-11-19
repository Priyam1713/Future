"""Bounded transit adapter. Native calculations and interpretation rules are unchanged."""
import asyncio
import copy
from datetime import datetime, timedelta, timezone
import multiprocessing as mp
import time
import threading
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from fastapi import HTTPException

ROOT=Path(__file__).resolve().parents[1]
DEADLINE_SECONDS=60


class TransitOrigin(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    natal: dict
    proof: str=Field(max_length=160)


class TransitInput(BaseModel):
    model_config=ConfigDict(extra='forbid',strict=True)
    origin: TransitOrigin
    start: str=Field(min_length=20,max_length=40)
    days: int=Field(ge=1,le=30)

    @field_validator('start')
    @classmethod
    def dated_window(cls,value):
        try:
            t=datetime.fromisoformat(value)
            if t.tzinfo is None or t.utcoffset() is None: raise ValueError()
            if not 1850<=t.astimezone(timezone.utc).year<=2149: raise ValueError()
        except (ValueError,OverflowError):
            raise ValueError('Choose an offset-aware start within the native 1850–2149 ephemeris range, with room for the window.')
        return value

    @model_validator(mode='after')
    def end_bound(self):
        if (datetime.fromisoformat(self.start).astimezone(timezone.utc)+timedelta(days=self.days)).year>2149:
            raise ValueError('The full selected window must stay inside the native 1850–2149 range.')
        return self


def natal_basis(result):
    # Reuse calculated geometry; no birth, names, time conversion, traces or AI.
    return copy.deepcopy({k:result[k] for k in ('technique_id','settings','angles','house_cusps','planets','reproducibility')})


def calculate_transits(natal,start,days,engine=None):
    from future.natal import SkyfieldEphemeris,signed
    from future.transits import forecast,phase
    from future.forecast_report import present
    from future.western import load_context,interpreter,traditional_configuration_context
    from future.knowledge import Registry
    owned=engine is None
    engine=engine or SkyfieldEphemeris(ROOT/'data/de440s.bsp')
    registry=Registry()
    try:
        n=copy.deepcopy(natal)
        n['traditional_configuration_context']=traditional_configuration_context(n)
        records=load_context(registry,n['settings']['tradition'])
        begin=datetime.fromisoformat(start).astimezone(timezone.utc)
        report=present(forecast(engine,n,begin,days,interpreter=interpreter(records,n)))
        targets={**{name:p['longitude'] for name,p in n['planets'].items()},**n['angles']}
        frames=[]
        for day in range(days):
            t=begin+timedelta(days=day)
            _,positions=engine.positions(t)
            contacts=[]
            for c in report['configurations']:
                p=positions[c['transiting']]
                error=signed(p['longitude']-targets[c['natal_target']]-c['branch_degrees'])
                if abs(error)<=c['orb_limit']:
                    contacts.append(dict(configuration_id=c['configuration_id'],phase=phase(error,p['speed_degrees_per_day']),orb=abs(error),retrograde=p['retrograde']))
            frames.append(dict(utc=t.isoformat(),planets=positions,contacts=contacts))
        return dict(report=report,sky_samples=frames,sampling='One native ephemeris sample per day at the window’s UTC clock time; exact contacts use native root times, without interpolation.')
    finally:
        registry.close()
        if owned:engine.kernel.close()


def _worker(connection,natal,start,days):
    try:connection.send(('ok',calculate_transits(natal,start,days)))
    except Exception as exc:connection.send(('error',str(exc)))
    finally:connection.close()


class TransitRunner:
    """One killable computation, no queue/job store and no birth-input storage."""
    def __init__(self,deadline=DEADLINE_SECONDS):
        self.slot=threading.BoundedSemaphore(1)
        self.deadline=deadline

    async def run(self,natal,start,days,disconnected):
        if not self.slot.acquire(blocking=False):
            raise HTTPException(429,'The time instrument is calculating another window. Please try again shortly.')
        parent,child=mp.get_context('spawn').Pipe(duplex=False)
        process=mp.get_context('spawn').Process(target=_worker,args=(child,natal,start,days),daemon=True)
        started=time.monotonic()
        try:
            process.start();child.close()
            while not parent.poll():
                if not process.is_alive():raise ValueError('The transit calculation ended unexpectedly. Your natal chart remains available.')
                if time.monotonic()-started>self.deadline:
                    raise HTTPException(504,'This window exceeded the 60-second computation budget. Try fewer days; your natal chart is unchanged.')
                if await disconnected():raise HTTPException(499,'Transit calculation cancelled.')
                await asyncio.sleep(.05)
            status,payload=await asyncio.to_thread(parent.recv)
            if status!='ok':raise ValueError(payload)
            return dict(**payload,computation=dict(seconds=round(time.monotonic()-started,3),deadline_seconds=self.deadline,native_days=days))
        finally:
            if process.pid:
                if process.is_alive():process.terminate()
                await asyncio.to_thread(process.join,2)
                if process.is_alive():process.kill();await asyncio.to_thread(process.join,2)
                process.close()
            parent.close();child.close();self.slot.release()
