"""Deterministic, engine-specific personal-input builders."""
from future import face_reading, phrenology, moleosophy, podomancy, graphology, aura, iridology, oracle, iching, runes, pendulum, scrying, mirror, dream, automatic_writing, akashic, tasseography, coffee, pyromancy, hydromancy, aeromancy, geomancy, lithomancy, osteomancy, bibliomancy, cleromancy, augury, haruspicy, feng_shui, intuitive_prediction, deja_reve, quantum_probability_forecasting as quantum, psychohistory, digital_twin
import secrets, csv, io, hashlib
from fractions import Fraction
from . import remote_intake, dream_intake

def select(key,label,choices,default='unknown'):
    return dict(key=key,label=label,type='select',choices=choices,default=default)

def text(key,label,required=True):
    return dict(key=key,label=label,type='text',default='',required=required)

def contract(technique):
    if technique==53:
        return dict(title='Replay your scalar digital-twin measurements',description='Enter scalar model parameters as integers or fractions. Measurement rows: UTC timestamp, value (blank if missing), control, availability timestamp (blank if missing). Times use YYYY-MM-DDTHH:MM:SSZ and a contiguous grid. Archival mode requires independent review declarations.',fields=[select('mode','Data mode',['synthetic','archival'],'archival')]+[text(k,label) for k,label in [('asset','Asset ID'),('state_unit','State unit ID'),('measurement_unit','Measurement unit ID'),('version','Parameter version ID'),('A','State transition A'),('B','Control coefficient B'),('H','Measurement coefficient H'),('Q','Process variance Q'),('R','Measurement variance R'),('m0','Initial state mean'),('P0','Initial state variance'),('initial','Initial UTC time'),('step','Step length in seconds'),('evaluation','Evaluation cutoff UTC time'),('records','Measurement rows'),('snapshot','Data source and snapshot description'),('attribution','Attribution')]]+[text('controls','Future scenario controls, comma separated (optional)',False),select('rights','Data rights',['self_authored','permission_granted','public_domain','cc_by'],'self_authored')]+[select('checked_'+k,'Independently reviewed '+k,['yes','no'],'no') for k in digital_twin.DATA['schema']['archive_checks']])
    if technique==52:
        return dict(title='Simulate a hypothetical threshold network',description='Enter one node and activation threshold per row (node, fraction such as 1/2), and undirected edge rows (node, node). This is a synthetic scenario simulation, not a calibrated social forecast.',fields=[text('nodes','Node and threshold rows'),text('edges','Edge rows',False),text('active','Initially active node IDs, comma separated',False),text('rounds','Maximum rounds (0 to number of nodes)'),text('snapshot','Describe your synthetic scenario'),text('attribution','Scenario attribution'),select('synthetic','Confirm these inputs describe a synthetic scenario',['yes','no'],'')])
    if technique==50:
        return dict(title='Simulate your quantum circuit',description='Enter up to 64 gate rows: id/x/h, target; ry, target, angle in radians; cx, target, control. Qubits start at zero and q0 is the least significant bit. Outputs are ideal circuit probabilities, not forecasts of external events.',fields=[select('qubits','Number of qubits',['1','2','3','4'],'1'),text('gates','Gate rows (blank means the initial zero state)',False),select('event_kind','Event to measure',['qubit_one','bitstring'],'qubit_one'),text('event_value','Qubit index or complete bitstring'),select('task','Calculation',['simulate','sample'],'simulate'),text('shots','Number of samples (required for sample)',False),text('seed','Replay seed, integer 1 to 4294967295 (required for sample)',False),text('attribution','Circuit source and attribution'),select('rights','Circuit rights',['self_authored','permission_granted'],'self_authored')])
    if technique==46:
        return dict(title='Record your deja reve experience',description='Describe the experience, its timing and your own recollection attributes. The output reports compatibility of these declarations and preserves narrative provenance.',fields=[text(k,label) for k,label in [('pseudonym','Pseudonym'),('source','Original record source'),('narrative','Experience narrative'),('start','Occurrence start (ISO time)'),('end','Occurrence end (ISO time)'),('recorded','First-record time (ISO time)'),('locked','Original lock time (ISO time)'),('reviewer','Reviewer ID'),('confidence','Subjective confidence')]]+[select(k,k.replace('_',' ').capitalize(),['unknown','yes','no']) for k in ['dream_association','specific_recollection','familiarity','present_dreamy_state']]+[select('temporal','Temporal context',['specific','vague','none','unknown']),select('uncertain','Are these declarations uncertain?',['yes','no'],'yes'),select('permission','Permission for local processing of your self-authored record',['yes','no'],'')])
    if technique==45:
        return dict(title='Compare two alternatives using your ordered cues',description='Enter cue rows in descending validity order: cue ID, first value, second value, validity. Values are positive, negative or unknown; validity is a documented decimal from 0.5 to 1. This core uses the higher-criterion, positive-orientation convention.',fields=[text(k,label) for k,label in [('first','First alternative ID'),('second','Second alternative ID'),('criterion','Criterion to maximize'),('domain','Decision domain'),('observed','Observation time (ISO with time zone)'),('provenance','Cue and direction provenance'),('training','Training period for cue validity'),('cues','Ordered cue rows'),('practice','Practice history')]]+[select(k,label,['recognized','unrecognized','unknown']) for k,label in [('recognition1','Recognition of first alternative'),('recognition2','Recognition of second alternative')]]+[select(k,k.replace('_',' ').capitalize(),['adequate','inadequate','unknown']) for k in ['regularity','cue_validity','feedback_quality','feedback_latency']]+[select('changed','Has the environment changed?',['yes','no'],'')])
    if technique==44:
        return dict(title='Review a dream and independently recorded event',description='Enter a declared single-slot study record and evidence. Native checks preserve chronology, locks and human ratings. This is an unblinded descriptive review, not prospective certification. All times use ISO format with a time zone; evidence is retained locally.',fields=[text(k,label) for k,label in [('study','Study ID'),('participant','Participant ID'),('coordinator','Coordinator ID'),('collector','Event collector ID'),('judge','Judge ID'),('rule','Prespecified event collection rule'),('feature','Prespecified comparison feature'),('narrative','Original dream narrative'),('detail','Dream detail for this feature'),('event_text','Independent event description'),('evidence','Evidence text'),('holder','Evidence rights holder'),('source','Evidence source reference'),('reason','Judge reasoning')]]+[select('permission','Permission to retain this dream and evidence',['yes','no'],''),select('known','Was the outcome known when recording the dream?',['yes','no'],''),select('common','Is this a common event?',['yes','no'],''),select('coverage','Event collection coverage',['complete','known_omissions','unknown'],'unknown'),select('rating','Human comparison rating',list(dream_intake.engine.DATA['ratings']),'')]+[text(k,label) for k,label in [('created','Original plan creation time'),('slot_open','Dream recording slot opens'),('slot_due','Dream recording deadline'),('collection_start','Event collection window starts'),('collection_end','Event collection window ends'),('window_start','Comparison window starts'),('window_end','Comparison window ends'),('event_start','Event occurrence starts'),('event_end','Event occurrence ends'),('discovery','Event discovery time')]]+[text(k+'_at',k.replace('_',' ').capitalize()+' time') for k in dream_intake.ACTIONS])
    if technique==43:
        return dict(title='Review a recorded five-target viewing trial',description='Enter a completed training record. This shared-workspace review is not certified blind testing. Five images are center-cropped to 256 square pixels and retained locally for native replay. Use ISO timestamps with time zones for each declared event.',fields=[text(k,label) for k,label in [('study','Study ID'),('trial','Trial ID'),('tasker','Tasker ID'),('viewer','Viewer ID'),('judge','Judge ID'),('holder','Image rights holder'),('source','Image source and attribution')]]+[dict(key='images',label='Five target images, in candidate order (under 1 MB each)',type='images',default=[]),select('permission','Permission to retain and process these target images',['yes','no'],''),select('target','Actual target number',['1','2','3','4','5'],'')]+[select('rank'+str(i),'Rank for candidate '+str(i)+' (1 closest)',list('12345'),'') for i in range(1,6)]+[text('transcript','Original viewer transcript'),text('report','Judge reasoning'),text('created','Plan creation time')]+[text(k+'_at',k.replace('_',' ').capitalize()+' time') for k in remote_intake.ACTIONS])
    if technique==40:
        return dict(title='Enter your measured compass bearing',description='Enter degrees to at most one decimal place. Select the north reference and what the bearing represents; no automatic magnetic correction is applied.',fields=[text('degrees','Bearing in degrees (0 to 359.9)'),select('north','North reference',list(feng_shui.DATA['north_references']),''),select('role','Bearing role',list(feng_shui.DATA['bearing_roles']),''),text('uncertainty','Uncertainty in degrees',False),text('alternates','Alternate readings in degrees, comma separated',False)])
    if technique==39:
        return dict(title='Compare a documentary organ-feature account',description='Enter the tradition and source-described conditions. The result compares these declarations with the inspected historical records.',fields=[select('origin','Account origin',list(haruspicy.DATA['origins']),'unknown'),*[select(k,k.replace('_',' ').capitalize(),list(v)) for k,v in haruspicy.DATA['domains'].items()]])
    if technique==38:
        return dict(title='Record your bird observation',description='Enter the source bird label, call or flight, side and reference frame. Conflicting traditions and unknown evidence remain explicit.',fields=[text('bird_label','Bird label (crow, raven, or your observed label)'),*[select(k,k.replace('_',' ').capitalize(),list(augury.DATA[d]),'unresolved' if k=='relation' else 'unknown') for k,d in [('origin','origins'),('phenomenon','phenomena'),('relative_side','sides'),('relation','relations'),('reference_frame','frames'),('observer_facing','facings')]]])
    if technique==37:
        records=cleromancy.catalog()
        return dict(title='Record the mark on your selected lot',description='Choose the actual observed Greek-letter lot and its origin. The engine returns its exact catalog reference.',fields=[select('mark','Observed lot mark',[r['id'] for r in records],''),select('origin','Observation origin',list(cleromancy.DATA['observation_origins']),''),text('question','Your question',False)],labels={'mark':{r['id']:r['glyph']+' - '+r['name'] for r in records}})
    if technique==36:
        _,_,index=bibliomancy._assets();choices=[];labels={}
        for si,shelf in enumerate(index['shelves'],1):
            for bi,book in enumerate(shelf['books'],1):
                for pi,page in enumerate(book['pages'],1):
                    for ni,sentence in enumerate(page['sentences'],1):
                        key=','.join(map(str,[si,bi,pi,ni]));choices.append(key);labels[key]='Ruth chapter '+str(page['chapter'])+', sentence '+str(ni)
        return dict(title='Choose a passage from the supported corpus',description='Select a sentence from the pinned Ruth edition. The result includes the exact passage, neighboring context and source citation.',fields=[select('path','Passage',choices,''),text('question','Question or reflection context',False),select('radius','Neighboring sentences',['0','1','2'],'1')],labels={'path':labels})
    if technique==35:
        return dict(title='Inspect or compare documented bone inscriptions',description='Choose a source case and optionally a second case. Results show translated charges, provenance and explicitly supported comparisons.',fields=[select('case','First source case',list(osteomancy.CASES),''),select('second','Optional comparison case',['none',*osteomancy.CASES],'none'),text('question','Research question',False)])
    if technique==34:
        return dict(title='Enter your stone layout',description='Use one row per stone: role, x, y (integer coordinates). Supported roles: '+', '.join(lithomancy.ROLES)+'. Choose the coordinate frame and reader anchor explicitly.',fields=[text('stones','Stone rows: role, x, y'),select('frame','Coordinate frame',list(lithomancy.FRAMES),''),select('origin','Observation origin',['reported_real','hypothetical','synthetic','unknown'],''),text('anchor_x','Reader anchor x'),text('anchor_y','Reader anchor y')])
    if technique==33:
        return dict(title='Enter the four mother figures',description='For each mother enter four digits, top to bottom: 1 for one point and 2 for two points. The engine calculates the full shield.',fields=[text('question','Question or context',False),select('origin','Cast origin',['reported_real','hypothetical','synthetic','unknown'],''),*[text('mother'+str(i),'Mother '+str(i)+' (four digits, 1 or 2)') for i in range(1,5)]])
    if technique==32:
        return dict(title='Record atmospheric observations',description='Select the region, phenomenon and observed features for comparison with the source lore.',fields=[select('origin','Observation origin',list(aeromancy.ORIGINS),''),select('region','Region',list(aeromancy.REGIONS)),select('phenomenon','Phenomenon',['smoke','wind','cloud','other','unknown'],''),*[select(k,k.replace('_',' ').capitalize(),['unknown','yes','no'] if v=='bool' else ['unknown']+[str(i) for i in range(366)] if v=='days' else list(v)) for k,v in aeromancy.FEATURES.items()]])
    if technique==31:
        return dict(title='Record a water observation',description='Describe the medium, conditions and observation basis. The engine evaluates only the conditions you supply.',fields=[select('origin','Observation origin',list(hydromancy.ORIGINS),''),select('category','Observed phenomenon',list(hydromancy.CATEGORIES),''),select('basis','Observation basis',['physical','subjective','imagined','unknown']),text('description','Your observation'),*[select(k,k.replace('_',' ').capitalize(),['unknown','yes','no'] if v=='bool' else list(v)) for k,v in hydromancy.CONTEXT.items()]])
    if technique==30:
        return dict(title='Record a candle observation',description='Enter what was observed and any known physical explanation. Native processing preserves unknowns and evaluates the source conditions.',fields=[select('origin','Observation origin',list(pyromancy.ORIGINS),''),select('phenomenon','Phenomenon',list(pyromancy.PHENOMENA),''),*[select(group+'.'+k,(group+' '+k).replace('_',' ').capitalize(),['unknown','yes','no'] if v=='bool' else list(v)) for group,fields in [('attributes',pyromancy.ATTRIBUTES),('physical',pyromancy.PHYSICAL),('safety',{k:'bool' for k in pyromancy.SAFETY_FIELDS})] for k,v in fields.items()]])
    if technique==29:
        return dict(title='Record your coffee-ground symbols',description='Enter the vessel, observed symbol and its visible attributes. Unknown attributes remain missing evidence.',fields=[select('vessel','Vessel',['cup','saucer'],''),select('symbol','Observed symbol',list(coffee.SYMBOLS),''),select('half','Cup half',list(coffee.HALVES)),*[select(k,k.replace('_',' ').capitalize(),(['unknown','yes','no'] if v=='bool' else ['unknown']+[str(i) for i in range(9 if v=='humps' else 65)] if isinstance(v,str) else list(v))) for k,v in coffee.ATTRIBUTES.items()]])
    if technique==28:
        return dict(title='Record the symbols in your tea cup',description='Choose an observed symbol, its position and features, and an optional adjacent symbol. The engine applies the documented conditions to your observations.',fields=[select('symbol','Observed symbol',list(tasseography.SYMBOLS),''),*[select(k,k.replace('_',' ').capitalize(),list(v)) for k,v in tasseography.ENUMS.items()],select('adjacent','Adjacent symbol',['none',*tasseography.SYMBOLS],'none'),select('uncertain','Is the symbol uncertain?',['yes','no'],'yes')])
    if technique==26:
        return dict(title='Frame your reference or reflection question',description='Choose your purpose and source concept. The engine returns attributed source material and reflection guidance.',fields=[text('question','Your question'),select('purpose','Purpose',list(akashic.PURPOSES),''),select('form','Question form',list(akashic.FORMS),'unspecified'),select('concept','Source concept',list(akashic.CONCEPTS),''),text('background','Relevant background',False)])
    if technique==24:
        return dict(title='Record a completed writing session',description='Supply your original writing and declared session times. The report preserves the draft and calculates descriptive text metrics.',fields=[text('intention','Writing intention'),text('writing','Your original writing'),text('start','Declared start (ISO date/time with time zone)'),text('stop','Declared stop (ISO date/time with time zone)'),select('review','Did you review this draft?',['yes','no'],'')])
    if technique==23:
        return dict(title='Describe your dream',description='Enter your narrative and choose a source motif if relevant. Unknown context remains unknown in the historical reflection.',fields=[text('narrative','Dream narrative'),select('recall','Recall quality',list(dream.RECALL),'uncertain'),select('motif','Optional historical motif',['none',*dream.MOTIFS],'none'),*[select(k,k.replace('_',' ').capitalize(),['unknown','yes','no']) for k in dream.BOOL_CONTEXT]])
    if technique==22:
        return dict(title='Record your mirror session',description='Describe the mirror setup and your own experience. The output preserves attribution and provides procedural source context.',fields=[select('surface','Mirror surface',list(mirror.DATA['surfaces']),''),select('view','Reflection view',list(mirror.DATA['view_options']),''),text('lighting','Lighting'),text('intention','Intention'),select('kind','Experience category',list(mirror.TYPES),''),text('description','Your observation'),select('uncertain','Is the observation uncertain?',['yes','no'],'yes')])
    if technique==21:
        return dict(title='Record your crystal-gazing session',description='Enter the setup and your own observations. The report preserves your journal and provides source-attributed procedural context.',fields=[select('surface','Surface',list(scrying.DATA['surfaces']),''),text('lighting','Lighting'),text('background','Background',False),text('intention','Intention'),select('kind','Experience category',list(scrying.TYPES),''),text('description','What did you observe?'),select('uncertain','Is this observation uncertain?',['yes','no'],'yes')])
    if technique==20:
        signals=[v for v in pendulum.DATA['calibration']['mappable_signals'] if v!='irregular']
        return dict(title='Record your pendulum observation',description='Declare your yes/no calibration, then record the movement and its quality. Unclear observations remain unresolved.',fields=[text('question','Your question'),select('yes','Movement calibrated as yes',signals,''),select('no','Movement calibrated as no',signals,''),select('signal','Observed movement',list(pendulum.DATA['signals']),''),select('quality','Observation quality',list(pendulum.DATA['observations']['quality']),'')])
    if technique==19:
        return dict(title='Ask your rune-casting question',description='Choose one or three runes. The draw records a fresh seed and returns source-layered symbolic references.',fields=[text('question','Your question'),select('spread','Rune spread',list(runes.SPREADS),'three')])
    if technique==18:
        return dict(title='Enter your I Ching question and lines',description='Record six line values from the bottom upward: 6 old yin, 7 young yang, 8 young yin, 9 old yang.',fields=[text('question','Your question'),*[select('line'+str(i),'Line '+str(i)+(' (bottom)' if i==1 else ' (top)' if i==6 else ''),['6','7','8','9'],'') for i in range(1,7)]])
    if technique==17:
        return dict(title='Ask your oracle-card question',description='Choose a spread. A fresh recorded random seed produces a replayable draw and the source-supported symbolic reading.',fields=[text('question','Your question'),select('spread','Spread',list(oracle.SPREADS),'three')])
    if technique==15:
        return dict(title='Inspect a historical iris-chart label',description='Select a label from the upright source plate. Results describe the historical chart and its documented limitations.',fields=[select('entry','Eye and printed label',list(iridology.DATA['entries']),''),select('certainty','Selection certainty',['selected','uncertain','unknown'])],labels={'entry':{k:v['eye']+' eye: '+v['printed_label'] for k,v in iridology.DATA['entries'].items()}})
    if technique==14:
        return dict(title='Select your symbolic colors and context',description='Enter your own symbolic selection to retrieve the documented color meaning and context.',fields=[select('color','Color',list(aura.DATA['terms']),''),select('context','Symbolic context',list(aura.DATA['contexts']),''),select('certainty','Selection certainty',['selected','uncertain','unknown'])])
    if technique==13:
        return dict(title='Describe your handwriting observations',description='Select visible writing features. Unknown features remain unresolved. The engine returns descriptive terminology and historical sources.',fields=[select('direction','Writing direction',['ltr','rtl','unknown']),*[select(k,k.replace('_',' ').capitalize(),[t for t,v in graphology.DATA['terms'].items() if k in v['features']]+['unknown']) for k in graphology.FEATURES]])
    if technique==12:
        return dict(title='Choose a documented foot or sole feature',description='The selected source feature, orientation and certainty produce a documentary reference with any conflicts retained.',fields=[select('entry','Source feature',list(podomancy.DATA['entries']),''),select('side','Foot side',['left','right','both','unknown']),select('view','View',['dorsal','plantar','unknown']),select('certainty','Selection certainty',['certain','uncertain','unknown'])])
    if technique==11:
        return dict(title='Choose a historical body-region reference',description='Select a documented region and side to retrieve the source passage and its limits.',fields=[select('region','Body region',sorted({e['region_id'] for e in moleosophy.DATA['entries'].values()}),''),select('side','Subject-relative side',['left','right','midline','unknown']),select('view','View',['frontal','posterior','unknown'])])
    if technique==10:
        return dict(title='Inspect a historical schematic label',description='Choose a printed view and label from the source. The output explains the historical label and its documented location.',fields=[select('schematic','Printed schematic',list(phrenology.DATA['schematics']),''),select('label','Printed label',list(phrenology.DATA['entries']), '')],labels={'label':{k:k+' - '+v['original_name'] for k,v in phrenology.DATA['entries'].items()}})
    if technique!=9:return None
    f=face_reading
    return dict(title='Describe the region you want to inspect',description='Record visible features and inspect the historical source associated with that region. The result contains annotations and source references.',fields=[
        select('region','Face region',list(f.DATA['regions']),''),
        select('view','View',['frontal','left_profile','right_profile','unknown']),
        select('frame','Side labels refer to',['subject','viewer'],'subject'),
        select('mirrored','Is the view mirrored?',['unknown','yes','no']),
        select('side','Region side',['unknown','left','right','both','midline']),
        select('visibility','Visibility',['unknown','visible','occluded']),
        *[select(k,k.replace('_',' ').capitalize(),choices+['unknown','uncertain']) for k,choices in f.GEOMETRY.items()],
        select('marking','Visible marking',['unknown','none','line','spot','crease'])])

