"""Reproducible CLI checks; example time is illustrative, not a historical question."""
import json,subprocess,sys
from pathlib import Path

def run():
    base=[sys.executable,'-X','utf8','-m','future','horary',
          'Was this advice given with honest intent?','advice-intent',
          '2026-11-03T12:00:00','Asia/Kolkata','28.6139','77.209','--protocol','advice-begins']
    cases=[('JSON',base,False),('Markdown',base+['--format','markdown'],False),
           ('unsupported',base[:7]+['relationship']+base[8:],False),
           ('wrong tradition',base+['--profile','Frawley'],True),
           ('protocol required',base[:-2],True)]
    results=[]
    for name,args,reject in cases:
        p=subprocess.run(args,capture_output=True,text=True,encoding='utf-8')
        assert (p.returncode!=0)==reject,(name,p.stderr)
        if name=='JSON':
            r=json.loads(p.stdout)
            assert r['classification']=='indeterminate' and 'gate.seventh_full' in r['unknown_rules']
            assert r['technique_id']==5 and r['question_chart']['settings']['houses']=='regiomontanus'
            Path('data/horary-advice-2026.json').write_text(p.stdout,encoding='utf-8')
        elif name=='Markdown':Path('data/horary-advice-2026.md').write_text(p.stdout,encoding='utf-8')
        elif name=='unsupported':assert json.loads(p.stdout)['classification']=='unsupported_question'
        results.append({'case':name,'passed':True})
    Path('data/horary-smoke.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(len(results),'Horary CLI cases passed')
if __name__=='__main__':run()
