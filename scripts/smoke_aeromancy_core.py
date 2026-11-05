import copy,json,re,subprocess,sys,tempfile
from pathlib import Path
from future.aeromancy import PROFILE,read
def examples():
 f=json.loads(Path('tests/fixtures/aeromancy_reference_v1.json').read_text(encoding='utf-8'))
 def o(phenomenon='smoke',features=None,**kw):return dict(id='o1',phenomenon=phenomenon,features=copy.deepcopy(features or {}))|kw
 def q(row=None,region='unknown',**kw):return dict(schema_version=1,profile=PROFILE,task='atmospheric_lore_comparison',mode='manual',origin='hypothetical',region=region,observations=[row] if row else [])|kw
 hake=lambda axis:o('cloud',dict(cloud_appearance='hake_shaped',cloud_axis=axis))
 texas=copy.deepcopy(f['cases'][11][1]);missing=texas.copy();missing.pop('prior_wind_strength')
 return {'smoke-east':q(o(features=dict(smoke_drift_towards='east')),'scotland'),'smoke-west':q(o(features=dict(smoke_drift_towards='west')),'scotland'),
 'smoke-unknown':q(o(),'scotland'),'wind-not-smoke':q(o(features=dict(named_wind_direction='east',wind_direction_convention='from')),'scotland'),
 'hake-ew':q(hake('east_west'),'bedfordshire'),'hake-ns':q(hake('north_south'),'bedfordshire'),'hake-unknown':q(hake('unknown'),'bedfordshire'),
 'fleecy-full':q(o('cloud',f['cases'][6][1]),'scotland'),'fleecy-partial':q(o('cloud',dict(cloud_appearance='fleecy',cloud_motion='rapid')),'scotland'),
 'mackerel-mares':q(o('cloud',dict(mackerel_sky=True,mares_tails=True))),'mackerel-alone':q(o('cloud',dict(mackerel_sky=True,mares_tails=False))),
 'mackerel-competing':q(o('cloud',dict(mackerel_sky=True)),notes='Compare all five separately attributed accounts and horizons;no consensus outcome.'),
 'wing-south':q(o('wind',f['cases'][10][1])),'texas':q(o('wind',texas),'texas'),'texas-missing':q(o('wind',missing),'texas'),
 'region-mismatch':q(o(features=dict(smoke_drift_towards='east')),'texas'),'region-unknown':q(o(features=dict(smoke_drift_towards='east'))),
 'conflicting':q(o(features=dict(smoke_drift_towards=['east','west'])),'scotland'),
 'hypothetical':q(o(features=dict(smoke_drift_towards='east'),description='  Café Café\r\n猫 ☁\t ',association='```json\n personal  '),'scotland'),
 'reference-only':q(include_reference_catalog=True),'empty':q()}
def run():
 rows=examples();cases=[]
 with tempfile.TemporaryDirectory() as tmp:
  path=Path(tmp,'q.json')
  def check(name,q,fmt='json',reject=False,output=None):
   path.write_bytes(json.dumps(q,ensure_ascii=False).encode('utf-8'));p=subprocess.run([sys.executable,'-m','future','aeromancy',str(path),'--format',fmt],capture_output=True)
   assert p.returncode==(2 if reject else 0),(name,p.stderr)
   text=p.stdout.decode('utf-8').replace('\r\n','\n')
   if fmt=='markdown':text=text.rstrip('\n')+'\n'
   if reject:
    if fmt=='json':assert json.loads(text)['aeromancy_report'] is None
    else:assert 'request rejected' in text
   elif fmt=='json':assert json.loads(text)==read(q)
   else:
    m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert read(json.loads(m[2])['request'])==read(q)
   if output:Path('data',output).write_bytes(text.encode('utf-8'))
   cases.append(dict(case=name,passed=True,rejected=reject))
  for name,q in rows.items():
   Path('data',f'aeromancy-{name}-input.json').write_bytes((json.dumps(q,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
   check(name+' JSON',q,output=f'aeromancy-{name}.json');check(name+' Markdown',q,'markdown',output=f'aeromancy-{name}.md');check(name+' repeat JSON',q)
  invalid=copy.deepcopy(rows['texas']);invalid['observations'][0]['features']['light_wind_duration_days']=True
  bad=[('invalid duration',invalid),('wrong profile',rows['empty']|dict(profile='tyson-atmospheric')),('camera unsupported',rows['empty']|dict(mode='camera')),('seed unsupported',rows['empty']|dict(seed=1)),('geolocation unsupported',rows['empty']|dict(latitude=1)),('bad region',rows['empty']|dict(region='worldwide')),('bad timestamp',rows['empty']|dict(timestamp='now')),('bad catalog',rows['empty']|dict(include_reference_catalog=1))]
  for name,q in bad:check(name,q,reject=True,output='aeromancy-invalid.json' if name=='invalid duration' else None)
  check('invalid Markdown',invalid,'markdown',True,'aeromancy-invalid.md');Path('data/aeromancy-invalid-input.json').write_text(json.dumps(invalid,indent=2)+'\n',encoding='utf-8')
 Path('data/aeromancy-input.json').write_text(json.dumps(rows['smoke-east'],indent=2)+'\n',encoding='utf-8');Path('data/aeromancy-smoke.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
 for name,q in rows.items():
  assert json.loads(Path('data',f'aeromancy-{name}.json').read_text(encoding='utf-8'))==read(q)
  text=Path('data',f'aeromancy-{name}.md').read_text(encoding='utf-8');m=re.search(r'(`{3,})json\n(.*?)\n\1',text.split('## Exact replay metadata')[1],re.S);assert read(json.loads(m[2])['request'])==read(q)
 print(len(cases),'Aeromancy CLI cases passed;21 JSON/21 Markdown saved replays verified')
if __name__=='__main__':run()
