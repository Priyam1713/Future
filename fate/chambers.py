"""Consumer projections for the four native chambers."""
from datetime import datetime, timezone
from typing import Annotated, Literal
from zoneinfo import available_timezones

from pydantic import BaseModel, ConfigDict, Field, field_validator

from future import chinese, chinese_readings, iching, runes, vedic, vedic_timing
from future.iching_cast import PROTOCOL as COIN_PROTOCOL
from future.natal import SkyfieldEphemeris
from .western import ROOT

GRAHAS = (*vedic.CLASSICAL, 'Rahu', 'Ketu')
PILLARS = ('year', 'month', 'day', 'hour')


class ChamberInput(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)


class RecordedBirth(ChamberInput):
    local: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?$')
    zone: str = Field(min_length=1, max_length=80)
    latitude: float = Field(gt=-90, lt=90, allow_inf_nan=False)
    longitude: float = Field(ge=-180, le=180, allow_inf_nan=False)
    fold: Literal[0, 1] | None = None

    @field_validator('fold', mode='before')
    @classmethod
    def explicit_fold(cls, value):
        if value is not None and type(value) is not int:
            raise ValueError('A repeated-time choice must be integer 0 or 1.')
        return value

    @field_validator('zone')
    @classmethod
    def iana_zone(cls, value):
        if value not in available_timezones():
            raise ValueError('Choose a recognized IANA timezone.')
        return value

    def args(self):
        return self.local, self.zone, self.latitude, self.longitude, self.fold


class VedicInput(RecordedBirth):
    oracle: Literal[2]
    target: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$')
    year_key: Literal['pvr-2000-savana', 'solar-365.2425'] = 'pvr-2000-savana'


class BaziInput(RecordedBirth):
    oracle: Literal[3]
    profile: Literal['civil-zi23', 'standard-zi23', 'civil-split-zi'] = 'civil-zi23'


class CoinInput(ChamberInput):
    oracle: Literal[18]
    seed: str = Field(min_length=1, max_length=128)


class RuneInput(ChamberInput):
    oracle: Literal[19]
    seed: str = Field(min_length=1, max_length=128)
    spread: Literal['one', 'three']


Input = Annotated[VedicInput | BaziInput | CoinInput | RuneInput, Field(discriminator='oracle')]


def chart_for(q, pool):
    # Reuse the existing local kernel and its lock without sharing personal inputs.
    with pool.lock:
        if pool.ephemeris is None:
            pool.ephemeris = SkyfieldEphemeris(ROOT / 'data/de440s.bsp')
        engine = pool.ephemeris
        if isinstance(q, VedicInput):
            target = datetime.fromisoformat(q.target).replace(tzinfo=timezone.utc)
            return vedic_timing.enrich(vedic.d1(engine, *q.args()), target, q.year_key, True)
        return chinese_readings.enrich(chinese.chart(engine, *q.args(), q.profile))


def read(q, pool):
    if isinstance(q, RecordedBirth):
        return chart_for(q, pool)
    common = dict(schema_version=1, task='symbolic_reading', mode='seeded', seed=q.seed)
    if isinstance(q, CoinInput):
        return iching.read(dict(common, profile=iching.PROFILE, reading_policy=iching.POLICY,
            method='three-coin', line_order='bottom_to_top', protocol=COIN_PROTOCOL))
    return runes.read(dict(common, profile=runes.PROFILE, spread=q.spread,
        protocol=runes.PROTOCOL, orientation_policy='upright_only'))


def period(row):
    # The chapter stores UTC calendar-day labels rather than precise endpoints.
    return [row['lord'], row['start_inclusive_utc'][:10], row['end_exclusive_utc'][:10]]


def snapshot(result):
    oracle = result['technique_id']
    base = dict(oracle=oracle, profile=result['profile'])
    if oracle == 2:
        dasha = result['vimshottari']
        mansion = result['moon_nakshatra']
        d9 = result['d9']
        return dict(base, asc=[result['ascendant']['longitude'], result['ascendant']['sign_index']],
            d9Asc=[d9['ascendant']['longitude_symbolic'], d9['ascendant']['sign_index']],
            planets=[[result['planets'][n]['longitude'], result['planets'][n]['sign_index'],
                      result['planets'][n]['house'], d9['planets'][n]['longitude_symbolic'],
                      d9['planets'][n]['sign_index'], d9['planets'][n]['house']] for n in GRAHAS],
            mansion=[mansion['index'], mansion['pada'], mansion['boundary_sensitive']],
            year=dasha['year_key'], main=[period(dasha['current']['mahadasa']),
                *map(period, dasha['upcoming']['mahadasas'])],
            sub=list(map(period, dasha['current_md_antardashas'])),
            active=next(i for i, row in enumerate(dasha['current_md_antardashas'])
                if row == dasha['current']['antardasha']))
    if oracle == 3:
        return dict(base, pairs=[result['pillars'][name]['sexagenary_index'] for name in PILLARS])
    if oracle == 18:
        c = result['calculation']
        return dict(base, values=c['values'], figures=[c['initial']['number'], c['resulting']['number']])
    return dict(base, runes=[row['rune_id'] for row in result['replay']['selected']])


def commentary_sources(result):
    """Public symbolic excerpts only. Birth inputs, questions and replay data stay out."""
    oracle = result['technique_id']
    if oracle == 2:
        return [('vedic.d9', result['d9']['interpretation']['topics']),
                ('vedic.vimshottari', result['vimshottari']['interpretation']['method'])]
    if oracle == 3:
        source = result['reading']['day_master']
        return [(source['id'], source['text'])]
    if oracle == 18:
        texts = [result['calculation']['initial']['judgment'],
                 *result['changing_line_texts'], result['calculation']['resulting']['judgment']]
        return list(dict.fromkeys((row['rule_id'], row['text']) for row in texts))
    return [(row['rune']['id'], row['rune']['composition']['reflection'])
            for row in result['readings']]
