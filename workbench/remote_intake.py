"""User-declared training record reconstruction; never prospective certification."""
import base64,io,struct,zlib,hashlib
from pathlib import Path
from PIL import Image,ImageOps
from future import remote_viewing as rv

ACTIONS=['commit','start','entry','lock_viewer','start_judge','rank','lock_judge','reveal','report']

def build(a):
    if a['permission']!='yes':raise ValueError('Permission to retain all five target images is required')
    if not isinstance(a['images'],list) or len(a['images'])!=5:raise ValueError('Upload exactly five distinct target images')
    candidates=[]
    directory=rv.ROOT/'tmp/workbench-targets';directory.mkdir(parents=True,exist_ok=True)
    for i,encoded in enumerate(a['images'],1):
        raw=base64.b64decode(encoded.split(',')[-1],validate=True)
        if len(raw)>1000000:raise ValueError('Each target image must be under 1 MB')
        with Image.open(io.BytesIO(raw)) as image:
            if image.width*image.height>24000000:raise ValueError('Target image exceeds 24 megapixels')
            normalized=ImageOps.fit(ImageOps.exif_transpose(image).convert('RGB'),(256,256))
            pixels=normalized.tobytes()
        def chunk(kind,data):return struct.pack('>I',len(data))+kind+data+struct.pack('>I',zlib.crc32(kind+data)&0xffffffff)
        png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',256,256,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(b''.join(b'\0'+pixels[y*768:(y+1)*768] for y in range(256))))+chunk(b'IEND',b'')
        sha=hashlib.sha256(png).hexdigest();path=directory/(sha+'.png');path.write_bytes(png)
        candidates.append(dict(id='target'+str(i),path=path.relative_to(rv.ROOT).as_posix(),sha256=sha,provenance=a['source'],rights=dict(basis='permission',holder=a['holder'],permission='User declares permission for local retained target processing',attribution=a['source'])))
    plan=dict(schema_version=1,profile=rv.PROFILE,profile_sha256=rv.PROFILE_HASH,experiment_id=a['study'],trial_ids=[a['trial']],trial_id=a['trial'],origin='human',mode='training_feedback',tasker=a['tasker'],viewer=a['viewer'],monitor=None,judges=[a['judge']],knowledge=dict(tasker='aware',viewer='aware',monitor='absent',judges='aware'),separation='shared_filesystem',assignment_policy='manual',presentation_order=list(range(5)),primary_endpoint='actual_target_rank',tie_policy='reject',stopping_rule='fixed_trial_ids',exclusion_rule='retain_all_attempts',reuse_policy='declare_dependence',created_at=a['created'],pool=dict(id=a['trial']+'-pool',version=1,candidates=candidates))
    trial=rv.create(plan,target_id='target'+a['target'])
    ranks={f'c{i}':int(a['rank'+str(i)]) for i in range(1,6)}
    for action in ACTIONS:
        actor=a['viewer'] if action in ('start','entry','lock_viewer') else a['judge'] if action=='rank' else a['tasker']
        payload=dict(text=a['transcript'],stage=None,attachments=[]) if action=='entry' else dict(ranks=ranks,report=a['report']) if action=='rank' else dict(digest=rv.lock_digest(trial,'viewer' if action=='lock_viewer' else 'judge')) if action in ('lock_viewer','lock_judge') else dict(preimage=rv.preimage(trial)) if action=='reveal' else {}
        trial=rv.apply(trial,action,actor,a[action+'_at'],payload)
        if not trial['events'][-1]['accepted']:raise ValueError(trial['events'][-1]['error'])
    return dict(technique_id=43,operation='remote-viewing',input=dict(schema_version=1,profile=rv.PROFILE,task='report',trial=trial))
