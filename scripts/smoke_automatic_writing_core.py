import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from future.automatic_writing import PROFILE, read


def examples():
    def event(kind,i,**kwargs):return dict(id='e'+str(i),type=kind,**kwargs)
    def segment(text,i):return dict(id='s'+str(i),order=i,text=text,authorship='user')
    def request(events,state,**kwargs):return dict(schema_version=1,profile=PROFILE,task='guided_writing',mode='manual',session_id='sample',state=state,events=events,**kwargs)
    complete=request([event('begin',0,timestamp='2026-11-04T10:00:00Z'),event('append',1,segment=segment('The blue door opens.',1)),event('stop',2,timestamp='2026-11-04T10:02:00Z'),event('complete',3)],'completed',intention='A voluntary writing exercise.',review_policy='no_review')
    interrupted=request([event('begin',0),event('append',1,segment=segment('A window',1)),event('interruption',2,comment='I chose to stop here.'),event('restart',3,comment='Editorial restart; no arbitrary letter required.'),event('append',4,segment=segment(' opens.\n',2)),event('pause',5),event('resume',6),event('stop',7),event('complete',8)],'completed')
    revisions=copy.deepcopy(complete);revisions['review_policy']='required';revisions['events']=revisions['events'][:3]+[event('review',3),event('revise',4,revision=dict(id='r1',parent='first_draft',text='A blue door opens.',authorship='user',comment='Changed the article.')),event('revise',5,revision=dict(id='r2',parent='r1',text='A blue door opens slowly.',authorship='user')),event('complete',6)]
    unicode=request([event('begin',0),event('append',1,segment=segment(' A🐍\r\n',1)),event('append',2,segment=segment('Café\t猫 ',2)),event('stop',3)],'stopped',associations=['My own association.'],comments='  Preserved verbatim. ')
    partial=request([event('begin',0,timestamp='2026-11-04T10:00:00'),event('append',1,segment=segment('Unfinished',1)),event('stop',2,timestamp='2026-11-04T10:01:00Z')],'stopped')
    return {'complete':complete,'interrupted':interrupted,'revisions':revisions,'empty':request([],'prepared'),
            'unicode':unicode,'partial-timing':partial,'procedure':request([],'prepared',editorial_questions=False)}


def run():
    rows=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            p=subprocess.run([sys.executable,'-m','future','automatic-writing',str(path),'--format',fmt],capture_output=True)
            assert p.returncode==(2 if reject else 0),(name,p.stderr)
            text=p.stdout.decode('utf-8').replace('\r\n','\n')
            if reject:
                if fmt=='json':assert json.loads(text)['automatic_writing_report'] is None
                else:assert 'request rejected' in text
            elif fmt=='json':assert json.loads(text)==read(value)
            else:
                replay=json.loads(text.split('## Exact replay metadata')[1].split('```json\n')[1].split('\n```')[0])
                assert read(replay['request'])==read(value)
            if output:Path('data',output).write_text(text,encoding='utf-8')
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,value in rows.items():
            Path('data',f'automatic-writing-{name}-input.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',value,output=f'automatic-writing-{name}.json')
            check(name+' Markdown',value,'markdown',output=f'automatic-writing-{name}.md')
        bad_order=copy.deepcopy(rows['complete']);bad_order['events']=[bad_order['events'][1]]
        bad_parent=copy.deepcopy(rows['revisions']);bad_parent['events'][4]['revision']['parent']='missing'
        bad_unicode=copy.deepcopy(rows['complete']);bad_unicode['events'][1]['segment']['text']='\ud800'
        invalid=[('profile',rows['empty']|dict(profile='spirit')),('ordering',bad_order),('parent',bad_parent),
                 ('state mismatch',rows['empty']|dict(state='completed')),('unknown field',rows['empty']|dict(seed=1)),
                 ('generated mode',rows['empty']|dict(mode='llm')),('bad timestamp',rows['empty']|dict(start_time='now')),
                 ('bad Unicode',bad_unicode)]
        for name,value in invalid:check(name,value,reject=True)
        check('ordering Markdown rejection',bad_order,'markdown',True,output='automatic-writing-invalid.md')
        check('ordering JSON rejection',bad_order,reject=True,output='automatic-writing-invalid.json')
        Path('data/automatic-writing-invalid-input.json').write_text(json.dumps(bad_order,indent=2)+'\n',encoding='utf-8')
    Path('data/automatic-writing-input.json').write_text(json.dumps(rows['complete'],indent=2)+'\n',encoding='utf-8')
    Path('data/automatic-writing-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Automatic Writing CLI cases passed')


if __name__=='__main__':run()
