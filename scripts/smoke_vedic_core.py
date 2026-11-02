"""Public Vedic CLI acceptance and reproducible full report; no source text copied."""
from pathlib import Path
import subprocess,sys,os,json

ROOT=Path(__file__).resolve().parents[1]
B=['1990-07-15T14:30','Asia/Kolkata','28.6139','77.209']
T='2026-11-03T00:00:00+00:00'

def run():
    cases=[];env=dict(os.environ,PYTHONIOENCODING='utf-8')
    def invoke(name,args,kind='json',reject=False):
        p=subprocess.run([sys.executable,'-m','future','jyotish']+args,cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',timeout=60)
        if reject:
            assert p.returncode!=0,(name,p.stdout)
            cases.append({'case':name,'status':'rejected as required'});return
        assert p.returncode==0,(name,p.stderr)
        cases.append({'case':name,'status':'passed'})
        return json.loads(p.stdout) if kind=='json' else p.stdout
    r=invoke('D1/D9/Vimshottari savana JSON',B+['--d9','--target',T])
    assert r['technique_id']==2 and len(r['planets'])==len(r['d9']['planets'])==9
    assert r['ascendant']['sign']=='Libra' and r['moon_nakshatra']['name']=='Revati'
    assert r['vimshottari']['year_days']==360
    Path('data/vedic-core-1990.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
    md=invoke('D1/D9/Vimshottari Markdown',B+['--d9','--target',T,'--format','markdown'],'markdown')
    assert 'D9 / Navamsa' in md and 'Vimshottari' in md and 'https://vedicastrologer.org/articles/vedic_astro_textbook.pdf' in md
    Path('data/vedic-core-1990.md').write_text(md,encoding='utf-8')
    solar=invoke('Explicit solar year',B+['--target',T,'--year-key','solar-365.2425'])
    assert solar['vimshottari']['birth_balance']['end_exclusive_utc']!=r['vimshottari']['birth_balance']['end_exclusive_utc']
    plain=invoke('D1-only interface',B)
    assert 'd9' not in plain and 'vimshottari' not in plain
    h=invoke('Historical IANA D1',['1879-03-14T11:30','Europe/Berlin','48.4','10'])
    assert h['birth']['utc']=='1879-03-14T10:36:32+00:00'
    amb=['2024-11-03T01:30','America/New_York','40.7','-74']
    invoke('Unresolved DST fold',amb,reject=True)
    a=invoke('DST fold zero',amb+['--fold','0']);b=invoke('DST fold one',amb+['--fold','1'])
    assert a['birth']['utc']!=b['birth']['utc']
    invoke('DST gap',['2024-03-10T02:30','America/New_York','40.7','-74'],reject=True)
    invoke('Offset missing on dasha target',B+['--target','2026-11-03T00:00'],reject=True)
    invoke('Unsupported node request',B+['--nodes','true'],reject=True)
    invoke('Unsupported year request',B+['--target',T,'--year-key','unknown'],reject=True)
    report={'technique_id':2,'passed':len(cases),'cases':cases,'scope':'CLI contract and explicit rejection behavior; independent/published calculation fixtures are in tests/fixtures/.'}
    Path('data/vedic-core-smoke.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(f'{len(cases)} Vedic CLI cases passed')
    return report

if __name__=='__main__':run()
