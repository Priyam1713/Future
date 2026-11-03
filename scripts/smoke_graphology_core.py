import json
import subprocess
import sys
import tempfile
from pathlib import Path
from future.graphology import PROFILE


def run():
    base=dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='manual',script='latin',writing_direction='ltr',
        observations=[dict(feature=f,category=c) for f,c in [('baseline_direction','ascending'),('baseline_path','rectilinear'),('slant','inclined'),
            ('letter_size','large'),('shape','rounded'),('word_spacing','crowded'),('line_spacing','clear'),('connection','juxtaposed'),
            ('stroke_appearance','muddy_heavy'),('word_proportions','diminishing')]]+
            [dict(feature='regularity',category='regular',certainty='uncertain')],pressure_evidence='image_darkness',
        geometry=dict(coordinate_system='cartesian_y_up',units='mm',baseline=[[0,0],[4,3]],upstroke=[[0,0],[1,7]],
            spacing=dict(x_height=2,word_gap=6,letter_gap=1,line_gap=5),proportions=dict(x_height=2,ascender_height=4,descender_depth=1)))
    example=dict(schema_version=1,profile=PROFILE,task='historical_reference',mode='source_example',example_id='figure-18')
    for name,value in [('graphology-reference-input.json',base),('graphology-source-example-input.json',example)]:
        Path('data',name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
    cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def check(name,value,fmt='json',reject=False,output=None):
            path.write_text(json.dumps(value),encoding='utf-8')
            p=subprocess.run([sys.executable,'-X','utf8','-m','future','graphology-reference',str(path),'--format',fmt],capture_output=True,text=True,encoding='utf-8')
            assert (p.returncode!=0)==reject,(name,p.stderr)
            if not reject:
                if fmt=='json':
                    r=json.loads(p.stdout);assert r['technique_id']==13 and not r['inference_enabled'] and r['individual_assessment'] is None
                    if name=='manual JSON':assert len(r['observations'])==11 and not r['conflicts'] and r['geometry']['slant_from_baseline_normal']==45
                    if name=='conflict':assert r['conflicts'] and all(x['status']=='conflict' for x in r['observations'])
                    if name=='geometry only':assert not r['observations'] and r['geometry']['interpretation_applied'] is False
                    if name=='unsupported direction':assert all(x['status']=='unsupported_script_direction' for x in r['observations'])
                    if name=='pressure evidence':assert r['pressure']['status']=='unsupported'
                else:assert 'No personal-trait' in p.stdout
            if output:Path('data',output).write_text(p.stdout,encoding='utf-8')
            cases.append(dict(case=name,passed=True))
        check('manual JSON',base,output='graphology-reference.json')
        check('manual Markdown',base,'markdown',output='graphology-reference.md')
        check('source JSON',example,output='graphology-source-example.json')
        check('source Markdown',example,'markdown',output='graphology-source-example.md')
        check('unknown and ambiguous',base|dict(observations=[dict(feature='slant',category=['inclined','reversed']),dict(feature='shape')]))
        check('conflict',base|dict(observations=[dict(feature='slant',category='inclined'),dict(feature='slant',category='reversed')]))
        check('geometry only',base|dict(observations=[]))
        check('unsupported direction',base|dict(script='arabic',writing_direction='rtl'))
        check('pressure evidence',base|dict(pressure_evidence='physical_dynamic'))
        check('wrong edition',base|dict(profile='ABC-1929'),reject=True)
        check('personal inference',base|dict(task='employment'),reject=True)
        check('handwriting image',base|dict(image='sample.png'),reject=True)
        check('bad geometry',base|dict(geometry=dict(coordinate_system='cartesian_y_up',units='mm',baseline=[[0,0],[0,0]])),reject=True)
        check('source override',example|dict(observations=base['observations']),reject=True)
    Path('data/graphology-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(len(cases),'Graphology CLI cases passed')


if __name__=='__main__':run()
