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
    from .houses import SYSTEMS
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
    natal.add_argument('--houses', choices=SYSTEMS, default='whole-sign')
    natal.add_argument('--tradition', default='modern psychological')
    natal.add_argument('--kernel', default=str(ROOT/'data/de440s.bsp'))
    natal.add_argument('--orbs', help='JSON mapping of aspect angle to orb')
    natal.add_argument('--profections-date',help='Optional explicit annual symbolic context at offset-aware datetime')
    transit=sub.add_parser('forecast')
    transit.add_argument('local')
    transit.add_argument('zone')
    transit.add_argument('latitude',type=float)
    transit.add_argument('longitude',type=float)
    transit.add_argument('start',help='ISO datetime with explicit UTC offset')
    transit.add_argument('--days',type=int,default=30)
    transit.add_argument('--fold',type=int,choices=[0,1])
    transit.add_argument('--houses',choices=SYSTEMS,default='whole-sign')
    transit.add_argument('--tradition',default='modern psychological')
    transit.add_argument('--kernel',default=str(ROOT/'data/de440s.bsp'))
    transit.add_argument('--bodies',help='Comma-separated transiting planets')
    transit.add_argument('--orbs',help='JSON mapping of aspect angle to orb')
    transit.add_argument('--format',choices=['json','markdown'],default='json')
    transit.add_argument('--profections',action='store_true',help='Append separately labeled Hellenistic annual context')
    prog=sub.add_parser('progressions')
    prog.add_argument('local')
    prog.add_argument('zone')
    prog.add_argument('latitude',type=float)
    prog.add_argument('longitude',type=float)
    prog.add_argument('target',help='ISO target datetime with explicit offset')
    prog.add_argument('--fold',type=int,choices=[0,1])
    prog.add_argument('--houses',choices=SYSTEMS,default='placidus')
    prog.add_argument('--tradition',default='modern psychological')
    prog.add_argument('--year-key',choices=['tropical','julian'],default='tropical')
    prog.add_argument('--angles',choices=['none','naibod-ra','solar-arc-mc','secondary-rotation'],default='naibod-ra')
    prog.add_argument('--window-days',type=int,default=365)
    prog.add_argument('--orbs')
    prog.add_argument('--kernel',default=str(ROOT/'data/de440s.bsp'))
    doctrine=sub.add_parser('doctrines')
    doctrine.add_argument('local')
    doctrine.add_argument('zone')
    doctrine.add_argument('latitude',type=float)
    doctrine.add_argument('longitude',type=float)
    doctrine.add_argument('--tradition',choices=['Hellenistic','medieval/traditional'],default='Hellenistic')
    doctrine.add_argument('--houses',choices=SYSTEMS,default='whole-sign')
    doctrine.add_argument('--bounds',choices=['egyptian','lilly-ptolemaic'])
    doctrine.add_argument('--fold',type=int,choices=[0,1])
    doctrine.add_argument('--kernel',default=str(ROOT/'data/de440s.bsp'))
    prof=sub.add_parser('profections')
    prof.add_argument('local');prof.add_argument('zone');prof.add_argument('latitude',type=float);prof.add_argument('longitude',type=float)
    prof.add_argument('target')
    prof.add_argument('--houses',choices=SYSTEMS,default='whole-sign')
    prof.add_argument('--boundary',choices=['birth-time','midnight'],default='birth-time')
    prof.add_argument('--leap-day',choices=['march-1','february-28'],default='march-1')
    prof.add_argument('--fold',type=int,choices=[0,1])
    prof.add_argument('--anniversary-fold',type=int,choices=[0,1])
    prof.add_argument('--kernel',default=str(ROOT/'data/de440s.bsp'))
    sr=sub.add_parser('solar-return')
    sr.add_argument('local');sr.add_argument('zone');sr.add_argument('latitude',type=float);sr.add_argument('longitude',type=float)
    sr.add_argument('year',type=int);sr.add_argument('--return-latitude',type=float);sr.add_argument('--return-longitude',type=float)
    sr.add_argument('--houses',choices=SYSTEMS,default='placidus')
    sr.add_argument('--tradition',default='modern psychological')
    sr.add_argument('--fold',type=int,choices=[0,1]);sr.add_argument('--orbs')
    sr.add_argument('--format',choices=['json','markdown'],default='json')
    sr.add_argument('--kernel',default=str(ROOT/'data/de440s.bsp'))
    args = parser.parse_args()
    if args.command=='solar-return':
        from .natal import SkyfieldEphemeris,Settings,chart
        from .solar_returns import solar_return,register_knowledge,markdown
        e=SkyfieldEphemeris(args.kernel);registry=load_registry(args.database)
        try:
            register_knowledge(registry)
            n=chart(e,args.local,args.zone,args.latitude,args.longitude,Settings(tradition=args.tradition,houses=args.houses),args.fold)
            result=solar_return(e,n,args.year,args.latitude if args.return_latitude is None else args.return_latitude,
                args.longitude if args.return_longitude is None else args.return_longitude,args.houses,
                {int(k):float(v) for k,v in json.loads(args.orbs).items()} if args.orbs else None)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close();e.kernel.close()
        return
    if args.command=='profections':
        from datetime import datetime
        from .natal import SkyfieldEphemeris,Settings,chart
        from .profections import context,register_knowledge
        from .doctrines import register_knowledge as register_doctrines
        e=SkyfieldEphemeris(args.kernel);registry=load_registry(args.database)
        try:
            register_doctrines(registry);register_knowledge(registry)
            n=chart(e,args.local,args.zone,args.latitude,args.longitude,Settings(tradition='Hellenistic',houses=args.houses),args.fold)
            result=context(e,n,datetime.fromisoformat(args.target),boundary=args.boundary,leap_day=args.leap_day,anniversary_fold=args.anniversary_fold)
            print(json.dumps({'natal':n,'annual_profection':result},indent=2))
        finally:registry.close();e.kernel.close()
        return
    if args.command=='doctrines':
        from dataclasses import replace
        from .natal import SkyfieldEphemeris,Settings,chart
        from .doctrines import analyze,DoctrineSettings,register_knowledge
        e=SkyfieldEphemeris(args.kernel)
        registry=load_registry(args.database)
        try:
            register_knowledge(registry)
            n=chart(e,args.local,args.zone,args.latitude,args.longitude,Settings(tradition=args.tradition,houses=args.houses),args.fold)
            config=DoctrineSettings() if args.tradition=='Hellenistic' else DoctrineSettings('lilly-ptolemaic','lilly','lilly-ca113','fixed-day-fortune','dignity-occupancy')
            if args.bounds:config=replace(config,bounds=args.bounds)
            print(json.dumps({'natal':n,'conditions':analyze(e,n,config)},indent=2))
        finally:registry.close();e.kernel.close()
        return
    if args.command=='progressions':
        from datetime import datetime
        from .natal import SkyfieldEphemeris,Settings
        from .progressions import progress,register_knowledge
        e=SkyfieldEphemeris(args.kernel)
        try:
            registry=load_registry(args.database)
            try:register_knowledge(registry)
            finally:registry.close()
            result=progress(e,args.local,args.zone,args.latitude,args.longitude,datetime.fromisoformat(args.target),
                Settings(tradition=args.tradition,houses=args.houses),args.fold,args.year_key,args.angles,
                {int(k):float(v) for k,v in json.loads(args.orbs).items()} if args.orbs else None,args.window_days)
            print(json.dumps(result,indent=2))
        finally:e.kernel.close()
        return
    if args.command=='forecast':
        from datetime import datetime
        from .natal import SkyfieldEphemeris, Settings, chart
        from .transits import forecast
        from .western import load_context,interpreter,natal_context,traditional_configuration_context
        e=SkyfieldEphemeris(args.kernel)
        n=chart(e,args.local,args.zone,args.latitude,args.longitude,Settings(tradition=args.tradition,houses=args.houses),args.fold)
        registry=load_registry(args.database)
        try:
            records=load_context(registry,args.tradition)
            n['knowledge_context']=natal_context(records,n)
            n['traditional_configuration_context']=traditional_configuration_context(n)
            result=forecast(e,n,datetime.fromisoformat(args.start),args.days,
                            {int(k):float(v) for k,v in json.loads(args.orbs).items()} if args.orbs else None,
                            args.bodies.split(',') if args.bodies else None,interpreter(records,n))
            if args.profections:
                from .profections import context,register_knowledge
                register_knowledge(registry)
                result['annual_profection_context']=context(e,n,datetime.fromisoformat(args.start))
                transition=datetime.fromisoformat(result['annual_profection_context']['period']['end_exclusive_utc'])
                result['annual_profection_transitions']=([context(e,n,transition)] if transition<datetime.fromisoformat(result['window']['end_utc']) else [])
            from .forecast_report import present,markdown
            result=present(result)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally: registry.close();e.kernel.close()
        return
    if args.command == 'natal':
        from .natal import SkyfieldEphemeris, Settings, chart
        e=SkyfieldEphemeris(args.kernel)
        result = chart(e, args.local,args.zone,args.latitude,args.longitude,
                       Settings(tradition=args.tradition,houses=args.houses),args.fold,
                       {int(k):float(v) for k,v in json.loads(args.orbs).items()} if args.orbs else None)
        from .interpretations import explain
        registry = load_registry(args.database)
        try:
            result['interpretations'] = explain(result,registry)
            if args.profections_date:
                from datetime import datetime
                from .profections import context,register_knowledge
                register_knowledge(registry)
                result['annual_profection_context']=context(e,result,datetime.fromisoformat(args.profections_date))
        finally:
            registry.close()
            e.kernel.close()
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
