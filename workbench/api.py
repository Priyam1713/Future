"""Local-only HTTP boundary. All computation/evaluation delegates to Future Lab."""
import copy, csv, io, json, os, threading, secrets
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, Response, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware
from future import lab
from future.lab.common import ROOT, REGISTRY_HASH, PROFILE_HASH, digest
from .store import Store, dumps, now, uid, LOCK
from .prospective import build, at, snapshot

PHASES=['Astrology & Celestial Prediction','Physical & Human-Based Divination','Mystical & Spiritual Divination','Nature, Objects & Ancient Practices','Psychic & Paranormal Prediction','Futuristic & Hypothetical Technologies']
def phase(i):return 1 if i<=7 else 2 if i<=15 else 3 if i<=27 else 4 if i<=40 else 5 if i<=48 else 6
def read(path):return json.loads(Path(path).read_text(encoding='utf-8'))
def strict(text):
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('Duplicate JSON key: '+k)
            out[k]=v
        return out
    return json.loads(text,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('Nonfinite JSON')))

def create_app(directory=None,clock=now):
    app=FastAPI(title='Future Workbench',docs_url=None,redoc_url=None,openapi_url=None)
    store=Store(directory);app.state.store=store
    app.add_middleware(TrustedHostMiddleware,allowed_hosts=['localhost','127.0.0.1','[::1]','testserver'])
    @app.middleware('http')
    async def boundary(request,call_next):
        origin=request.headers.get('origin')
        if request.headers.get('sec-fetch-site')=='cross-site' or (origin and origin not in [str(request.base_url).rstrip('/'),'http://127.0.0.1:5173','http://localhost:5173']):
            return JSONResponse({'error':'Foreign origin is not allowed'},403)
        if request.url.path.startswith('/api') and request.method in ['POST','PUT','PATCH','DELETE']:
            body=bytearray()
            async for chunk in request.stream():
                body.extend(chunk)
                if len(body)>8*1024*1024:return JSONResponse({'error':'Request exceeds 8 MiB'},413)
            request._body=bytes(body)
            if body:
                try:strict(body)
                except (ValueError,RecursionError,UnicodeError) as exc:return JSONResponse({'error':str(exc)},422)
        response=await call_next(request)
        response.headers['Cache-Control']='no-store'
        response.headers['X-Content-Type-Options']='nosniff'
        response.headers['Referrer-Policy']='no-referrer'
        response.headers['Content-Security-Policy']="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
        return response
    @app.exception_handler(ValueError)
    async def invalid(request,exc):return JSONResponse({'error':str(exc),'type':type(exc).__name__},422)
    @app.exception_handler(KeyError)
    async def missing(request,exc):return JSONResponse({'error':'Missing required field: '+str(exc)},422)
    @app.exception_handler(TypeError)
    async def incorrect(request,exc):return JSONResponse({'error':'Incorrect field type: '+str(exc)},422)
    def write(request,payload,fn):
        result=store.write(request.headers.get('idempotency-key'),dict(path=request.url.path,body=payload),fn)
        if 'record_id' in result:
            with store.connect() as db:return store.get(db,result['record_id'])
        return result
    def consent(db,case_id,mode,technique_id=None):
        c=store.get(db,case_id,'case');p=store.get(db,c['parent'],'participant')
        if mode not in p['scopes']:raise ValueError('Participant did not consent to this use scope')
        if technique_id and technique_id not in p['techniques']:raise ValueError('Technique is outside participant consent')
        return c
    @app.get('/api/registry')
    def catalogue():
        r=lab.registry();return dict(registry_sha256=REGISTRY_HASH,profile_sha256=PROFILE_HASH,phases=PHASES,excluded_ids=r['excluded_ids'],entries=[dict(e,phase=phase(e['technique_id'])) for e in r['entries']])
    @app.get('/api/techniques/{id}')
    def capability(id:int):
        e=lab.capability(id);return dict(capability=e,release=read(ROOT/e['core_record']),sample=read(ROOT/'data/future-lab-invocation-examples.json')['entries'][str(id)]['request'])
    def invoke(q):
        for a in q.get('arguments',[]):
            if a=='--kernel' or a.startswith('--kernel='):raise ValueError('Workbench uses the pinned local kernel; paths cannot be overridden')
        with LOCK:return lab.invoke(q)
    @app.post('/api/validate')
    def validate(q:dict):
        r=invoke(q);return dict(status='native_rejected' if r['native_error'] else 'native_completed',invocation=r,method='Native offline execution; may cost the same as a run')
    @app.post('/api/sessions')
    def run(q:dict,request:Request):
        def action(db):
            mode=q.get('mode','explore');case=q.get('case_id')
            if mode not in ['explore','blind']:raise ValueError('Unsupported session mode')
            if case:consent(db,case,mode,q['request']['technique_id'])
            if mode=='blind' and (not case or not q.get('hidden_answer')):raise ValueError('Blind testing requires a consented case and a separate hidden answer')
            alternatives=q.get('alternatives',[])
            if not isinstance(alternatives,list) or len(alternatives)>10 or any(not isinstance(a,str) or len(a)>4000 for a in alternatives):raise ValueError('Up to ten bounded textual alternatives allowed')
            alternatives=list(alternatives);secrets.SystemRandom().shuffle(alternatives)
            alternatives=[dict(label=chr(65+i),text=a) for i,a in enumerate(alternatives)]
            r=invoke(q['request']);v=store.new(db,'session',dict(mode=mode,request=q['request'],result=r,origin=q.get('origin','manual'),notes=q.get('notes',''),locked=None,revealed=False,feedback=[],alternatives=alternatives),case)
            if mode=='blind':db.execute('INSERT INTO secrets VALUES(?,?)',(v['id'],dumps(dict(answer=q['hidden_answer']))))
            return {'record_id':v['id']}
        return write(request,q,action)
    @app.get('/api/records')
    def records():
        with store.connect() as db:return store.rows(db)
    @app.post('/api/participants')
    def participant(q:dict,request:Request):
        def action(db):
            if q.get('consent') is not True or not q.get('scopes') or not set(q['scopes'])<=set(['explore','blind','prospective']):raise ValueError('Explicit consent and permitted scopes required')
            ids=q.get('techniques',[]);allowed={e['technique_id'] for e in lab.list_techniques()}
            if not ids or not set(ids)<=allowed:raise ValueError('Retained permitted technique IDs required')
            v=store.new(db,'participant',dict(nickname=str(q.get('nickname',''))[:120],pseudonym='P-'+uid()[:8],consent_at=clock(),scopes=q['scopes'],techniques=ids,retain_frozen=q.get('retain_frozen') is True))
            return {'record_id':v['id']}
        return write(request,q,action)
    @app.post('/api/cases')
    def case(q:dict,request:Request):
        def action(db):
            store.get(db,q['participant_id'],'participant')
            if not q.get('title'):raise ValueError('Case title required')
            v=store.new(db,'case',dict(title=q['title'],study=q.get('study',''),notes=q.get('notes','')),q['participant_id']);return {'record_id':v['id']}
        return write(request,q,action)
    @app.post('/api/sessions/{id}/{action}')
    def blind(id:str,action:str,q:dict,request:Request):
        def change(db):
            v=store.get(db,id,'session')
            if v['mode']!='blind':raise ValueError('Requires blind mode')
            if action=='lock':
                if v['locked'] or not q.get('interpretation'):raise ValueError('An immutable interpretation is required, once only')
                v['locked']=dict(at=clock(),interpretation=q['interpretation'],input_sha256=digest(v['request']),result_sha256=digest(v['result']),alternatives_sha256=digest(v['alternatives']))
                v['locked']['sha256']=digest(v['locked'])
            elif action=='reveal':
                if not v['locked']:raise ValueError('Lock interpretation before reveal')
                v['revealed']=True
                row=db.execute('SELECT body FROM secrets WHERE id=?',(id,)).fetchone()
                if row is None:raise ValueError('Unrevealed answer was not included in imported export; cannot reveal here')
                v['answer']=json.loads(row[0])['answer']
            elif action=='feedback':
                if not v['revealed'] or q.get('agreement') not in [1,2,3,4,5] or not q.get('assessor'):raise ValueError('Reveal first; assessor identity and agreement 1–5 required')
                v['feedback'].append(dict(at=clock(),assessor=q['assessor'],agreement=q['agreement'],notes=q.get('notes',''),meaning='Descriptive agreement, not predictive validity'))
            else:raise ValueError('Unsupported action')
            store.put(db,v);return {'record_id':id}
        return write(request,q,change)
    @app.post('/api/studies')
    def study(q:dict,request:Request):
        def action(db):
            case=q.get('case_id');stamp=clock();identity='study-'+uid()
            if case:consent(db,case,'prospective',q.get('plan',{}).get('technique_id',51))
            if 'plan' in q:
                p=copy.deepcopy(q['plan'])
                if p['mode']!='declared_prospective' or not at(stamp)<at(p['cutoff']):raise ValueError('Advanced plan requires a future cutoff and declared_prospective mode')
                p['created_at']=stamp;p['selection']['frozen_at']=stamp
                ledger=lab.forecast(lab.create(p),stamp)
            else:ledger=build(q,stamp,identity)
            v=store.new(db,'study',dict(ledger=ledger,report=lab.evaluate(ledger),dispositions=[],title=q.get('question',ledger['plan']['target_definition'])),case);return {'record_id':v['id']}
        return write(request,q,action)
    @app.post('/api/studies/{id}/outcome')
    def outcome(id:str,q:dict,request:Request):
        def action(db):
            v=store.get(db,id,'study');stamp=clock();target=next((x for x in v['ledger']['plan']['targets'] if x['id']==q.get('target_id')),None)
            if target is None:raise ValueError('Unknown target')
            status=q.get('status')
            if not q.get('reason') or not q.get('evidence'):raise ValueError('Independent outcome evidence and reason required')
            if status in ['void','disputed','correction']:
                v['dispositions'].append(dict(version=len(v['dispositions'])+1,target_id=target['id'],status=status,at=stamp,reason=q['reason'],evidence=q['evidence']))
                # Workbench annotations cannot rewrite a committed Lab outcome.
            else:
                e=dict(id='evidence-'+uid(),available_at=stamp,rights='self_authored',attribution=q.get('assessor','Independent local assessor declaration'),snapshot=q['evidence'],snapshot_sha256=snapshot(q['evidence']))
                o=dict(target_id=target['id'],event_id=target['event_id'],version=1,status=status,value=q.get('value') if status=='resolved' else None,known_at=q.get('known_at') if status=='resolved' else None,reason=q['reason'],evidence=e)
                v['ledger']=lab.resolve(v['ledger'],o,stamp);v['report']=lab.evaluate(v['ledger'])
            store.put(db,v);return {'record_id':id}
        return write(request,q,action)
    @app.post('/api/compare')
    def comparison(q:dict):
        with store.connect() as db:
            vs=[store.get(db,i) for i in q['ids']]
            if q.get('quantitative'):
                if any(v['kind']!='study' or v['dispositions'] for v in vs):raise ValueError('Only undisputed Lab studies admit quantitative comparison')
                return lab.compare([lab.evaluate(v['ledger']) for v in vs])
            return dict(mode='descriptive',records=vs,notice='Side-by-side inspection; no universal probability or accuracy score')
    @app.get('/api/dashboard')
    def dashboard(technique:int|None=None,participant:str|None=None,study:str|None=None,since:str|None=None,until:str|None=None):
        with store.connect() as db:
            rows=store.rows(db);cases=[v for v in rows if v['kind']=='case' and (not participant or v['parent']==participant) and (not study or v.get('study')==study)];caseids={v['id'] for v in cases}
            def selected(v):return (not participant and not study or v.get('parent') in caseids) and (not since or v['created_at']>=since) and (not until or v['created_at']<=until)
            sessions=[v for v in rows if v['kind']=='session' and selected(v) and (not technique or v['request']['technique_id']==technique)]
            studies=[v for v in rows if v['kind']=='study' and selected(v) and (not technique or v['ledger']['plan']['technique_id']==technique)]
            reports=[dict(record_id=v['id'],report=v['report'],dispositions=v['dispositions'],scoring_blocked=bool(v['dispositions'])) for v in studies]
            eligible=[v['report'] for v in studies if not v['dispositions']]
            return dict(cases=len(cases),sessions=len(sessions),sample_sessions=sum(v['origin']=='sample' for v in sessions),submitted_interpretations=sum(bool(v['locked']) for v in sessions),submitted_forecasts=sum(len(v['report']['cases']) for v in studies),pending=sum(c['outcome_status']=='unrecorded' for v in studies for c in v['report']['cases']),resolved=sum(c['outcome_status']=='resolved' for v in studies for c in v['report']['cases']),eligible_scored=sum(v['coverage']['matched'] for v in eligible),missing=sum(v['coverage']['missing_outcomes'] for v in eligible),abstentions=sum(v['coverage']['missing_forecasts'] for v in eligible),rejected=sum(bool(v['result']['native_error']) for v in sessions),sessions_by_technique={str(i):sum(v['request']['technique_id']==i for v in sessions) for i in sorted({v['request']['technique_id'] for v in sessions})},reports=reports,notice='Descriptive local records. Samples are not real observations. Scores/calibration/baselines remain per compatible Lab study. Dispositions suspend scoring.')
    @app.get('/api/export')
    def export(format:str='json',participant:str|None=None):
        with store.connect() as db:
            rows=store.rows(db)
            if participant:
                cs={v['id'] for v in rows if v.get('parent')==participant};rows=[v for v in rows if v['id']==participant or v.get('parent')==participant or v.get('parent') in cs]
            # Unrevealed secrets are deliberately absent from portable exports.
            body=dict(schema_version=1,registry_sha256=REGISTRY_HASH,profile_sha256=PROFILE_HASH,records=rows,blind_secrets_included=False)
            out=dict(payload=body,sha256=digest(body))
            if format=='json':return out
            if format=='csv':
                s=io.StringIO();w=csv.writer(s);w.writerow(['id','kind','created_at','parent','mode','technique_id'])
                for v in rows:w.writerow([v['id'],v['kind'],v['created_at'],v.get('parent'),v.get('mode'),v.get('request',{}).get('technique_id',v.get('ledger',{}).get('plan',{}).get('technique_id'))])
                return Response(s.getvalue(),media_type='text/csv',headers={'Content-Disposition':'attachment; filename=future-records.csv'})
            if format=='markdown':return Response('# Future Workbench export\n\nLocal descriptive records; no empirical skill certification.\n\n'+ '\n'.join('- '+v['kind']+' / '+v['id']+' / '+v['created_at'] for v in rows),media_type='text/markdown')
            raise ValueError('Unknown export format')
    @app.post('/api/import')
    def restore(q:dict,request:Request):
        def action(db):
            p=q['payload']
            if digest(p)!=q['sha256'] or p['schema_version']!=1 or p['registry_sha256']!=REGISTRY_HASH or p['profile_sha256']!=PROFILE_HASH:raise ValueError('Export integrity or version mismatch')
            existing={v['id']:v for v in store.rows(db)};ids=set();allowed=['participant','case','session','study','archive']
            for v in p['records']:
                if v['id'] in ids or v['kind'] not in allowed:raise ValueError('Duplicate ID or unsupported record kind')
                ids.add(v['id'])
                if v['id'] in existing and existing[v['id']]!=v:raise ValueError('Conflicting record ID')
                if v['kind']=='study':
                    lab.replay(v['ledger'])
                    if lab.evaluate(v['ledger'])!=v['report']:raise ValueError('Stored research report mismatch')
                if v['kind']=='session':
                    if digest(v['request'])!=v['result']['request_sha256']:raise ValueError('Session input commitment mismatch')
                    r=v['result'];h=r.get('invocation_sha256')
                    if digest({k:x for k,x in r.items() if k!='invocation_sha256'})!=h:raise ValueError('Invocation commitment mismatch')
                    if v.get('locked'):
                        l=v['locked']
                        if l['input_sha256']!=digest(v['request']) or l['result_sha256']!=digest(r) or digest({k:x for k,x in l.items() if k!='sha256'})!=l['sha256']:raise ValueError('Blind lock integrity mismatch')
            for v in p['records']:
                if v.get('parent') and v['parent'] not in ids|existing.keys():raise ValueError('Missing parent record')
                if v['id'] not in existing:store.put(db,v)
            return dict(imported=len(ids-existing.keys()),notice='Unrevealed blind answers are not exported or restored; imported records are not authenticated external evidence.')
        return write(request,q,action)
    @app.get('/api/records/{id}/deletion')
    def deletion(id:str):
        with store.connect() as db:
            v=store.get(db,id);cs={x['id'] for x in store.rows(db) if x.get('parent')==id};affected=[x for x in store.rows(db) if x['id']==id or x.get('parent')==id or x.get('parent') in cs]
            return dict(records=len(affected),separately_consented_frozen_retention=v.get('retain_frozen',False),notice='Deletes local active records and secrets. Previously downloaded exports and backups must be deleted separately. Frozen retention applies only when separately consented.')
    @app.delete('/api/records/{id}')
    def delete(id:str,request:Request):
        def action(db):
            v=store.get(db,id)
            if v['kind'] not in ['participant','case']:raise ValueError('Delete the owning case or participant')
            rows=store.rows(db);cs={x['id'] for x in rows if x.get('parent')==id};affected=[x for x in rows if x['id']==id or x.get('parent')==id or x.get('parent') in cs]
            owner=v if v['kind']=='participant' else store.get(db,v['parent'],'participant');retained=0
            for x in affected:
                if owner['retain_frozen'] and (x['kind']=='study' or x['kind']=='session' and x.get('locked')):
                    store.new(db,'archive',dict(consented_at=owner['consent_at'],frozen_record=x,notice='Retained by separate consent; may contain original sensitive inputs'));retained+=1
                db.execute('DELETE FROM records WHERE id=?',(x['id'],))
            # No response-body caches of deleted records exist. Clear stale idempotency pointers.
            db.execute('DELETE FROM receipts')
            return dict(deleted=len(affected),retained_frozen=retained)
        return write(request,{},action)
    web=Path(__file__).parent/'web/dist'
    if web.exists():
        app.mount('/assets',StaticFiles(directory=web/'assets'),name='assets')
        @app.get('/{path:path}')
        def spa(path:str):return FileResponse(web/'index.html')
    return app
