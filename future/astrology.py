"""First Western Astrology component: explicit UT1 calendar arithmetic.

Not a birth-chart engine. No UTC/UT1 approximation, ephemeris or interpretation.
"""
from datetime import date
import math


def julian_date_ut1(year: int, month: int, day: int, hour_ut1: float):
    if any(type(x) is not int for x in (year, month, day)):
        raise ValueError('Calendar fields must be integers')
    if not 1801 <= year <= 2099:
        raise ValueError('Supported Gregorian years: 1801..2099')
    date(year, month, day)
    if isinstance(hour_ut1, bool) or not isinstance(hour_ut1, (int, float)):
        raise ValueError('UT1 hour must be a number')
    if not math.isfinite(hour_ut1) or not 0 <= hour_ut1 < 24:
        raise ValueError('UT1 hour must be finite and in [0,24)')
    correction = -0.5 * (1 if 100*year + month - 190002.5 > 0 else -1) + 0.5
    return (367*year - math.trunc(7*(year + math.trunc((month+9)/12))/4)
            + math.trunc(275*month/9) + day + 1721013.5 + hour_ut1/24 + correction)


def run_calendar(registry, year, month, day, hour_ut1):
    rules = registry.select_rules(1, 'natal', 'shared astronomical computation')
    rule = next((r for r in rules if r['operation'] == 'gregorian_ut1_to_jd'), None)
    if rule is None:
        raise ValueError('No verified calendar rule for this scope')
    if rule['parameters'] != {'min_year': 1801, 'max_year': 2099, 'calendar': 'Gregorian', 'time_scale': 'UT1'}:
        raise ValueError('Rule parameters do not match the implemented calculation')
    jd = julian_date_ut1(year, month, day, hour_ut1)
    context = registry.search('Julian Gregorian UT1', [rule['source_id']])
    return {
        'technique_id': 1, 'variation': 'natal', 'component': 'calendar conversion',
        'inputs': {'year': year, 'month': month, 'day': day, 'hour_ut1': hour_ut1},
        'result': {'julian_date_ut1': jd},
        'rules_applied': [{'id': rule['id'], 'version': rule['version'], 'locator': rule['locator']}],
        'interpretation': None,
        'explanation': f'Gregorian input in UT1 converts to Julian date {jd}. This is calendar arithmetic.',
        'retrieved_references': [{'source_id': r['source_id'], 'locator': r['locator'],
                                  'document_sha256': r['digest']} for r in context],
        'reproducibility': {'algorithm': 'USNO Almanac for Computers formula', 'version': '0.1.0'},
        'limitations': ['Not a natal chart or prediction.', 'Input must already be UT1; UTC and local time conversion are not implemented.',
                        'Gregorian calendar only, 1801 through 2099.'],
    }
