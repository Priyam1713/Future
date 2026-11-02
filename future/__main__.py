import argparse
import json
from pathlib import Path
from .knowledge import Registry, Rule
from .astrology import julian_date_ut1, run_calendar

ROOT = Path(__file__).resolve().parents[1]


def load_registry(path=':memory:'):
    registry = Registry(path)
    try:
        for source in json.loads((ROOT/'knowledge/sources.json').read_text(encoding='utf-8')):
            registry.add_source(source)
        registry.ingest_text('usno-jd-notes-v1', 'usno-jd', ROOT/'knowledge/notes/usno-jd-v1.txt',
                             'Formula for Conversion and Introduction', content_kind='original_research_notes')
        fixtures = {f['id']: f for f in json.loads((ROOT/'knowledge/examples.json').read_text())}
        for record in json.loads((ROOT/'knowledge/rules.json').read_text()):
            rule = Rule(**record)
            if rule.status == 'verified':
                if rule.operation != 'gregorian_ut1_to_jd':
                    raise ValueError('No verifier registered for this operation')
                for fid in rule.fixture_ids:
                    f = fixtures[fid]
                    if f['source_id'] != rule.source_id or not f['locator']:
                        raise ValueError('Fixture provenance mismatch')
                    if abs(julian_date_ut1(*f['inputs']) - f['expected_jd']) > 1e-9:
                        raise ValueError(f'Fixture failed: {fid}')
            registry.add_rule(rule)
        return registry
    except Exception:
        registry.close()
        raise


def main():
    parser = argparse.ArgumentParser(description='Local knowledge pipeline and first astronomy component')
    parser.add_argument('--database', default=':memory:')
    sub = parser.add_subparsers(dest='command', required=True)
    search = sub.add_parser('search')
    search.add_argument('query')
    calendar = sub.add_parser('calendar')
    calendar.add_argument('year', type=int)
    calendar.add_argument('month', type=int)
    calendar.add_argument('day', type=int)
    calendar.add_argument('hour_ut1', type=float)
    natal = sub.add_parser('natal')
    natal.add_argument('local')
    natal.add_argument('zone')
    natal.add_argument('latitude', type=float)
    natal.add_argument('longitude', type=float)
    natal.add_argument('--fold', type=int, choices=[0,1])
    natal.add_argument('--houses', choices=['whole-sign','equal'], default='whole-sign')
    natal.add_argument('--tradition', default='modern psychological')
    natal.add_argument('--kernel', default=str(ROOT/'data/de440s.bsp'))
    natal.add_argument('--orbs', help='JSON mapping of aspect angle to orb')
    args = parser.parse_args()
    if args.command == 'natal':
        from .natal import SkyfieldEphemeris, Settings, chart
        result = chart(SkyfieldEphemeris(args.kernel), args.local,args.zone,args.latitude,args.longitude,
                       Settings(tradition=args.tradition,houses=args.houses),args.fold,
                       {int(k):float(v) for k,v in json.loads(args.orbs).items()} if args.orbs else None)
        from .interpretations import explain
        registry = load_registry(args.database)
        try:
            result['interpretations'] = explain(result,registry)
        finally:
            registry.close()
        print(json.dumps(result,indent=2))
        return
    registry = load_registry(args.database)
    try:
        result = registry.search(args.query, ['usno-jd']) if args.command == 'search' else run_calendar(
            registry, args.year, args.month, args.day, args.hour_ut1)
        print(json.dumps(result, indent=2))
    finally:
        registry.close()


if __name__ == '__main__':
    main()
