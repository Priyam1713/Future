"""Offline CLI lifecycle, actual packet exports and accepted/rejected exact replays."""
import copy
import json
from pathlib import Path
import re
import struct
import subprocess
import sys
import tempfile
import zlib
from future import remote_viewing as r
from tests.test_remote_viewing import KNOWN,fresh,step,recording,viewer_locked,judged,completed


def request(task,**values):return dict(schema_version=1,profile=r.PROFILE,task=task,**values)


def examples():
    valid=completed();before=judged();v=r.viewer_packet(step(fresh(),'commit'));j=r.judge_packet(viewer_locked(),'judge')
    human_path=Path('data/remote-viewing-human-manual-input.json')
    human=(json.loads(human_path.read_text(encoding='utf-8'))['trial'] if human_path.exists() else completed(fresh(origin='human',assignment_policy='manual')))
    # This is a manually recorded human-origin schema demonstration,not a fabricated human study.
    training=recording(fresh(mode='training_feedback'))
    training=step(training,'feedback',payload=dict(text='Documentary training feedback only;N means Near Site.',code='N'))
    training=step(training,'lock_viewer',payload=dict(digest=r.lock_digest(training,'viewer')))
    training=step(training,'start_judge');training=step(training,'rank',payload=dict(ranks=dict(zip(r.ALIASES,range(1,6))),report='Unblinded training demonstration;not eligible for blind scoring.'))
    training=step(training,'lock_judge',payload=dict(digest=r.lock_digest(training,'judge')));training=step(training,'reveal',payload=dict(preimage=r.preimage(training)))
    failed=step(fresh(),'reveal',payload=dict(preimage=r.preimage(fresh())));failed=completed(failed)
    reused=[completed(fresh(trial_ids=['trial001','trial002'],trial_id=i,reuse_policy='declare_dependence')) for i in ('trial001','trial002')]
    feedback=step(completed(),'feedback',payload=dict(code='C',text='After-reveal comparison note.'))
    # report is terminal reported;post-feedback is prohibited;use revealed state instead.
    feedback=copy.deepcopy(valid);feedback['events']=feedback['events'][:-1]
    feedback=step(feedback,'feedback',payload=dict(code='C',text='After-reveal comparison note,not the locked blind rank.'))
    accepted={
      'simulated':request('report',trial=valid),'human-manual':request('report',trial=human),
      **{f'rank{n}':request('report',trial=completed(target_rank=n)) for n in (1,3,5)},
      'multiple-judges':request('report',trial=completed(fresh(judges=['j1','j2']))),
      'training-feedback':request('report',trial=training),'reused-dependence':request('summary',trials=reused),
      'failure-retained':request('report',trial=failed),'viewer-packet':request('viewer_packet',trial=step(fresh(),'commit')),
      'judge-packet':request('judge_packet',trial=viewer_locked(),judge_id='judge'),
      'pre-reveal-status':request('report',trial=before),'summary':request('summary',trials=[valid]),
      'validate-viewer':request('validate_packet',packet=v),'validate-judge':request('validate_packet',packet=j),
      'unicode':request('report',trial=valid),'after-reveal-feedback':request('report',trial=feedback)}
    for status in r.TERMINAL:
        t=step(recording(),'terminate',payload=dict(status=status,reason='Explicitly recorded demonstration exception;retained in ledger.'))
        accepted[status]=request('summary',trials=[t])
    # Attachment source paths remain private;public derivative uses fresh neutral names.
    at=recording();at=step(at,'entry',payload=dict(text='Original sketch fixture',stage='III',attachments=[copy.deepcopy(at['plan']['pool']['candidates'][0])]))
    at=step(at,'lock_viewer',payload=dict(digest=r.lock_digest(at,'viewer')))
    accepted['attachment-packet']=request('judge_packet',trial=at,judge_id='judge')
    def apply_request(t,action,actor=None,payload=None,at=None):
        return request('apply',trial=t,action=action,actor=actor or t['plan']['tasker'],at=at or f'2026-11-06T09:{len(t["events"])+1:02d}:00+05:30',payload=payload or {})
    mutated=copy.deepcopy(valid);mutated['events'][2]['payload']['text']+='changed'
    judge_mut=copy.deepcopy(valid);judge_mut['events'][5]['payload']['ranks']=dict(zip(r.ALIASES,range(1,6)))
    wrong_pool=copy.deepcopy(valid);wrong_pool['plan']['pool']['id']='wrong'
    wrong_asset=copy.deepcopy(valid);wrong_asset['plan']['pool']['candidates'][0]['sha256']='0'*64
    aliases=copy.deepcopy(j);aliases['candidates'][1]['alias']='c1'
    leaked=copy.deepcopy(v);leaked['target_id']='planted-secret'
    no_rights=copy.deepcopy(KNOWN['plan']);no_rights['pool']['candidates'][0]['rights']['permission']=''
    conflicting=copy.deepcopy(KNOWN['plan']);conflicting['viewer']='tasker'
    badpolicy=copy.deepcopy(KNOWN['plan']);badpolicy['primary_endpoint']='posthoc-match'
    duplicate=copy.deepcopy(KNOWN['plan']);duplicate['pool']['candidates'][1]['id']='t1'
    rawpng=Path(KNOWN['plan']['pool']['candidates'][0]['path']).read_bytes();data=b'actual target label'
    planted=struct.pack('>I',len(data))+b'eXIf'+data+struct.pack('>I',zlib.crc32(b'eXIf'+data)&0xffffffff)
    exif=rawpng[:33]+planted+rawpng[33:]
    path=Path('data/remote-viewing-assets/rejected-exif.png');path.write_bytes(exif)
    exifplan=copy.deepcopy(KNOWN['plan']);exifplan['pool']['candidates'][0].update(path=path.as_posix(),sha256=r.bytes_hash(exif))
    ranking=step(viewer_locked(),'start_judge')
    wrongopening=r.preimage(before);wrongopening['nonce']='0'*64
    rejected={
      'premature-reveal':apply_request(step(fresh(),'commit'),'reveal',payload=dict(preimage=r.preimage(fresh()))),
      'transcript-mutation':request('report',trial=mutated),'judge-mutation':request('report',trial=judge_mut),
      'wrong-pool':request('report',trial=wrong_pool),'wrong-asset':request('report',trial=wrong_asset),
      'duplicate-alias':request('validate_packet',packet=aliases),'invalid-ranking':apply_request(ranking,'rank','judge',dict(ranks=dict(zip(r.ALIASES,[1,1,3,4,5])),report='')),
      'leaking-viewer':request('validate_packet',packet=leaked),'exif-metadata':request('create',plan=exifplan,seed=KNOWN['seed']),
      'no-rights':request('create',plan=no_rights,seed=KNOWN['seed']),
      'missing-timezone':apply_request(step(fresh(),'commit'),'start','viewer',at='2026-11-06T09:02:00'),
      'contradictory-chronology':apply_request(step(fresh(),'commit'),'start','viewer',at='2026-11-06T08:00:00+05:30'),
      'conflicting-roles':request('create',plan=conflicting,seed=KNOWN['seed']),
      'invalid-protocol':request('create',plan=badpolicy,seed=KNOWN['seed']),
      'duplicate-candidate':request('create',plan=duplicate,seed=KNOWN['seed']),
      'unauthorized-reveal':apply_request(before,'reveal','viewer',dict(preimage=r.preimage(before))),
      'wrong-opening':apply_request(before,'reveal',payload=dict(preimage=wrongopening)),
      'incomplete-ledger':request('summary',trials=[completed(fresh(trial_ids=['trial001','trial002']))]),
      'forbidden-inference':request('predict',trial=valid),
      'seeded-human':request('create',plan=copy.deepcopy(KNOWN['plan'])|dict(origin='human'),seed=KNOWN['seed']),
      'unlocked-judge-packet':request('judge_packet',trial=recording(),judge_id='judge')}
    return accepted,rejected


