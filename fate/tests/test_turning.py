import asyncio
import copy
from datetime import datetime,timezone
import json
from pathlib import Path
import unittest
from fastapi.testclient import TestClient
from fate.api import create_app
from fate.turning import TransitInput,TransitRunner,calculate_transits,natal_basis
from fate.western import WesternService,WesternInput
from future.knowledge import Registry
from future.natal import SkyfieldEphemeris,signed
from future.transits import forecast,phase
from future.forecast_report import present
from future.western import load_context,interpreter,traditional_configuration_context

ROOT=Path(__file__).resolve().parents[2]
Q=dict(local='1990-07-15T14:30:00',zone='Europe/London',latitude=51.50853,longitude=-.12574,houses='whole-sign',fold=None)
START='2026-11-19T00:00:00Z'


class TurningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        service=WesternService()
        try:cls.natal=service.read(WesternInput(**Q))
        finally:service.close()
        cls.engine=SkyfieldEphemeris(ROOT/'data/de440s.bsp')
    @classmethod
    def tearDownClass(cls):cls.engine.kernel.close()

    def test_native_forecast_report_parity_and_input_immutability(self):
        basis=natal_basis(self.natal);before=copy.deepcopy(basis)
        actual=calculate_transits(basis,START,2,self.engine)
        n=copy.deepcopy(basis);n['traditional_configuration_context']=traditional_configuration_context(n)
        r=Registry()
        try:expected=present(forecast(self.engine,n,datetime.fromisoformat(START),2,interpreter=interpreter(load_context(r,'modern psychological'),n)))
        finally:r.close()
        self.assertEqual(actual['report'],expected)
        self.assertEqual(basis,before)
        self.assertNotIn('birth',actual['report']['natal_summary'])

    def test_samples_are_native_positions_and_native_phases(self):
        actual=calculate_transits(natal_basis(self.natal),START,2,self.engine)
        configs={c['configuration_id']:c for c in actual['report']['configurations']}
        targets={**{k:v['longitude'] for k,v in self.natal['planets'].items()},**self.natal['angles']}
        for sample in actual['sky_samples']:
            _,native=self.engine.positions(datetime.fromisoformat(sample['utc']))
            self.assertEqual(sample['planets'],native)
            for c in sample['contacts']:
                conf=configs[c['configuration_id']];p=native[conf['transiting']]
                error=signed(p['longitude']-targets[conf['natal_target']]-conf['branch_degrees'])
                self.assertEqual(c['phase'],phase(error,p['speed_degrees_per_day']))
                self.assertEqual(c['orb'],abs(error))

    def test_strict_day_and_offset_bounds(self):
        origin={'natal':{},'proof':'x'}
        for days in [0,31,True,7.5,'7']:
            with self.assertRaises(ValueError):TransitInput(origin=origin,start=START,days=days)
        for start in ['2026-11-19','2026-11-19T00:00:00','1849-12-01T00:00:00Z','2149-12-25T00:00:00Z']:
            with self.assertRaises(ValueError):TransitInput(origin=origin,start=start,days=7)

    def test_signed_origin_has_no_birth_inputs_and_accepts_js_integral_float_roundtrip(self):
        with TestClient(create_app(signing_key=b'fixture')) as c:
            env=c.post('/api/western',json=Q).json();origin=env['transit_origin']
            self.assertEqual(origin['natal'],json.loads(json.dumps(natal_basis(self.natal))))
            self.assertFalse(set(origin['natal'])&{'birth','times','reading','receipt'})
            # JSON.stringify serializes integral JS Numbers without '.0'.
            def js(v):
                if isinstance(v,dict):return {k:js(x) for k,x in v.items()}
                if isinstance(v,list):return [js(x) for x in v]
                return int(v) if type(v)is float and v.is_integer() else v
            r=c.post('/api/western/transits',json={'origin':js(origin),'start':START,'days':1})
            self.assertEqual(r.status_code,200,r.text)
            self.assertEqual(len(r.json()['sky_samples']),1)
            self.assertEqual(r.headers['cache-control'],'no-store')
            self.assertNotIn('birth',r.json()['report']['natal_summary'])

    def test_missing_forged_expired_or_restarted_proofs_never_reconstruct_birth(self):
        clock=[1000]
        with TestClient(create_app(signing_key=b'first',clock=lambda:clock[0])) as c:
            origin=c.post('/api/western',json=Q).json()['transit_origin']
            altered=copy.deepcopy(origin);altered['natal']['planets']['Sun']['longitude']+=1
            for q in [{'origin':altered,'start':START,'days':1},{'origin':{'natal':{},'proof':'missing'},'start':START,'days':1}]:
                self.assertEqual(c.post('/api/western/transits',json=q).status_code,403)
            clock[0]=4601
            self.assertEqual(c.post('/api/western/transits',json={'origin':origin,'start':START,'days':1}).status_code,403)
        with TestClient(create_app(signing_key=b'second')) as c:
            self.assertEqual(c.post('/api/western/transits',json={'origin':origin,'start':START,'days':1}).status_code,403)

    def test_raw_birth_and_saved_snapshot_inputs_are_not_a_transit_api_contract(self):
        with TestClient(create_app()) as c:
            for payload in [{'start':START,'days':1,'birth':Q},{'origin':{'natal':{},'proof':'x'},'start':START,'days':1,'question':'private'}]:
                self.assertEqual(c.post('/api/western/transits',json=payload).status_code,422)

    def test_runner_has_hard_timeout_and_releases_single_slot(self):
        async def check():
            runner=TransitRunner(deadline=0)
            async def connected():return False
            with self.assertRaises(Exception) as e:await runner.run(natal_basis(self.natal),START,30,connected)
            self.assertEqual(e.exception.status_code,504)
            self.assertTrue(runner.slot.acquire(blocking=False));runner.slot.release()
        asyncio.run(check())

    def test_runner_cancels_client_disconnect_and_rejects_busy_without_queue(self):
        async def check():
            runner=TransitRunner()
            async def disconnected():return True
            with self.assertRaises(Exception) as e:await runner.run(natal_basis(self.natal),START,30,disconnected)
            self.assertEqual(e.exception.status_code,499)
            runner.slot.acquire()
            try:
                with self.assertRaises(Exception) as e:await runner.run({},START,1,disconnected)
                self.assertEqual(e.exception.status_code,429)
            finally:runner.slot.release()
        asyncio.run(check())

    def test_frozen_source_edition_matches_existing_native_context(self):
        from fate.build_turning import build
        archive=json.loads((ROOT/'fate/web/src/turning/reference-v1.json').read_text(encoding='utf-8'))
        self.assertEqual(archive,build());self.assertEqual(len(archive['records']),62)


if __name__=='__main__':unittest.main()
