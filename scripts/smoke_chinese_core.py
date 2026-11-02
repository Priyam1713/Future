"""Public BaZi CLI acceptance and reproducible source-grounded examples."""
from pathlib import Path
import json,subprocess,sys,os

ROOT=Path(__file__).resolve().parents[1]
B=['1990-07-15T14:30','Asia/Kolkata','28.6139','77.209']

def run():
    cases=[];env=dict(os.environ,PYTHONIOENCODING='utf-8')
    def invoke(name,args,kind='json',reject=False):
        p=subprocess.run([sys.executable,'-m','future','bazi']+args,cwd=ROOT,env=env,
            capture_output=True,text=True,encoding='utf-8',timeout=60)
        if reject:
            assert p.returncode!=0,(name,p.stdout)
            cases.append({'case':name,'status':'rejected as required'});return
        assert p.returncode==0,(name,p.stderr)
        cases.append({'case':name,'status':'passed'})
        return json.loads(p.stdout) if kind=='json' else p.stdout
    full=invoke('Delhi full JSON',B)
    assert [p['pair'] for p in full['pillars'].values()]==['庚午','癸未','辛巳','乙未']
    assert full['day_master']['name']=='Xin' and full['reading']['coverage']['compositional']
    Path('data/bazi-core-1990.json').write_text(json.dumps(full,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    md=invoke('Delhi readable report',B+['--format','markdown'],'markdown')
    assert 'Ten God' in md and 'compositional' in md and 'Luck-pillar onset remains unsupported' in md
    Path('data/bazi-core-1990.md').write_text(md,encoding='utf-8')
    published=invoke('Published1918 Shanghai-settings example',['1918-12-01T12:30','Asia/Shanghai','0','120'])
    assert [p['pair'] for p in published['pillars'].values()]==['戊午','癸亥','壬午','丙午']
    Path('data/bazi-published-1918.json').write_text(json.dumps(published,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    early=['1988-02-15T23:30','Asia/Shanghai','31.2','121.5']
    whole=invoke('Whole Zi',early);split=invoke('Split Zi',early+['--profile','civil-split-zi'])
    assert whole['pillars']['day']['pair']=='辛丑' and split['pillars']['day']['pair']=='庚子'
    assert whole['pillars']['hour']==split['pillars']['hour'] or whole['pillars']['hour']['pair']==split['pillars']['hour']['pair']
    standard=invoke('Explicit standard time',['2000-02-29T23:30','Australia/Sydney','-33.9','151.2','--profile','standard-zi23'])
    assert standard['clock']['effective'].endswith('22:30:00')
    separate=invoke('Solar year versus festival animal',['2026-02-10T12:00','Asia/Hong_Kong','22.3','114.2'])
    assert separate['pillars']['year']['branch']['animal']=='Horse' and separate['lunar_year_animal']['animal']=='Snake'
    amb=['2026-11-01T01:30','America/New_York','40.7','-74']
    invoke('Unresolved DST fold',amb,reject=True)
    a=invoke('DST fold0',amb+['--fold','0']);b=invoke('DST fold1',amb+['--fold','1'])
    assert a['birth']['utc']!=b['birth']['utc']
    invoke('DST gap',['2026-03-08T02:30','America/New_York','40.7','-74'],reject=True)
    invoke('Unsupported solar clock',B+['--profile','local-apparent'],reject=True)
    invoke('Unsupported luck request',B+['--luck-pillars'],reject=True)
    invoke('Unsupported ancient domain',['1800-01-01T12:00','UTC','0','0'],reject=True)
    invoke('Invalid location',['1990-07-15T14:30','UTC','91','0'],reject=True)
    result={'technique_id':3,'passed':len(cases),'cases':cases,
        'scope':'Public CLI contracts/rejections; calculation independence and published facts separately checked in regression fixtures.'}
    Path('data/chinese-core-smoke.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(f'{len(cases)} Chinese CLI cases passed')
    return result

if __name__=='__main__':run()