def run():
    accepted,rejected=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        inp=Path(tmp,'request.json')
        def cli(name,q,fmt='json',bad=False,save=None,extra=()):
            inp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            cp=subprocess.run([sys.executable,'-m','future','remote-viewing',str(inp),'--format',fmt,*extra],capture_output=True)
            assert cp.returncode==(2 if bad else 0),(name,cp.returncode,cp.stderr,cp.stdout[:200])
            out=cp.stdout.decode('utf-8').replace('\r\n','\n').rstrip('\n')+'\n'
            if fmt=='json':v=json.loads(out)
            else:
                match=re.search(r'(`{3,})json\n(.*?)\n\1',out,re.S);assert match,name;v=json.loads(match[2])
            try:expected=r.read(q)
            except ValueError:expected=dict(visibility='public_error',status='rejected',error='Remote Viewing request rejected',remote_viewing_report=None)
            assert v==expected,(name,'replay')
            if save:Path(save).write_bytes(out.encode('utf-8'))
            cases.append(dict(case=name,format=fmt,rejected=bad,passed=True));return v
        for bad,examples_ in [(False,accepted),(True,rejected)]:
            for name,q in examples_.items():
                Path(f'data/remote-viewing-{name}-input.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
                for fmt in ('json','markdown'):
                    cli(name,q,fmt,bad,save=f'data/remote-viewing-{name}.'+('json' if fmt=='json' else 'md'))
                if not bad:cli(name+' repeat',q)
        # Complete lifecycle through the actual command,not only report APIs.
        created=cli('lifecycle create',request('create',plan=copy.deepcopy(KNOWN['plan']),seed=KNOWN['seed']))
        t=created['trial']
        for event in KNOWN['reported_trial']['events']:
            q=request('apply',trial=t,action=event['action'],actor=event['actor'],at=event['at'],payload=event['payload'])
            t=cli('lifecycle '+event['action'],q)['trial']
        assert t==KNOWN['reported_trial']
        cli('lifecycle final report',request('report',trial=t))
        for name in ('viewer-packet','judge-packet','attachment-packet'):
            out=Path(tmp,name)
            packet=cli('export '+name,accepted[name],extra=('--export-dir',str(out)))
            assert json.loads((out/'packet.json').read_text(encoding='utf-8'))==packet
            names={x.name for x in out.iterdir()}
            allowed={'packet.json'}
            if packet['visibility']=='blind_judge':
                allowed|={a['name'] for a in packet['candidates']}
                allowed|={a['name'] for e in packet['transcript'] for a in e['attachments']}
            assert names==allowed
            for path in out.iterdir():
                assert KNOWN['nonce'].encode() not in path.read_bytes()
                assert KNOWN['seed'].encode() not in path.read_bytes()
    out=dict(passed=True,cli_cases=len(cases),accepted_pairs=len(accepted),rejected_pairs=len(rejected),full_cli_lifecycle=True,actual_directory_exports=3,exact_json_markdown_replay=True,cases=cases)
    Path('data/remote-viewing-smoke.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print(f'{len(cases)} Remote Viewing CLI cases passed;{len(accepted)} accepted/{len(rejected)} rejected JSON/Markdown pairs;3 exact blind directory exports')

if __name__=='__main__':run()
