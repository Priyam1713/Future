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
    elect=sub.add_parser('election')
    elect.add_argument('category',choices=['retain-received-money','rapid-use-received-money'])
    elect.add_argument('start');elect.add_argument('end')
    elect.add_argument('latitude',type=float);elect.add_argument('longitude',type=float)
    elect.add_argument('--profile',choices=['ramesey-retain-money','ramesey-rapid-use-money'],default='ramesey-retain-money')
    elect.add_argument('--tradition',default='Ramesey 1653')
    elect.add_argument('--houses',choices=SYSTEMS,default='regiomontanus')
    elect.add_argument('--require',help='Comma-separated supported rule IDs; omitted rules are explicitly reported')
    elect.add_argument('--min-minutes',type=float,default=5)
    elect.add_argument('--utc-hours',nargs=2,type=int)
    elect.add_argument('--ascendant-signs',help='Comma-separated zero-based sign indices')
    elect.add_argument('--angle-step',choices=[5,10],type=int,default=10)
    elect.add_argument('--kernel',default=str(ROOT/'data/de440s.bsp'))
    zr=sub.add_parser('releasing',help='Source-named Spirit/Fortune Zodiacal Releasing')
    zr.add_argument('local');zr.add_argument('zone');zr.add_argument('latitude',type=float);zr.add_argument('longitude',type=float)
    zr.add_argument('start',help='Offset-aware range start');zr.add_argument('end',help='Offset-aware exclusive end')
    zr.add_argument('--lot',choices=['Spirit','Fortune'],default='Spirit')
    zr.add_argument('--levels',type=int,choices=[1,2,3,4],default=4)
    zr.add_argument('--profile',choices=['brennan-2019-360'],default='brennan-2019-360')
    zr.add_argument('--fold',type=int,choices=[0,1]);zr.add_argument('--houses',choices=SYSTEMS,default='whole-sign')
    zr.add_argument('--format',choices=['json','markdown'],default='json')
    zr.add_argument('--kernel',default=str(ROOT/'data/de440s.bsp'))
    jy=sub.add_parser('jyotish',help='Named Parashari sidereal D1 and Moon nakshatra')
    jy.add_argument('local');jy.add_argument('zone');jy.add_argument('latitude',type=float);jy.add_argument('longitude',type=float)
    jy.add_argument('--fold',type=int,choices=[0,1]);jy.add_argument('--format',choices=['json','markdown'],default='json')
    jy.add_argument('--kernel',default=str(ROOT/'data/de440s.bsp'))
    jy.add_argument('--d9',action='store_true',help='Add separately labeled Navamsa')
    jy.add_argument('--target',help='Offset-aware target for Vimshottari current/upcoming periods')
    jy.add_argument('--year-key',choices=['pvr-2000-savana','solar-365.2425'],default='pvr-2000-savana')
    from .chinese import PROFILES
    bz=sub.add_parser('bazi')
    bz.add_argument('local');bz.add_argument('zone');bz.add_argument('latitude',type=float);bz.add_argument('longitude',type=float)
    bz.add_argument('--fold',type=int,choices=[0,1])
    bz.add_argument('--profile',choices=PROFILES,default='civil-zi23')
    bz.add_argument('--format',choices=['json','markdown'],default='json')
    bz.add_argument('--kernel',default=str(ROOT/'data/de440s.bsp'))
    nu=sub.add_parser('numerology')
    nu.add_argument('birth');nu.add_argument('name');nu.add_argument('target')
    nu.add_argument('--basis',required=True,choices=['birth','current'])
    nu.add_argument('--y-roles',default='')
    nu.add_argument('--format',choices=['json','markdown'],default='json')
    ho=sub.add_parser('horary',help='Lilly Horary Core v1 diagnostic scope; question judgment experimental')
    ho.add_argument('question');ho.add_argument('category')
    ho.add_argument('local');ho.add_argument('zone');ho.add_argument('latitude',type=float);ho.add_argument('longitude',type=float)
    ho.add_argument('--protocol',required=True,choices=['advice-begins'])
    ho.add_argument('--profile',default='lilly-1647-advice-intent')
    ho.add_argument('--fold',type=int,choices=[0,1])
    ho.add_argument('--format',choices=['json','markdown'],default='json')
    ho.add_argument('--kernel',default=str(ROOT/'data/de440s.bsp'))
    mi=sub.add_parser('mundane-ingress',help='Four exact cardinal ingresses and Green-based local chart components')
    mi.add_argument('year',type=int);mi.add_argument('zone');mi.add_argument('latitude',type=float);mi.add_argument('longitude',type=float)
    mi.add_argument('--profile',default='green-1911-tropical-placidus-v1')
    mi.add_argument('--historical-duration',action='store_true')
    mi.add_argument('--format',choices=['json','markdown'],default='json')
    mi.add_argument('--kernel',default=str(ROOT/'data/de440s.bsp'))
    mc=sub.add_parser('mundane-cycle',help='Selected exact Jupiter–Saturn conjunctions; no fixed orbs/duration')
    mc.add_argument('start');mc.add_argument('end');mc.add_argument('zone');mc.add_argument('latitude',type=float);mc.add_argument('longitude',type=float)
    mc.add_argument('--profile',default='green-1911-tropical-placidus-v1')
    mc.add_argument('--format',choices=['json','markdown'],default='json')
    mc.add_argument('--kernel',default=str(ROOT/'data/de440s.bsp'))
    acg=sub.add_parser('astrocartography')
    acg.add_argument('local')
    acg.add_argument('zone')
    acg.add_argument('latitude',type=float)
    acg.add_argument('longitude',type=float)
    acg.add_argument('--fold',type=int,choices=[0,1])
    acg.add_argument('--houses',choices=SYSTEMS,default='placidus')
    acg.add_argument('--destinations',default='[]',help='JSON list: name,latitude,longitude,zone')
    acg.add_argument('--query',nargs=2,type=float,metavar=('LAT','LON'))
    acg.add_argument('--bodies',help='Comma-separated supported planets; default all ten')
    acg.add_argument('--tolerance',type=float,default=.01)
    acg.add_argument('--uncertainty-minutes',type=float,default=0)
    acg.add_argument('--profile',default='geocentric-apparent-geometric-v1')
    acg.add_argument('--format',choices=['json','markdown','geojson'],default='json')
    acg.add_argument('--kernel',default=str(ROOT/'data/de440s.bsp'))
    palm=sub.add_parser('palmistry')
    palm.add_argument('observations',help='Path to source-profiled manual-observation JSON')
    palm.add_argument('--format',choices=['json','markdown'],default='json')
    face=sub.add_parser('face-reference')
    face.add_argument('input',help='Path to manual region annotations or named historical schematic JSON')
    face.add_argument('--format',choices=['json','markdown'],default='json')
    phren=sub.add_parser('phrenology-reference')
    phren.add_argument('input',help='Path to historical schematic/label selection JSON; no personal data')
    phren.add_argument('--format',choices=['json','markdown'],default='json')
    moles=sub.add_parser('moleosophy-reference')
    moles.add_argument('input',help='Path to historical region/entry or source-example JSON; no personal skin data')
    moles.add_argument('--format',choices=['json','markdown'],default='json')
    podo=sub.add_parser('podomancy-reference')
    podo.add_argument('input',help='Path to documentary foot-region/entry selection JSON; no personal foot data')
    podo.add_argument('--format',choices=['json','markdown'],default='json')
    graph=sub.add_parser('graphology-reference')
    graph.add_argument('input',help='Path to manual descriptive or published-example JSON; no writer assessment')
    graph.add_argument('--format',choices=['json','markdown'],default='json')
    aura=sub.add_parser('aura-reference')
    aura.add_argument('input',help='Manual symbolic colors or published teaching example JSON; no personal inference')
    aura.add_argument('--format',choices=['json','markdown'],default='json')
    iris=sub.add_parser('iridology-reference')
    iris.add_argument('input',help='Historical schematic/legend selection JSON; no patient iris analysis')
    iris.add_argument('--format',choices=['json','markdown'],default='json')
    tarot=sub.add_parser('tarot')
    tarot.add_argument('input',help='Path to seeded/manual symbolic Tarot reading JSON')
    tarot.add_argument('--format',choices=['json','markdown'],default='json')
    oracle=sub.add_parser('oracle')
    oracle.add_argument('input',help='Named deck seeded/manual symbolic Oracle reading JSON')
    oracle.add_argument('--format',choices=['json','markdown'],default='json')
    iching=sub.add_parser('iching')
    iching.add_argument('input',help='Manual/seeded source-bounded I Ching reading JSON')
    iching.add_argument('--format',choices=['json','markdown'],default='json')
    runes=sub.add_parser('runes')
    runes.add_argument('input',help='Named Elder24 manual/seeded symbolic rune reading JSON')
    runes.add_argument('--format',choices=['json','markdown'],default='json')
    pendulum=sub.add_parser('pendulum')
    pendulum.add_argument('input',help='Manual calibrated observation or seeded symbolic Pendulum JSON')
    pendulum.add_argument('--format',choices=['json','markdown'],default='json')
    scrying=sub.add_parser('scrying')
    scrying.add_argument('input',help='Historical guided session and user-entered Scrying journal JSON')
    scrying.add_argument('--format',choices=['json','markdown'],default='json')
    mirror=sub.add_parser('mirror-scrying')
    mirror.add_argument('input',help='Source-specific Mirror guidance and user-entered journal JSON')
    mirror.add_argument('--format',choices=['json','markdown'],default='json')
    dream=sub.add_parser('dream')
    dream.add_argument('input',help='Historical Dream taxonomy,explicit contextual references andmanual journal JSON')
    dream.add_argument('--format',choices=['json','markdown'],default='json')
    automatic=sub.add_parser('automatic-writing')
    automatic.add_argument('input',help='Manual writing events, immutable draft segments and linked revisions JSON')
    automatic.add_argument('--format',choices=['json','markdown'],default='json')
    akashic=sub.add_parser('akashic-reference')
    akashic.add_argument('input',help='Named source concepts, explicit question purpose and voluntary reflection JSON')
    akashic.add_argument('--format',choices=['json','markdown'],default='json')
    tasseography=sub.add_parser('tasseography')
    tasseography.add_argument('input',help='Kent ordinary-cup manual placements and source-conditioned symbolic references JSON')
    tasseography.add_argument('--format',choices=['json','markdown'],default='json')
    coffee=sub.add_parser('coffee-reading')
    coffee.add_argument('input',help='Manual Turkish coffee observations and conditional source references JSON')
    coffee.add_argument('--format',choices=['json','markdown'],default='json')
    pyro=sub.add_parser('pyromancy')
    pyro.add_argument('input',help='Manual candle flame and jar-soot observations with source qualifications JSON')
    pyro.add_argument('--format',choices=['json','markdown'],default='json')
    hydro=sub.add_parser('hydromancy')
    hydro.add_argument('input',help='Manual water-specific source conditions andvoluntary observations JSON')
    hydro.add_argument('--format',choices=['json','markdown'],default='json')
    aero=sub.add_parser('aeromancy')
    aero.add_argument('input',help='Manual atmospheric observations andregional historical source conditions JSON')
    aero.add_argument('--format',choices=['json','markdown'],default='json')
    geo=sub.add_parser('geomancy')
    geo.add_argument('input',help='Manual Turner1655 fifteen-position shield or named figure catalog JSON')
    geo.add_argument('--format',choices=['json','markdown'],default='json')
    litho=sub.add_parser('lithomancy')
    litho.add_argument('input',help='Manual Howard general-set placements, explicit anchor and integer coordinate frame JSON')
    litho.add_argument('--format',choices=['json','markdown'],default='json')
    osteo=sub.add_parser('osteomancy')
    osteo.add_argument('input',help='Documentary AFE Shang charge references, source groups and structured comparisons JSON')
    osteo.add_argument('--format',choices=['json','markdown'],default='json')
    biblio=sub.add_parser('bibliomancy')
    biblio.add_argument('input',help='Edition-pinned manual sentence paths or historical Homeric indexing-only reference JSON')
    biblio.add_argument('--format',choices=['json','markdown'],default='json')
    clero=sub.add_parser('cleromancy')
    clero.add_argument('input',help='Named Greek Alphabet Oracle single declared marked-lot or source catalog JSON')
    clero.add_argument('--format',choices=['json','markdown'],default='json')
    augur=sub.add_parser('augury')
    augur.add_argument('input',help='Manual Roman bird-sign source observations or exact context references JSON')
    augur.add_argument('--format',choices=['json','markdown'],default='json')
    harus=sub.add_parser('haruspicy')
    harus.add_argument('input',help='Manual Roman historical entrail conditions or documentary source references JSON')
    harus.add_argument('--format',choices=['json','markdown'],default='json')
    feng=sub.add_parser('feng-shui')
    feng.add_argument('input',help='Exact integer-tenth24mountain source heading,reference or comparison JSON')
    feng.add_argument('--format',choices=['json','markdown'],default='json')
    rv=sub.add_parser('remote-viewing')
    rv.add_argument('input',help='Versioned offline trial create/apply/packet/report/summary request JSON')
    rv.add_argument('--asset-root',default=str(ROOT),help='Root for verified relative local asset references')
    rv.add_argument('--export-dir',help='New directory for allowlisted blind packet and neutral PNG exports only')
    rv.add_argument('--format',choices=['json','markdown'],default='json')
    pd=sub.add_parser('prophetic-dreams')
    pd.add_argument('input',help='Prospective dream/event ledger create/apply/report/judge/reference JSON')
    pd.add_argument('--asset-root',default=str(ROOT))
    pd.add_argument('--export-dir',help='New directory for consented allowlisted text judge packet only')
    pd.add_argument('--format',choices=['json','markdown'],default='json')
    ip=sub.add_parser('intuitive-prediction')
    ip.add_argument('input',help='Source-specific heuristic or exact binary forecast evaluation request JSON')
    ip.add_argument('--asset-root',default=str(ROOT))
    ip.add_argument('--format',choices=['json','markdown'],default='json')
    dr=sub.add_parser('deja-reve')
    dr.add_argument('input',help='Private structured annotation,source reference or finite prior-dream provenance request JSON')
    dr.add_argument('--format',choices=['json','markdown'],default='json')
    ai=sub.add_parser('ai-predictive-modeling')
    ai.add_argument('input',help='Offline CPU forecast,evaluation,benchmark or reference scoring request JSON')
    ai.add_argument('--format',choices=['json','markdown'],default='json')
    qp=sub.add_parser('quantum-probability-forecasting')
    qp.add_argument('input',help='Offline small circuit simulation,sampling,comparison,reference or report JSON')
    qp.add_argument('--format',choices=['json','markdown'],default='json')
    sf=sub.add_parser('superforecasting')
    sf.add_argument('input',help='Offline versioned binary question,class,forecast,update,resolution orscore request JSON')
    sf.add_argument('--format',choices=['json','markdown'],default='json')
    args = parser.parse_args()
    if args.command=='superforecasting':
        import sys
        from .scrying import load_input
        from .superforecasting import read,markdown
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError,TypeError,KeyError,OverflowError):
                result=dict(status='rejected',error='Superforecasting request rejected',result=None)
                print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,ensure_ascii=False,indent=2))
        finally:registry.close()
        return
    if args.command=='quantum-probability-forecasting':
        import sys
        from .scrying import load_input
        from .quantum_probability_forecasting import read,markdown
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError,TypeError,KeyError,OverflowError):
                result=dict(status='rejected',error='CPU quantum probability request rejected',result=None)
                print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,ensure_ascii=False,indent=2))
        finally:registry.close()
        return
    if args.command=='ai-predictive-modeling':
        import sys
        from .scrying import load_input
        from .ai_predictive_modeling import read,markdown
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError,TypeError,KeyError,OverflowError):
                result=dict(status='rejected',error='CPU forecasting request rejected',result=None)
                print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,ensure_ascii=False,indent=2))
        finally:registry.close()
        return
    if args.command=='deja-reve':
        import sys
        from .scrying import load_input
        from .deja_reve import read,markdown
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError,TypeError,KeyError):
                result=dict(status='rejected',error='Deja Reve request rejected',result=None)
                print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,ensure_ascii=False,indent=2))
        finally:registry.close()
        return
    if args.command=='intuitive-prediction':
        import sys
        from .scrying import load_input
        from .intuitive_prediction import read,markdown
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),args.asset_root,registry)
            except (ValueError,OSError,TypeError,KeyError):
                result=dict(status='rejected',error='Intuitive prediction request rejected',result=None)
                print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,ensure_ascii=False,indent=2))
        finally:registry.close()
        return
    if args.command=='prophetic-dreams':
        import sys
        from .scrying import load_input
        from .prophetic_dreams import read,markdown,export_packet
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:
                result=read(load_input(args.input),args.asset_root,registry)
                if args.export_dir:export_packet(result,args.export_dir)
            except (ValueError,OSError):
                result=dict(visibility='public_error',status='rejected',error='Dream ledger request rejected',prophetic_dreams_report=None)
                print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,ensure_ascii=False,indent=2))
            if result.get('accepted') is False:raise SystemExit(2)
        finally:registry.close()
        return
    if args.command=='remote-viewing':
        import sys
        from .scrying import load_input
        from .remote_viewing import read,markdown,export_packet
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:
                result=read(load_input(args.input),args.asset_root,registry)
                if args.export_dir:export_packet(result,args.export_dir)
            except (ValueError,OSError) as exc:
                # Do not echo paths/private request text in a public error response.
                result=dict(visibility='public_error',status='rejected',error='Remote Viewing request rejected',remote_viewing_report=None)
                print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,ensure_ascii=False,indent=2))
            if result.get('accepted') is False:raise SystemExit(2)
        finally:registry.close()
        return
    if args.command=='feng-shui':
        import sys
        from .scrying import load_input
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:
                from .feng_shui import read,markdown
                result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                from html import escape
                print(json.dumps(dict(status='rejected',error=str(exc),feng_shui_report=None),indent=2) if args.format=='json' else '# Feng Shui request rejected\n\n'+escape(str(exc))+'\n')
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,ensure_ascii=False,indent=2))
        finally:registry.close()
        return
    if args.command=='haruspicy':
        import sys
        from .scrying import load_input
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:
                from .haruspicy import read,markdown
                result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                from html import escape
                print(json.dumps(dict(status='rejected',error=str(exc),haruspicy_report=None),indent=2) if args.format=='json' else '# Haruspicy request rejected\n\n'+escape(str(exc))+'\n')
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,ensure_ascii=False,indent=2))
        finally:registry.close()
        return
    if args.command=='augury':
        import sys
        from .scrying import load_input
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:
                from .augury import read,markdown
                result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                from html import escape
                print(json.dumps(dict(status='rejected',error=str(exc),augury_report=None),indent=2) if args.format=='json' else '# Augury request rejected\n\n'+escape(str(exc))+'\n')
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,ensure_ascii=False,indent=2))
        finally:registry.close()
        return
    if args.command=='cleromancy':
        import sys
        from .scrying import load_input
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:
                from .cleromancy import read,markdown
                result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                from html import escape
                print(json.dumps(dict(status='rejected',error=str(exc),cleromancy_report=None),indent=2) if args.format=='json' else '# Cleromancy request rejected\n\n'+escape(str(exc))+'\n')
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,ensure_ascii=False,indent=2))
        finally:registry.close()
        return
    if args.command=='bibliomancy':
        import sys
        from .scrying import load_input
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:
                from .bibliomancy import read,markdown
                result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                from html import escape
                print(json.dumps(dict(status='rejected',error=str(exc),bibliomancy_report=None),indent=2) if args.format=='json' else '# Bibliomancy request rejected\n\n'+escape(str(exc))+'\n')
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,ensure_ascii=False,indent=2))
        finally:registry.close()
        return
    if args.command=='osteomancy':
        import sys
        from .osteomancy import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='lithomancy':
        import sys
        from .lithomancy import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='geomancy':
        import sys
        from .geomancy import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='aeromancy':
        import sys
        from .aeromancy import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='hydromancy':
        import sys
        from .hydromancy import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='pyromancy':
        import sys
        from .pyromancy import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='coffee-reading':
        import sys
        from .coffee import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='tasseography':
        import sys
        from .tasseography import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='akashic-reference':
        import sys
        from .akashic import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='automatic-writing':
        import sys
        from .automatic_writing import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='dream':
        import sys
        from .dream import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='mirror-scrying':
        import sys
        from .mirror import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='scrying':
        import sys
        from .scrying import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='pendulum':
        import sys
        from .pendulum import load_input,read,markdown,rejection
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            try:result=read(load_input(args.input),registry)
            except (ValueError,OSError) as exc:
                print(rejection(exc,args.format))
                raise SystemExit(2)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='runes':
        import sys
        from .runes import load_input,read,markdown
        if hasattr(sys.stdout,'reconfigure'):sys.stdout.reconfigure(encoding='utf-8')
        registry=load_registry(args.database)
        try:
            result=read(load_input(args.input),registry)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='iching':
        from .iching import load_input,read,markdown
        registry=load_registry(args.database)
        try:
            result=read(load_input(args.input),registry)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='oracle':
        from .oracle import load_input,read,markdown
        registry=load_registry(args.database)
        try:
            result=read(load_input(args.input),registry)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='tarot':
        from .tarot import load_input,read,markdown
        registry=load_registry(args.database)
        try:
            result=read(load_input(args.input),registry)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='iridology-reference':
        from .iridology import load_input,reference,markdown
        registry=load_registry(args.database)
        try:
            result=reference(load_input(args.input),registry)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='aura-reference':
        from .aura import load_input,reference,markdown
        registry=load_registry(args.database)
        try:
            result=reference(load_input(args.input),registry)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='graphology-reference':
        from .graphology import load_input,reference,markdown
        registry=load_registry(args.database)
        try:
            result=reference(load_input(args.input),registry)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='podomancy-reference':
        from .podomancy import load_input,reference,markdown
        registry=load_registry(args.database)
        try:
            result=reference(load_input(args.input),registry)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='moleosophy-reference':
        from .moleosophy import load_input,reference,markdown
        registry=load_registry(args.database)
        try:
            result=reference(load_input(args.input),registry)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='phrenology-reference':
        from .phrenology import load_input,reference,markdown
        registry=load_registry(args.database)
        try:
            result=reference(load_input(args.input),registry)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='face-reference':
        from .face_reading import load_input,reference,markdown
        registry=load_registry(args.database)
        try:
            result=reference(load_input(args.input),registry)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='palmistry':
        from .palmistry import load_observations,read,markdown
        registry=load_registry(args.database)
        try:
            result=read(load_observations(args.observations),registry)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close()
        return
    if args.command=='astrocartography':
        from .natal import SkyfieldEphemeris
        from .astrocartography import generate,markdown,register_knowledge
        e=SkyfieldEphemeris(args.kernel)
        registry=load_registry(args.database)
        try:
            register_knowledge(registry)
            result=generate(e,args.local,args.zone,args.latitude,args.longitude,fold=args.fold,
                destinations=json.loads(args.destinations),query=args.query,
                bodies=args.bodies.split(',') if args.bodies else None,houses=args.houses,
                tolerance=args.tolerance,uncertainty_minutes=args.uncertainty_minutes,profile=args.profile)
            print(markdown(result) if args.format=='markdown' else json.dumps(result['geojson'] if args.format=='geojson' else result,indent=2))
        finally:registry.close();e.kernel.close()
        return
    if args.command in ('mundane-ingress','mundane-cycle'):
        from datetime import datetime
        from .natal import SkyfieldEphemeris
        from .mundane import ingresses,conjunctions,register_knowledge,markdown
        e=SkyfieldEphemeris(args.kernel);registry=load_registry(args.database)
        try:
            register_knowledge(registry)
            if args.command=='mundane-ingress':
                result=ingresses(e,args.year,args.zone,args.latitude,args.longitude,args.profile,args.historical_duration)
            else:result=conjunctions(e,datetime.fromisoformat(args.start),datetime.fromisoformat(args.end),args.zone,args.latitude,args.longitude,args.profile)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close();e.kernel.close()
        return
    if args.command=='horary':
        from .natal import SkyfieldEphemeris
        from .horary import assess,register_knowledge,markdown
        e=SkyfieldEphemeris(args.kernel);registry=load_registry(args.database)
        try:
            register_knowledge(registry)
            result=assess(e,args.question,args.category,args.local,args.zone,args.latitude,args.longitude,args.protocol,args.fold,args.profile)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close();e.kernel.close()
        return
    if args.command=='numerology':
        from .numerology import calculate,markdown,readings
        r=readings(calculate(args.birth,args.name,args.basis,args.target,args.y_roles))
        print(markdown(r) if args.format=='markdown' else json.dumps(r,indent=2))
        return
    if args.command=='bazi':
        from .natal import SkyfieldEphemeris
        from .chinese import chart,register_knowledge,markdown
        e=SkyfieldEphemeris(args.kernel);registry=load_registry(args.database)
        try:
            register_knowledge(registry)
            result=chart(e,args.local,args.zone,args.latitude,args.longitude,args.fold,args.profile)
            from .chinese_readings import enrich,markdown,register_knowledge as register_readings
            register_readings(registry)
            result=enrich(result)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2,ensure_ascii=True))
        finally:registry.close();e.kernel.close()
        return
    if args.command=='jyotish':
        from .natal import SkyfieldEphemeris
        from .vedic import d1,register_knowledge,markdown
        e=SkyfieldEphemeris(args.kernel);registry=load_registry(args.database)
        try:
            register_knowledge(registry)
            result=d1(e,args.local,args.zone,args.latitude,args.longitude,args.fold)
            from .vedic_timing import enrich
            from datetime import datetime
            result=enrich(result,datetime.fromisoformat(args.target) if args.target else None,args.year_key,args.d9)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close();e.kernel.close()
        return
    if args.command=='releasing':
        from datetime import datetime
        from .natal import SkyfieldEphemeris,Settings,chart
        from .releasing import from_natal,register_knowledge,markdown
        e=SkyfieldEphemeris(args.kernel);registry=load_registry(args.database)
        try:
            register_knowledge(registry)
            n=chart(e,args.local,args.zone,args.latitude,args.longitude,Settings(tradition='Hellenistic',houses=args.houses),args.fold)
            result=from_natal(e,n,datetime.fromisoformat(args.start),datetime.fromisoformat(args.end),args.lot,args.levels,args.profile)
            print(markdown(result) if args.format=='markdown' else json.dumps(result,indent=2))
        finally:registry.close();e.kernel.close()
        return
    if args.command=='election':
        from datetime import datetime
        from .natal import SkyfieldEphemeris
        from .elections import search,register_knowledge
        e=SkyfieldEphemeris(args.kernel);registry=load_registry(args.database)
        try:
            register_knowledge(registry)
            result=search(e,args.category,datetime.fromisoformat(args.start),datetime.fromisoformat(args.end),
                args.latitude,args.longitude,args.profile,args.tradition,args.houses,
                args.require.split(',') if args.require else None,args.min_minutes,args.utc_hours,
                [int(s) for s in args.ascendant_signs.split(',')] if args.ascendant_signs else None,args.angle_step)
            print(json.dumps(result,indent=2))
        finally:registry.close();e.kernel.close()
        return
    if args.command=='solar-return':
        from .natal import SkyfieldEphemeris,Settings,chart
        from .solar_returns import solar_return,register_knowledge,markdown
        e=SkyfieldEphemeris(args.kernel);registry=load_registry(args.database)
        try:
            register_knowledge(registry)
            from .core_readings import register_knowledge as register_core
            register_core(registry)
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
            try:
                register_knowledge(registry)
                from .core_readings import register_knowledge as register_core
                register_core(registry)
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
            from .core_readings import placements
            result['reading'] = placements(result,registry)
            if args.tradition in ('Hellenistic','medieval/traditional'):
                from .doctrines import analyze,register_knowledge as register_doctrines
                register_doctrines(registry)
                result['traditional_conditions'] = analyze(e,result)
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
