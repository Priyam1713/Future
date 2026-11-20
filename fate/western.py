"""Consumer adapter: the native natal calculation and source composition stay untouched."""
from pathlib import Path
from threading import RLock
from functools import lru_cache
import json
import unicodedata
from zoneinfo import ZoneInfoNotFoundError, available_timezones

from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Literal
from future.natal import SkyfieldEphemeris, Settings, chart
from future.core_readings import placements
from future.knowledge import Registry

ROOT = Path(__file__).resolve().parents[1]


class WesternInput(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    local: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?$')
    zone: str = Field(min_length=1, max_length=80)
    latitude: float = Field(gt=-90, lt=90, allow_inf_nan=False)
    longitude: float = Field(ge=-180, le=180, allow_inf_nan=False)
    houses: Literal['whole-sign', 'equal', 'porphyry', 'placidus', 'regiomontanus', 'campanus'] = 'whole-sign'
    fold: Literal[0, 1] | None = None

    @field_validator('fold', mode='before')
    @classmethod
    def explicit_fold(cls, value):
        if value is not None and type(value) is not int:
            raise ValueError('A repeated-time choice must be integer 0 or 1.')
        return value


class WesternService:
    def __init__(self):
        self.lock = RLock()
        self.ephemeris = None

    def get_ephemeris(self):
        with self.lock:
            if self.ephemeris is None:
                self.ephemeris = SkyfieldEphemeris(ROOT / 'data/de440s.bsp')
            return self.ephemeris

    def read(self, q):
        if q.zone not in available_timezones():
            raise ValueError('Choose a recognized IANA timezone, such as Asia/Kolkata.')
        with self.lock:
            try:
                result = chart(self.get_ephemeris(), q.local, q.zone, q.latitude, q.longitude,
                               Settings(houses=q.houses), q.fold)
            except ZoneInfoNotFoundError as exc:
                raise ValueError('The IANA timezone is unavailable.') from exc
            registry = Registry()
            try:
                result['reading'] = placements(result, registry)
            finally:
                registry.close()
            return result

    def close(self):
        with self.lock:
            if self.ephemeris is not None:
                self.ephemeris.kernel.close()
                self.ephemeris = None


def normalize(value):
    return ''.join(c for c in unicodedata.normalize('NFKD', value.casefold()) if not unicodedata.combining(c))


@lru_cache(maxsize=1)
def places():
    rows = json.loads((ROOT / 'fate/data/places-v1.json').read_text(encoding='utf-8'))
    return [(r, normalize(f'{r[1]} {r[2]} {r[3]}')) for r in rows]


def search_places(query):
    q = normalize(query.strip())
    if len(q) < 2:
        return []
    hits = [(r, name) for r, name in places() if all(word in name for word in q.split())]
    hits.sort(key=lambda item: (not normalize(item[0][1]).startswith(q), -item[0][8]))
    return [dict(zip(['id', 'name', 'ascii', 'country', 'region', 'latitude', 'longitude', 'zone'], r[:8])) for r, _ in hits[:12]]
