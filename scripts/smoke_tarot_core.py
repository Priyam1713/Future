import json
from pathlib import Path
import subprocess
import sys
import tempfile
from future.tarot_catalog import PROFILE,ORDER
from future.card_random import PROTOCOL


def run():
    base=dict(schema_version=1,profile=PROFILE,task='symbolic_reading',mode='seeded',spread='three',
        seed='Future-Tarot-v1',protocol=PROTOCOL,orientation_policy='seeded_reversals',question='What symbolic themes could help me reflect on a creative project?')
    one=base|dict(spread='one')
    celtic=base|dict(spread='waite_celtic',significator=dict(card_id='major-11',facing='left',basis='matter'))
    manual={k:v for k,v in base.items() if k not in ('seed','protocol')}|dict(mode='manual',spread='one',orientation_policy='explicit',cards=[dict(card_id='wands-four',orientation='reversed')])
    for name,value in [('tarot-one-input.json',one),('tarot-three-input.json',base),('tarot-celtic-input.json',celtic),('tarot-manual-input.json',manual)]:
        Path('data',name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            p=subprocess.run([sys.executable,'-X','utf8','-m','future','tarot',str(path),'--format',fmt],capture_output=True,text=True,encoding='utf-8')
            assert (p.returncode!=0)==reject,(name,p.stderr)
            if not reject:
                if fmt=='json':
                    r=json.loads(p.stdout);assert r['technique_id']==16 and not r['factual_prediction']
                    assert len({c['card']['id'] for c in r['readings']})==len(r['readings'])
                    assert all(c['direct_component']['locator'] and c['composition']['coverage']=='compositional' for c in r['readings'])
                    if name=='Celtic JSON':assert len(r['readings'])==10 and r['significator']['card']['id'] not in [c['card']['id'] for c in r['readings']]
                    if name=='manual JSON':assert 'unaltered' in r['readings'][0]['direct_component']['text']
                    if name=='upright only':assert all(c['orientation']=='upright' for c in r['readings'])
                    if name=='custom positions':assert [c['position']['label'] for c in r['readings']]==['Situation','Challenge','Reflection']
                else:assert 'no certain prediction or diagnosis' in p.stdout
            if output:Path('data',output).write_text(p.stdout,encoding='utf-8')
            cases.append(dict(case=name,passed=True))
        for title,value,prefix in [('one',one,'tarot-one'),('three',base,'tarot-three'),('Celtic',celtic,'tarot-celtic'),('manual',manual,'tarot-manual')]:
            check(title+' JSON',value,output=prefix+'.json')
            check(title+' Markdown',value,'markdown',output=prefix+'.md')
        check('upright only',base|dict(orientation_policy='upright_only'))
        check('custom positions',base|dict(positions=['Situation','Challenge','Reflection']))
        cm={k:v for k,v in celtic.items() if k not in ('seed','protocol')}|dict(mode='manual',orientation_policy='upright_only',
            cards=[dict(card_id=k) for k in list(ORDER)[:10]])
        check('manual Celtic',cm)
        check('right facing',celtic|dict(significator=celtic['significator']|dict(facing='right')))
        check('unknown card',manual|dict(cards=[dict(card_id='Thoth_Lust',orientation='upright')]),reject=True)
        check('duplicate cards',cm|dict(cards=[dict(card_id='major-00')]*10),reject=True)
        check('significator repeated',cm|dict(cards=[dict(card_id=k) for k in list(ORDER)[2:12]]),reject=True)
        check('unknown protocol',base|dict(protocol='future-cards-v2'),reject=True)
        check('missing seed',{k:v for k,v in base.items() if k!='seed'},reject=True)
        check('unknown tradition',base|dict(profile='Thoth'),reject=True)
        check('missing significator',{k:v for k,v in celtic.items() if k!='significator'},reject=True)
        check('mixed draw',base|dict(cards=manual['cards']),reject=True)
        check('diagnosis',base|dict(task='diagnosis'),reject=True)
        check('photo assessment',base|dict(photo='person.jpg'),reject=True)
    Path('data/tarot-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Tarot CLI cases passed')


if __name__=='__main__':run()