def build(technique,answers):
    if technique not in [9,10,11,12,13,14,15,17,18,19,20,21,22,23,24,26,28,29,30,31,32,33,34,35,36,37,38,39,40,43,44,45,46,50,52,53]:raise ValueError('Dedicated builder is not implemented for this technique')
    if not isinstance(answers,dict):raise ValueError('Input answers must be an object')
    spec=contract(technique);a={}
    for field in spec['fields']:
        value=answers.get(field['key'],field['default'])
        if field['type']=='select' and value not in field['choices']:raise ValueError('Choose '+field['label'])
        if field['type']=='text' and (not isinstance(value,str) or len(value)>10000 or (field.get('required') and not value.strip())):raise ValueError('Enter '+field['label'])
        a[field['key']]=value
    if technique==53:
        asset=dict(id=a['asset'],state_unit=a['state_unit'],measurement_unit=a['measurement_unit'],parameter_version=a['version']);records=[]
        for row in csv.reader(io.StringIO(a['records'])):
            if not row:continue
            if len(row)!=4:raise ValueError('Each measurement needs timestamp, value, control, availability timestamp')
            at,value,control,available=[x.strip() for x in row];tick=len(records)+1
            records.append(dict(id='observation-'+str(tick),asset_id=asset['id'],state_unit=asset['state_unit'],measurement_unit=asset['measurement_unit'],tick=tick,timestamp=at,value=value or None,control=control,available_at=available or None))
        controls=[x.strip() for x in a['controls'].split(',')] if a['controls'].strip() else []
        q=dict(schema_version=1,profile=dict(id=digital_twin.DATA['id'],sha256=digital_twin.PROFILE_HASH,catalog_sha256=digital_twin.DATA['source_manifest_sha256']),mode=a['mode'],asset=asset,parameters=dict(version=a['version'],**{k:a[k].strip() for k in ('A','B','H','Q','R','m0','P0')}),timeline=dict(initial_at=a['initial'],step_seconds=int(a['step']),evaluation_at=a['evaluation']),records=records,horizon=len(controls),scenarios=[dict(id='user-scenario',controls=controls)] if controls else [],reference_scenario='user-scenario' if controls else None,provenance=dict(source_ref='digital-twin-welch-bishop-2002-v1',rights=a['rights'],attribution=a['attribution'],snapshot=a['snapshot'],snapshot_sha256=hashlib.sha256(a['snapshot'].encode()).hexdigest(),archive_checks={k:a['checked_'+k]=='yes' for k in digital_twin.DATA['schema']['archive_checks']}))
        digital_twin.validate(q)
        return dict(technique_id=53,operation='digital-twin',input=q)
    if technique==52:
        if a['synthetic']!='yes':raise ValueError('Only synthetic scenarios are supported')
        thresholds=[];edges=[]
        for row in csv.reader(io.StringIO(a['nodes'])):
            if not row:continue
            if len(row)!=2:raise ValueError('Each node row needs ID and exact threshold')
            node,phi=[x.strip() for x in row];thresholds.append(dict(node=node,phi=phi))
        thresholds.sort(key=lambda t:t['node']);nodes=[t['node'] for t in thresholds]
        for row in csv.reader(io.StringIO(a['edges'])):
            if not row:continue
            if len(row)!=2:raise ValueError('Each edge needs two node IDs')
            edges.append(sorted(x.strip() for x in row))
        scenario=dict(id='user-scenario',edges=sorted(edges),thresholds=thresholds,initial=dict(mode='fixed',fixed_seeds=sorted(x.strip() for x in a['active'].split(',') if x.strip()),probability=None,run_seeds=[],overrides=[]))
        q=dict(schema_version=1,profile=dict(id=psychohistory.DATA['id'],sha256=psychohistory.PROFILE_HASH,catalog_sha256=psychohistory.DATA['source_manifest_sha256']),population=dict(size=len(nodes),nodes=nodes),runs=1,rounds=int(a['rounds']),trace_states=True,rng=dict(algorithm='xorshift32-v1',seed=1),scenarios=[scenario],reference_scenario='user-scenario',provenance=dict(synthetic=True,source_ref='psychohistory-pentland-v1',rights='self_authored',attribution=a['attribution'],snapshot=a['snapshot'],snapshot_sha256=hashlib.sha256(a['snapshot'].encode()).hexdigest()))
        psychohistory.validate(q)
        return dict(technique_id=52,operation='psychohistory',input=q)
    if technique==50:
        gates=[]
        for row in csv.reader(io.StringIO(a['gates'])):
            if not row:continue
            row=[x.strip() for x in row];op=row[0]
            if op not in ('id','x','h','ry','cx') or len(row)!=(3 if op in ('ry','cx') else 2):raise ValueError('Use gate, target; ry, target, radians; or cx, target, control')
            gate=dict(op=op,target=int(row[1]))
            if op=='ry':gate['angle']=float(row[2])
            if op=='cx':gate['control']=int(row[2])
            gates.append(gate)
        event=dict(kind=a['event_kind'],value=int(a['event_value']) if a['event_kind']=='qubit_one' else a['event_value'].strip())
        q=quantum.request(task=a['task'],qubits=int(a['qubits']),gates=gates,event=event,shots=int(a['shots']) if a['task']=='sample' else None,seed=int(a['seed']) if a['task']=='sample' else 1)
        q['provenance'].update(rights=a['rights'],attribution=a['attribution'])
        quantum.validate(q,quantum.assets())
        return dict(technique_id=50,operation='quantum-probability-forecasting',input=q)
    if technique==46:
        if a['permission']!='yes':raise ValueError('Local processing permission required')
        attributes={k:None if a[k]=='unknown' else a[k]=='yes' for k in ['dream_association','specific_recollection','familiarity','present_dreamy_state']}
        attributes.update(temporal_context=a['temporal'],subjective_confidence=a['confidence'],reviewer=a['reviewer'],proposal=None,uncertain=a['uncertain']=='yes')
        original=dict(profile=deja_reve.DATA['id'],profile_version=1,kind='observation',id=secrets.token_hex(12),pseudonym=a['pseudonym'],source_ref=a['source'],occurrence=dict(start=a['start'],end=a['end']),first_record_at=a['recorded'],lock_at=a['locked'],narrative=a['narrative'],narrative_sha256=deja_reve.bytes_hash(a['narrative'].encode('utf-8')),context='ordinary_nonclinical',attributes=attributes,consent=dict(local_processing=True,rights='self_authored',export=False))
        record=dict(original=original,original_sha256=deja_reve.digest(original),amendments=[])
        deja_reve.validate_record(record)
        return dict(technique_id=46,operation='deja-reve',input=dict(schema_version=1,task='annotate',record=record))
    if technique==45:
        cues=[]
        for row in csv.reader(io.StringIO(a['cues'])):
            if not row:continue
            if len(row)!=4:raise ValueError('Each cue needs ID, first value, second value, validity')
            cue,x,y,v=[x.strip() for x in row];cues.append(dict(cue_id=cue,values=[x,y],validity=v,rank=len(cues)+1,provenance=a['provenance'],orientation='positive',training_period=a['training']))
        decision=dict(decision_id=secrets.token_hex(12),profile=intuitive_prediction.PROFILES['take-the-best'],alternatives=[a['first'],a['second']],criterion=a['criterion'],criterion_direction='higher',domain=a['domain'],observed_at=a['observed'],recognition=[a['recognition1'],a['recognition2']],ecological_direction='positive',direction_provenance=a['provenance'],training_period=a['training'],cues=cues,tie_policy='abstain',context=dict(**{k:a[k] for k in ['regularity','cue_validity','feedback_quality','feedback_latency']},practice_history=a['practice'],environment_changed=a['changed']=='yes'),confidence='',notes='')
        intuitive_prediction.decision(decision)
        return dict(technique_id=45,operation='intuitive-prediction',input=dict(schema_version=1,task='take-the-best',decision=decision))
    if technique==44:return dream_intake.build(a)
    if technique==43:return remote_intake.build(a)
    if technique==40:
        def tenths(value):
            n=Fraction(value)*10
            if n.denominator!=1:raise ValueError('Bearings require exact tenths of a degree; no rounding')
            return int(n)
        native=dict(schema_version=1,profile=feng_shui.PROFILE,mode='manual',task='classify',catalog_id=feng_shui.DATA['catalog_id'],catalog_version=1,catalog_sha256=feng_shui.CATALOG_HASH,bearing_tenths=tenths(a['degrees']),north_reference=a['north'],bearing_role=a['role'],uncertainty_tenths=tenths(a['uncertainty'] or '0'),alternate_readings=[tenths(x.strip()) for x in a['alternates'].split(',') if x.strip()])
        feng_shui.validate(native)
        return dict(technique_id=40,operation='feng-shui',input=native)
    if technique==39:
        native=dict(schema_version=1,profile=haruspicy.PROFILE,mode='manual',task='compare',catalog_id=haruspicy.DATA['catalog_id'],catalog_version=1,catalog_sha256=haruspicy.CATALOG_HASH,observations=[dict(observation_id='observed',**a)])
        haruspicy.validate(native)
        return dict(technique_id=39,operation='haruspicy',input=native)
    if technique==38:
        native=dict(schema_version=1,profile=augury.PROFILE,mode='manual',task='observe',catalog_id=augury.DATA['catalog_id'],catalog_version=1,catalog_sha256=augury.CATALOG_HASH,observations=[dict(observation_id='observed',**a)])
        augury.validate(native)
        return dict(technique_id=38,operation='augury',input=native)
    if technique==37:
        native=dict(schema_version=1,profile=cleromancy.PROFILE,mode='manual',task='reading',catalog_id=cleromancy.DATA['catalog_id'],catalog_version=1,catalog_sha256=cleromancy.CATALOG_HASH,mark=a['mark'],observation_origin=a['origin'],question=a['question'])
        cleromancy.validate(native)
        return dict(technique_id=37,operation='cleromancy',input=native)
    if technique==36:
        native=dict(schema_version=1,profile=bibliomancy.PROFILE,mode='manual_coarse',corpus_version=1,index_version=1,**{k:bibliomancy.DATA[k] for k in ['corpus_id','corpus_sha256','index_id','index_sha256']},selections=[dict(path=[int(x) for x in a['path'].split(',')])],question=a['question'],context=int(a['radius']))
        bibliomancy.validate(native,bibliomancy._assets()[2])
        return dict(technique_id=36,operation='bibliomancy',input=native)
    if technique==35:
        ids=[a['case']]+([] if a['second']=='none' else [a['second']])
        native=dict(schema_version=1,profile=osteomancy.PROFILE,mode='documentary',task='reference' if len(ids)==1 else 'compare',case_ids=ids,research_question=a['question'])
        osteomancy.validate(native)
        return dict(technique_id=35,operation='osteomancy',input=native)
    if technique==34:
        stones=[]
        for row in csv.reader(io.StringIO(a['stones'])):
            if not row:continue
            if len(row)!=3:raise ValueError('Each stone row needs role, x, y')
            role,x,y=[v.strip() for v in row];stones.append(dict(id='stone'+str(len(stones)+1),role_id=role,position=dict(x=int(x),y=int(y))))
        native=dict(schema_version=1,profile=lithomancy.PROFILE,task='manual_spatial_reading',mode='manual',reading_id=secrets.token_hex(12),frame=a['frame'],coverage='full_example' if len(stones)==12 else 'subset',origin=a['origin'],stones=stones,anchor=dict(kind='reader',position=dict(x=int(a['anchor_x']),y=int(a['anchor_y']))))
        lithomancy.validate(native)
        return dict(technique_id=34,operation='lithomancy',input=native)
    if technique==33:
        native=dict(schema_version=1,profile=geomancy.PROFILE,task='shield',mode='manual',input_mode='patterns',mothers=[a['mother'+str(i)].strip() for i in range(1,5)],origin=a['origin'],question=a['question'])
        geomancy.validate(native)
        return dict(technique_id=33,operation='geomancy',input=native)
    if technique==32:
        features={k:(a[k]=='yes' if v=='bool' else int(a[k]) if v=='days' else a[k]) for k,v in aeromancy.FEATURES.items() if a[k]!='unknown'}
        native=dict(schema_version=1,profile=aeromancy.PROFILE,task='atmospheric_lore_comparison',mode='manual',origin=a['origin'],region=a['region'],observations=[dict(id='observed',phenomenon=a['phenomenon'],features=features)])
        aeromancy.validate(native)
        return dict(technique_id=32,operation='aeromancy',input=native)
    if technique==31:
        session={k:(a[k]=='yes' if v=='bool' else a[k]) for k,v in hydromancy.CONTEXT.items() if a[k]!='unknown'}
        native=dict(schema_version=1,profile=hydromancy.PROFILE,task='water_observation_reference',mode='manual',origin=a['origin'],session=session,observations=[dict(id='observed',sequence=1,origin=a['origin'],category=a['category'],basis=a['basis'],description=a['description'])])
        hydromancy.validate(native)
        return dict(technique_id=31,operation='hydromancy',input=native)
    if technique==30:
        row=dict(id='observed',phenomenon=a['phenomenon'],origin=a['origin'])
        for group,fields in [('attributes',pyromancy.ATTRIBUTES),('physical',pyromancy.PHYSICAL),('safety',{k:'bool' for k in pyromancy.SAFETY_FIELDS})]:
            row[group]={k:(a[group+'.'+k]=='yes' if v=='bool' else a[group+'.'+k]) for k,v in fields.items() if a[group+'.'+k]!='unknown'}
        native=dict(schema_version=1,profile=pyromancy.PROFILE,task='symbolic_candle_observation',mode='manual',origin=a['origin'],observations=[row])
        pyromancy.validate(native)
        return dict(technique_id=30,operation='pyromancy',input=native)
    if technique==29:
        attrs={k:(a[k]=='yes' if v=='bool' else int(a[k]) if v in ('dots','humps') else a[k]) for k,v in coffee.ATTRIBUTES.items() if a[k]!='unknown'}
        native=dict(schema_version=1,profile=coffee.PROFILE,task='symbolic_coffee_reading',mode='manual',vessel=a['vessel'],observations=[dict(id='observed',symbol_id=a['symbol'],half=a['half'],attributes=attrs)])
        coffee.validate(native)
        return dict(technique_id=29,operation='coffee-reading',input=native)
    if technique==28:
        rows=[dict(id='observed',symbol_id=a['symbol'],uncertainty=a['uncertain']=='yes',**{k:a[k] for k in tasseography.ENUMS})]
        if a['adjacent']!='none':
            rows[0]['adjacent_to']=['adjacent'];rows.append(dict(id='adjacent',symbol_id=a['adjacent']))
        native=dict(schema_version=1,profile=tasseography.PROFILE,task='symbolic_cup_reading',mode='manual',vessel='cup',observations=rows)
        tasseography.validate(native)
        return dict(technique_id=28,operation='tasseography',input=native)
    if technique==26:
        native=dict(schema_version=1,profile=akashic.PROFILE,task='reference_reflection',mode='manual',question=dict(text=a['question'],purpose=a['purpose'],form=a['form']),concept_ids=[a['concept']],background=a['background'])
        akashic.validate(native)
        return dict(technique_id=26,operation='akashic-reference',input=native)
    if technique==24:
        events=[dict(id='begin',type='begin',timestamp=a['start']),dict(id='writing',type='append',segment=dict(id='draft',order=1,text=a['writing'],authorship='user')),dict(id='stop',type='stop',timestamp=a['stop'])]
        if a['review']=='yes':events.append(dict(id='review',type='review'))
        events.append(dict(id='complete',type='complete'))
        native=dict(schema_version=1,profile=automatic_writing.PROFILE,task='guided_writing',mode='manual',session_id=secrets.token_hex(12),state='completed',intention=a['intention'],review_policy='required' if a['review']=='yes' else 'no_review',events=events)
        automatic_writing.validate(native)
        return dict(technique_id=24,operation='automatic-writing',input=native)
    if technique==23:
        native=dict(schema_version=1,profile=dream.PROFILE,task='historical_reflection',mode='manual',narrative=a['narrative'],recall=a['recall'],lookups=[] if a['motif']=='none' else [a['motif']],context={k:a[k]=='yes' for k in dream.BOOL_CONTEXT if a[k]!='unknown'})
        dream.validate(native)
        return dict(technique_id=23,operation='dream',input=native)
    if technique==22:
        native=dict(schema_version=1,profile=mirror.PROFILE,task='guided_mirror_journal',mode='manual',session=dict(surface=a['surface'],view=a['view'],lighting=a['lighting'],intention=a['intention']),journal=[dict(experience_type=a['kind'],description=a['description'],uncertainty=a['uncertain']=='yes')])
        mirror.validate(native)
        return dict(technique_id=22,operation='mirror-scrying',input=native)
    if technique==21:
        native=dict(schema_version=1,profile=scrying.PROFILE,task='guided_journal',mode='manual',session=dict(surface=a['surface'],lighting=a['lighting'],background=a['background'],intention=a['intention']),journal=[dict(experience_type=a['kind'],description=a['description'],uncertainty=a['uncertain']=='yes')])
        scrying.validate(native)
        return dict(technique_id=21,operation='scrying',input=native)
    if technique==20:
        native=dict(schema_version=1,profile=pendulum.PROFILE,task='symbolic_response',mode='manual',question=a['question'],calibration=[dict(signal=a['yes'],response='yes'),dict(signal=a['no'],response='no')],observations=[dict(signal=a['signal'],quality=a['quality'])])
        pendulum.validate(native)
        return dict(technique_id=20,operation='pendulum',input=native)
    if technique==19:
        native=dict(schema_version=1,profile=runes.PROFILE,task='symbolic_reading',mode='seeded',spread=a['spread'],question=a['question'],seed=secrets.token_hex(16),protocol=runes.PROTOCOL,orientation_policy='upright_only')
        runes.validate(native)
        return dict(technique_id=19,operation='runes',input=native)
    if technique==18:
        native=dict(schema_version=1,profile=iching.PROFILE,reading_policy=iching.POLICY,task='symbolic_reading',mode='manual',method='manual',line_order='bottom_to_top',lines=[int(a['line'+str(i)]) for i in range(1,7)],question=a['question'])
        iching.validate(native)
        return dict(technique_id=18,operation='iching',input=native)
    if technique==17:
        native=dict(schema_version=1,profile=oracle.PROFILE,task='symbolic_reading',mode='seeded',spread=a['spread'],question=a['question'],seed=secrets.token_hex(16),protocol=oracle.PROTOCOL,orientation_policy='upright_only')
        oracle.validate(native)
        return dict(technique_id=17,operation='oracle',input=native)
    if technique==15:
        entry=iridology.DATA['entries'][a['entry']]
        native=dict(schema_version=1,profile=iridology.PROFILE,task='historical_reference',mode='manual',diagram='frontispiece',view='source_plate_upright',selections=[dict(eye=entry['eye'],label_id=entry['label_id'],certainty=a['certainty'])])
        iridology.validate(native)
        return dict(technique_id=15,operation='iridology-reference',input=native)
    if technique==14:
        native=dict(schema_version=1,profile=aura.PROFILE,task='symbolic_reference',mode='manual',components=[dict(color=a['color'],context=a['context'],certainty=a['certainty'])])
        aura.validate(native)
        return dict(technique_id=14,operation='aura-reference',input=native)
    if technique==13:
        native=dict(schema_version=1,profile=graphology.PROFILE,task='historical_reference',mode='manual',script='latin',writing_direction=a['direction'],observations=[dict(feature=k,category=a[k],scope='whole_sample',certainty='unknown' if a[k]=='unknown' else 'certain') for k in graphology.FEATURES])
        graphology.validate(native)
        return dict(technique_id=13,operation='graphology-reference',input=native)
    if technique==12:
        native=dict(schema_version=1,profile=podomancy.PROFILE,task='historical_reference',mode='manual',orientation=dict(frame='subject',view=a['view'],mirrored=False),selections=[dict(entry_id=a['entry'],side=a['side'],certainty=a['certainty'])])
        podomancy.validate(native)
        return dict(technique_id=12,operation='podomancy-reference',input=native)
    if technique==11:
        native=dict(schema_version=1,profile=moleosophy.PROFILE,task='historical_reference',mode='manual',orientation=dict(frame='subject',view=a['view'],mirrored=False),selections=[dict(region_id=a['region'],side=a['side'])])
        moleosophy.validate(native)
        return dict(technique_id=11,operation='moleosophy-reference',input=native)
    if technique==10:
        native=dict(schema_version=1,profile=phrenology.PROFILE,task='historical_reference',schematic=a['schematic'],selections=[dict(label_id=a['label'])])
        phrenology.validate(native)
        return dict(technique_id=10,operation='phrenology-reference',input=native)
    native=dict(schema_version=1,profile=face_reading.PROFILE,task='historical_reference',mode='manual',orientation=dict(view=a['view'],side_frame=a['frame'],mirrored={'yes':True,'no':False}.get(a['mirrored'],'unknown')),observations=[dict(region_id=a['region'],side=a['side'],visibility=a['visibility'],geometry={k:a[k] for k in face_reading.GEOMETRY},markings=[a['marking']])])
    face_reading.validate(native)
    return dict(technique_id=9,operation='face-reference',input=native)


