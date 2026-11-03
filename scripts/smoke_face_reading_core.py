"""Public CLI acceptance and reproducible documentary examples; no photographs."""
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run():
    base=[sys.executable,'-X','utf8','-m','future','face-reference']
    source=Path('data/face-reference-observations.json')
    example=Path('data/face-reference-example-input.json')
    data=json.loads(source.read_text());results=[]
    def check(name,path,extra=(),reject=False,output=None):
        p=subprocess.run(base+[str(path)]+list(extra),capture_output=True,text=True,encoding='utf-8')
        assert (p.returncode!=0)==reject,(name,p.stderr)
        if not reject and '--format' not in extra:
            r=json.loads(p.stdout);assert r['technique_id']==9 and not r['inference_enabled'] and r['individual_assessment'] is None
            assert all(not row['association_applied_to_individual'] for row in r['regions'])
            if name=='manual JSON':assert len(r['regions'])==8 and not r['missing_regions'] and not r['observation_conflicts']
            if name=='source JSON':assert r['source_example']['figure_number']==2
            if name=='unknown mirroring':assert r['regions'][0]['canonical_subject_side']=='unknown'
            if name=='conflicting annotations':assert r['observation_conflicts']
            if name=='unsupported region':assert r['regions'][0]['coverage']=='unsupported_region'
        if output:Path('data',output).write_text(p.stdout,encoding='utf-8')
        results.append(dict(case=name,passed=True))
    check('manual JSON',source,output='face-reference-manual.json')
    check('manual Markdown',source,['--format','markdown'],output='face-reference-manual.md')
    check('source JSON',example,output='face-reference-schematic.json')
    check('source Markdown',example,['--format','markdown'],output='face-reference-schematic.md')
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp,'input.json')
        def case(name,value,reject=False):
            path.write_text(json.dumps(value));check(name,path,reject=reject)
        o=copy.deepcopy(data);o['orientation']=dict(view='frontal',side_frame='viewer',mirrored=True);case('mirrored',o)
        o=copy.deepcopy(data);o['orientation']=dict(view='frontal',side_frame='viewer',mirrored='unknown');o['observations']=[dict(region_id='eyes',side='left')];case('unknown mirroring',o)
        o=copy.deepcopy(data);o['observations']=[dict(region_id='nose',side='midline',visibility='unknown')];case('unknown observations',o)
        o=copy.deepcopy(data);o['observations']=[dict(region_id='nose',side='midline',geometry=dict(outline='convex')),dict(region_id='nose',side='midline',geometry=dict(outline='concave'))];case('conflicting annotations',o)
        o=copy.deepcopy(data);o['observations']=[dict(region_id='ear',side='left')];case('unsupported region',o)
        case('wrong profile',data|dict(profile='Yap'),True)
        case('personal inference',data|dict(task='personality'),True)
        o=json.loads(example.read_text());o['observations']=data['observations'];case('source override',o,True)
    Path('data/face-reference-smoke.json').write_text(json.dumps(results,indent=2)+'\n')
    print(len(results),'Face Reference CLI cases passed')

if __name__=='__main__':run()
