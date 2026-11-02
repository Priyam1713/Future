"""End-to-end public CLI acceptance; no new astronomy expected values generated here."""
from pathlib import Path
import json,subprocess,sys,os

ROOT=Path(__file__).resolve().parents[1]
B=['1990-07-15T14:30','Asia/Kolkata','28.6139','77.209']
T='2026-11-02T00:00:00+00:00';END='2026-12-02T00:00:00+00:00'

def run():
    results=[];env=dict(os.environ,PYTHONIOENCODING='utf-8')
    def check(label,args,verify,kind='json'):
        p=subprocess.run([sys.executable,'-m','future']+args,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',timeout=60)
        if p.returncode:raise AssertionError(f'{label}: {p.stderr}')
        r=json.loads(p.stdout) if kind=='json' else p.stdout
        if not verify(r):raise AssertionError(f'{label}: output contract failed')
        results.append({'case':label,'status':'passed'})
        return r
    check('calendar',['calendar','2000','1','1','12'],lambda r:r['result']['julian_date_ut1']==2451545.)
    check('retrieval',['search','UT1'],lambda r:bool(r))
    for tradition in ('modern psychological','Hellenistic','medieval/traditional'):
        r=check('natal '+tradition,['natal']+B+['--tradition',tradition],lambda r:len(r['house_cusps'])==12 and 'reading' in r)
        if tradition!='modern psychological':assert r['traditional_conditions']['sect']['type'] in ('day','night')
        else:
            Path('data/core-v1-natal-1990.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    check('natal annual context',['natal']+B+['--profections-date',T],lambda r:'annual_profection_context' in r)
    f=['forecast']+B+[T,'--days','1','--bodies','Moon']
    check('forecast JSON/profections',f+['--profections'],lambda r:bool(r['exact_events']) and 'annual_profection_context' in r)
    check('forecast Markdown',f+['--format','markdown'],lambda r:'Coverage gaps' in r,'markdown')
    for tradition in ('modern psychological','Hellenistic'):
        r=check('progressions '+tradition,['progressions']+B+[T,'--window-days','1','--tradition',tradition],lambda r:'reading' in r and 'Moon' in r['planets'])
        if tradition=='Hellenistic':assert r['reading']['coverage']=='unsupported' and r['interpretations']==[]
        else:Path('data/core-v1-progressions-1990.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    r=check('return JSON',['solar-return']+B+['2026'],lambda r:r['solar_residual_degrees']<1e-5 and bool(r['reading']['placements']))
    Path('data/core-v1-return-1990.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    text=check('return Markdown',['solar-return']+B+['2026','--format','markdown'],lambda r:'Return-to-natal' in r and 'house topics' in r,'markdown')
    Path('data/core-v1-return-1990.md').write_text(text,encoding='utf-8')
    check('return other house',['solar-return']+B+['2026','--houses','equal'],lambda r:r['reading']['coverage']=='unsupported')
    for tradition in ('Hellenistic','medieval/traditional'):
        check('doctrines '+tradition,['doctrines']+B+['--tradition',tradition],lambda r:len(r['conditions']['planets'])==7)
    check('profections',['profections']+B+[T],lambda r:r['annual_profection']['lord_of_year']=='Mars')
    for lot in ('Spirit','Fortune'):
        check('releasing '+lot,['releasing']+B+[T,END,'--lot',lot],lambda r:len(r['periods'])>0 and r['level_status']['3'].startswith('experimental'))
    check('releasing Markdown',['releasing']+B+[T,END,'--format','markdown'],lambda r:'Zodiacal Releasing' in r,'markdown')
    for category,profile in [('retain-received-money','ramesey-retain-money'),('rapid-use-received-money','ramesey-rapid-use-money')]:
        check('experimental election '+category,['election',category,T,'2026-11-02T03:00:00+00:00','28.6139','77.209','--profile',profile],
            lambda r:r['release_status']=='experimental' and r['eligible_windows']==[])
    for label,args in [('invalid natal zone gap',['natal','2024-03-10T02:30','America/New_York','40.7','-74']),
                       ('unsupported zodiac profile',['natal']+B+['--tradition','unknown'])]:
        p=subprocess.run([sys.executable,'-m','future']+args,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',timeout=60)
        if p.returncode==0:raise AssertionError(label+' unexpectedly accepted')
        results.append({'case':label,'status':'rejected as required'})
    report={'technique_id':1,'cases':results,'passed':len(results),'scope':'Public CLI contracts and explicit error behavior; independent numerical verification remains in the full test suite.'}
    Path('data/western-core-v1-smoke.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f"{len(results)} CLI smoke cases passed")
    return report

if __name__=='__main__':run()
