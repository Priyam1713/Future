import copy,json,re,subprocess,sys,tempfile
from pathlib import Path
from future.hydromancy import PROFILE,read
def examples():
 w=dict(medium='water',container='dark_bowl',rainwater=True,gaze='soft')
 def o(category='perceived_fogginess',basis='subjective',**kw):return dict(id='o1',sequence=1,category=category,basis=basis)|kw
 def q(rows=None,session=None,**kw):return dict(schema_version=1,profile=PROFILE,task='water_observation_reference',mode='manual',origin='hypothetical',session=copy.deepcopy(w if session is None else session),observations=rows or [])|kw
 return {'water-bowl':q(session=w|dict(observer_undisturbed=True,surface_visible=True,relaxed=True)),
 'rain-pool':q(session=w|dict(container='natural_pool',surface_motion='ripples')),'soft-gaze':q(),'intense-gaze':q(session=w|dict(gaze='intense')),'unknown-gaze':q(session={k:v for k,v in w.items() if k!='gaze'}),
 'fog':q([o()]),'mist':q([o('physical_mist','physical')]),'glare':q([o('glare','physical')]),'ripples':q([o('physical_ripples','physical')],session=w|dict(surface_motion='ripples')),
 'oil-water':q([o('oil_layer','physical')],session=w|dict(medium='oil_on_water')),'imagined':q([o('imagined_image','imagined',description='  Café Café\r\n猫 🌊\t ',association='```json\n personal  ')]),
 'no-imagery':q([o('no_imagery','unknown')]),'conflicting':q([o(basis='physical',alternatives=['physical_mist'])]),'unknown-medium':q([o()],session=w|dict(medium='unknown')),
 'discontinued':q([o()],session=w|dict(status='discontinued')),'coptic':q(documentary_comparison=True),'unsupported':q([o('oil_drops','physical',drop_count=3,color='blue')]),'empty':q(session={})}
def run():
 rows=examples();cases=[]
 with tempfile.TemporaryDirectory() as tmp:
  path=Path(tmp,'q.json')
  def check(name,q,fmt='json',reject=False,output=None):
   path.write_bytes(json.dumps(q,ensure_ascii=False).encode('utf-8'));p=subprocess.run([sys.executable,'-m','future','hydromancy',str(path),'--format',fmt],capture_output=True)
   assert p.returncode==(2 if reject else 0),(name,p.stderr)
   text=p.stdout.decode('utf-8').replace('\r\n','\n')
   if fmt=='markdown':text=text.rstrip('\n')+'\n'
   if reject:
    if fmt=='json':assert json.loads(text)['hydromancy_report'] is None
    else:assert 'request rejected' in text
   elif fmt=='json':assert json.loads(text)==read(q)
   else:
    m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert read(json.loads(m[2])['request'])==read(q)
   if output:Path('data',output).write_bytes(text.encode('utf-8'))
   cases.append(dict(case=name,passed=True,rejected=reject))
  for name,q in rows.items():
   Path('data',f'hydromancy-{name}-input.json').write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
   check(name+' JSON',q,output=f'hydromancy-{name}.json');check(name+' Markdown',q,'markdown',output=f'hydromancy-{name}.md');check(name+' repeat JSON',q)
  invalid=copy.deepcopy(rows['fog']);invalid['observations'][0]['sequence']=True
  bad=[('invalid sequence',invalid),('old profile',rows['empty']|dict(profile='atkinson-pg43954-guided-journal-v1')),('image mode',rows['empty']|dict(mode='photo')),('seed unsupported',rows['empty']|dict(seed=1)),('sensor unsupported',rows['empty']|dict(temperature=5)),('bad comparison',rows['empty']|dict(documentary_comparison='perform_rite')),('bad medium',rows['empty']|dict(session=dict(medium='tea'))),('bad notes',rows['empty']|dict(notes='\x00'))]
  for name,q in bad:check(name,q,reject=True,output='hydromancy-invalid.json' if name=='invalid sequence' else None)
  check('invalid Markdown',invalid,'markdown',True,'hydromancy-invalid.md');Path('data/hydromancy-invalid-input.json').write_text(json.dumps(invalid,indent=2)+'\n',encoding='utf-8')
 Path('data/hydromancy-input.json').write_text(json.dumps(rows['water-bowl'],indent=2)+'\n',encoding='utf-8');Path('data/hydromancy-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
 for name,q in rows.items():
  assert json.loads(Path('data',f'hydromancy-{name}.json').read_text(encoding='utf-8'))==read(q)
  text=Path('data',f'hydromancy-{name}.md').read_text(encoding='utf-8');m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert read(json.loads(m[2])['request'])==read(q)
 print(len(cases),'Hydromancy CLI cases passed;18 JSON/18 Markdown saved replays verified')
if __name__=='__main__':run()
