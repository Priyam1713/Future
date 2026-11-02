from pathlib import Path
import json,subprocess,sys

def run():
    base=[sys.executable,'-X','utf8','-m','future','numerology','1998-10-15','Thomas Cruise Mapother','2026-10-12','--basis','birth']
    results=[]
    for name,args,reject in [('JSON',base,False),('Markdown',base+['--format','markdown'],False),('current',base[:-1]+['current'],False),('Y missing',base[:7]+['Mary']+base[8:],True)]:
        p=subprocess.run(args,capture_output=True,text=True,encoding='utf-8');assert (p.returncode!=0)==reject,(name,p.stderr)
        results.append({'case':name,'passed':True})
        if name=='JSON':
            r=json.loads(p.stdout);assert r['life_path']['steps']==[16,7] and r['expression']['steps']==[31,4]
            Path('data/numerology-acceptance.json').write_text(p.stdout,encoding='utf-8')
        if name=='Markdown':Path('data/numerology-acceptance.md').write_text(p.stdout,encoding='utf-8')
    Path('data/numerology-smoke.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(len(results),'Numerology CLI cases passed')
if __name__=='__main__':run()
