import copy
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from future.akashic import PROFILE, read


def examples():
    base=dict(schema_version=1,profile=PROFILE,task='reference_reflection',mode='manual')
    return {
        'concepts':base|dict(concept_ids=['records','pathway','opening','closing','roles','conscious','question_framing','scope_limits','describe','clinical_boundary']),
        'guided':base|dict(question=dict(text='What personal values would I like to consider?',purpose='personal_reflection',form='open'),background='Only what I choose to share.',focus='My own choices.',session=dict(id='reflection1',state='completed',stages=[dict(id='source_review',status='completed'),dict(id='preparation',status='skipped',comment='No prayer performed.'),dict(id='question',status='completed'),dict(id='notes',status='completed'),dict(id='finish',status='completed',comment='Finished the software exercise.'),dict(id='reflection',status='completed')]),notes=[dict(id='n1',text='I can name my present priorities.',uncertainty=False)]),
        'reframed':base|dict(question=dict(text='Will this choice guarantee success?',purpose='factual_prediction',form='yes_no'),reframe='open_reflection',unknowns=['Future outcome remains unknown.']),
        'creative':base|dict(question=dict(text='  A🐍 Café\r\n猫 ',purpose='creative_imagination'),notes=[dict(id='scene1',kind='imagined_scene',text='  A blue library\t\n',uncertainty=True,concept_ids=['records']),dict(id='association1',kind='association',text='My own association.')],session=dict(state='in_progress',stages=[dict(id='notes',status='completed')])),
        'unknown':base|dict(concept_ids=['past_life_identity','unknown'],question=dict(purpose='unknown'),notes=[dict(id='n1',kind='unanswered',text=None)]),
        'prediction':base|dict(question=dict(text='What exact date will the event occur?',purpose='factual_prediction',form='time_based')),
        'empty':base|dict(question=dict(text=''),session=dict(state='discontinued',stages=[]),notes=[],unknowns=['']),
        'comparison':base|dict(question=dict(purpose='historical_research'),comparisons=['steiner-zimmer1959','cayce-numbered-readings'],reframe='source_research'),
        'clinical':base|dict(question=dict(text='Give me a diagnosis from the records.',purpose='medical_clinical'),concept_ids=['clinical_boundary'])}


def run():
    rows=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            p=subprocess.run([sys.executable,'-m','future','akashic-reference',str(path),'--format',fmt],capture_output=True)
            assert p.returncode==(2 if reject else 0),(name,p.stderr)
            text=p.stdout.decode('utf-8').replace('\r\n','\n')
            if fmt=='markdown':text=text.rstrip('\n')+'\n'
            if reject:
                if fmt=='json':assert json.loads(text)['akashic_report'] is None
                else:assert 'request rejected' in text
            elif fmt=='json':assert json.loads(text)==read(value)
            else:
                m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S)
                assert read(json.loads(m[2])['request'])==read(value)
            if output:Path('data',output).write_bytes(text.encode('utf-8'))
            cases.append(dict(case=name,passed=True,rejected=reject))
        for name,value in rows.items():
            Path('data',f'akashic-{name}-input.json').write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            check(name+' JSON',value,output=f'akashic-{name}.json')
            check(name+' Markdown',value,'markdown',output=f'akashic-{name}.md')
        base={k:rows['concepts'][k] for k in ('schema_version','profile','task','mode')}
        ordering=base|dict(session=dict(stages=[dict(id='finish'),dict(id='question')]))
        invalid=[('wrong profile',base|dict(profile='Steiner')),('wrong mode',base|dict(mode='generated')),
            ('unknown purpose',base|dict(question=dict(purpose='psychic'))),('duplicate concepts',base|dict(concept_ids=['records']*2)),
            ('ordering',ordering),('missing finish',base|dict(session=dict(state='completed'))),
            ('bad uncertainty',base|dict(notes=[dict(id='n',uncertainty=1)])),
            ('invalid timestamp',base|dict(session=dict(timestamp='now'))),('seed unsupported',base|dict(seed=0))]
        for name,value in invalid:check(name,value,reject=True,output='akashic-invalid.json' if name=='ordering' else None)
        check('ordering Markdown rejection',ordering,'markdown',True,output='akashic-invalid.md')
        Path('data/akashic-invalid-input.json').write_text(json.dumps(ordering,indent=2)+'\n',encoding='utf-8')
    Path('data/akashic-input.json').write_text(json.dumps(rows['guided'],indent=2)+'\n',encoding='utf-8')
    Path('data/akashic-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Akashic CLI cases passed')


if __name__=='__main__':run()
