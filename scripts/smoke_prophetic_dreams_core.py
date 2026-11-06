import copy,json,re,subprocess,sys,tempfile
from pathlib import Path
from future import prophetic_dreams as p
from tests.test_prophetic_dreams import F,build,action,tm

def req(task,**kw):return dict(schema_version=1,profile=p.PROFILE,task=task,**kw)
def examples():
    valid=build();exposed=build('exposed');parent=p.verify(valid)['entries']['dream1']['versions'][-1]['sha256']
    amendment=action(valid,'amend',dict(entry_id='dream1',parent_sha256=parent,text='More specific later narrative.',reason='Post-outcome clarification',outcome_known=True))
    commentary=action(valid,'commentary',dict(kind='feedback',text='Later feedback recorded.',event_reference='e1'))
    commentary=action(commentary,'commentary',dict(kind='association',text='A different later association;not a replacement endpoint.',event_reference='unregistered external event'))
    late=copy.deepcopy(F['entries']);late[0]['first_record_at']=tm(7,7,1)
    unknown=copy.deepcopy(F['events']);unknown[0]['occurrence']=None
    common=copy.deepcopy(F['events']);common[0]['common']=True
    blank=copy.deepcopy(F['entries']);blank[0]['text']='';blank[0]['details']={}
    boundary=copy.deepcopy(F['events']);boundary[0]['occurrence']=dict(start=tm(8,0),end=tm(8,0),precision='second')
    multi=copy.deepcopy(F['events']);multi[1]['occurrence']=dict(start=tm(8,13),end=tm(8,13),precision='second')
    pp=copy.deepcopy(F['plan']);pp['window'].update(endpoint='publication',end=tm(9,23))
    omissions=copy.deepcopy(F['events']);omissions[0]['coverage']='known_omissions'
    conflict=copy.deepcopy(F['events']);conflict[0]['publication_at']=tm(10,0)
    withdrawn=build('recording');withdrawn=action(withdrawn,'slot_status',dict(slot_id='s1',status='withdrawn',reason='Explicitwithdrawal'),at=tm(9,16,20));withdrawn=action(withdrawn,'seal',at=tm(9,17))
    aborted=action(p.create(F['plan']),'terminate',dict(status='aborted',reason='Stopped study;all slots retained.'))
    known=copy.deepcopy(F['entries']);known[0]['outcome_known']=True
    unblinded=copy.deepcopy(F['plan']);unblinded['blinding']='descriptive_unblinded'
    pairs=build('sealed',events=multi);pairs=action(pairs,'expose',dict(judge_id='j1',knowledge='unaware'))
    ratings={x['pair_id']:'match' if x['eligible'] else 'protocol_invalid' for x in p.pairs(pairs)}
    pairs=action(pairs,'rate',dict(ratings=ratings,notes='All eligible pairs marked match bydeclaredhumanfixture.'),actor='j1')
    good={
      'prospective':req('report',ledger=valid),'unknown-dream-time':req('report',ledger=valid),'after-event-before-discovery':req('report',ledger=valid),
      'amendment':req('report',ledger=amendment),'nonrecall':req('report',ledger=valid),'unsubmitted':req('report',ledger=valid),
      'late':req('report',ledger=build(entries=late)),'boundary':req('report',ledger=build(events=boundary)),
      'outside-window':req('report',ledger=valid),'uncertain-interval':req('report',ledger=valid),'multiple-matches':req('report',ledger=pairs),
      'common':req('report',ledger=build(events=common)),'duplicate-news':req('report',ledger=valid),'nonmatch':req('report',ledger=valid),
      'conflicting-time':req('report',ledger=build(events=conflict)),'two-judges':req('report',ledger=valid),'later-association':req('report',ledger=commentary),
      'zero-information':req('report',ledger=build(entries=blank)),'unicode':req('report',ledger=valid),'publication-endpoint':req('report',ledger=build(plan=pp)),
      'known-omissions':req('report',ledger=build(events=omissions)),'withdrawn':req('report',ledger=withdrawn),'aborted':req('report',ledger=aborted),
      'known-outcome':req('report',ledger=build(entries=known)),'unblinded':req('report',ledger=build(plan=unblinded)),
      'judge-packet':req('judge_packet',ledger=exposed,judge_id='j1'),
      'martinique':req('reference',ids=['martinique']),'lecture-nonmatch':req('reference',ids=['lecture-nonmatch']),'wargo-envelope':req('reference',ids=['wargo-envelope'])}
    def bad_ledger(field,value):
        l=copy.deepcopy(valid);l[field]=value;return req('report',ledger=l)
    mutation=copy.deepcopy(valid);mutation['events'][0]['payload']['entry']['text']+='x'
    wrongpool=copy.deepcopy(valid);wrongpool['plan']['universe_sha256']='0'*64
    criteria=copy.deepcopy(valid);criteria['plan']['features'][0]['description']='posthoc'
    window=copy.deepcopy(valid);window['plan']['window']['end']=tm(10,0)
    rank=copy.deepcopy(valid);next(e for e in rank['events'] if e['action']=='rate')['payload']['ratings']['d1:e1']='nonmatch'
    leak=p.judge_packet(exposed,'j1');leak['answer_flag']=True
    rights=copy.deepcopy(F['events'][0]);rights['evidence']['permission']=''
    no_consent=copy.deepcopy(F['plan']);no_consent['privacy_consent']=False
    bad={
      'one-byte-mutation':req('report',ledger=mutation),'wrong-universe':req('report',ledger=wrongpool),'changed-criteria':req('report',ledger=criteria),
      'window-expansion':req('report',ledger=window),'packet-leak':req('validate_packet',packet=leak),'rating-mutation':req('report',ledger=rank),
      'no-rights':req('apply',ledger=build('recording',events=[]),action='event',actor='collector',at=tm(9,16),payload=dict(event=rights)),
      'missing-timezone':req('apply',ledger=p.create(F['plan']),action='seal',actor='coordinator',at='2026-11-09T17:00:00',payload={}),
      'premature-reveal':req('apply',ledger=build('sealed'),action='reveal',actor='coordinator',at=tm(9,17,1),payload={}),
      'after-reveal-rating':req('apply',ledger=valid,action='rate',actor='j1',at=tm(9,21),payload=dict(ratings={},notes='posthoc')),
      'wrong-parent':req('apply',ledger=valid,action='amend',actor='person1',at=tm(9,21),payload=dict(entry_id='dream1',parent_sha256='0'*64,text='amend',reason='wrongparent',outcome_known=True)),
      'no-consent':req('judge_packet',ledger=build('exposed',plan=no_consent),judge_id='j1'),
      'incomplete-universe':req('apply',ledger=build('recording',events=F['events'][:-1]),action='seal',actor='coordinator',at=tm(9,17),payload={}),
      'invalid-schema':req('report',ledger=valid)|dict(unknown=True),'unsupported-prophecy':req('predict',ledger=valid)}
    return good,bad

def run():
    good,bad=examples();cases=[]
    with tempfile.TemporaryDirectory() as tmp:
        inp=Path(tmp,'input.json')
        def cli(name,q,fmt='json',reject=False,save=None,extra=()):
            inp.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            result=subprocess.run([sys.executable,'-m','future','prophetic-dreams',str(inp),'--format',fmt,*extra],capture_output=True)
            assert result.returncode==(2 if reject else 0),(name,result.stderr,result.stdout[:200])
            raw=result.stdout.decode('utf-8').replace('\r\n','\n').rstrip('\n')+'\n'
            if fmt=='json':actual=json.loads(raw)
            else:
                match=re.search(r'(`{3,})json\n(.*?)\n\1',raw,re.S);assert match,name;actual=json.loads(match[2])
            try:expected=p.read(q)
            except ValueError:expected=dict(visibility='public_error',status='rejected',error='Dream ledger request rejected',prophetic_dreams_report=None)
            assert actual==expected,(name,'exactreplay')
            if save:Path(save).write_bytes(raw.encode())
            cases.append(dict(case=name,format=fmt,rejected=reject,passed=True));return actual
        for reject,examples_ in [(False,good),(True,bad)]:
            for name,q in examples_.items():
                Path(f'data/prophetic-dreams-{name}-input.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
                for fmt in ('json','markdown'):cli(name,q,fmt,reject,save=f'data/prophetic-dreams-{name}.'+('json' if fmt=='json' else 'md'))
                if not reject:cli(name+' repeat',q)
        # Reproduce every action from an independent-spec study through CLI.
        ledger=cli('lifecycle create',req('create',plan=F['plan']))['ledger']
        for e in good['prospective']['ledger']['events']:
            ledger=cli('lifecycle '+e['action'],req('apply',ledger=ledger,action=e['action'],actor=e['actor'],at=e['at'],payload=e['payload']))['ledger']
        assert ledger==good['prospective']['ledger']
        packet=cli('export judge',good['judge-packet'],extra=('--export-dir',str(Path(tmp,'judge'))))
        assert json.loads(Path(tmp,'judge/packet.json').read_text(encoding='utf-8'))==packet
        assert [x.name for x in Path(tmp,'judge').iterdir()]==['packet.json']
    Path('data/prophetic-dreams-input.json').write_text(json.dumps(good['prospective'],ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    Path('data/prophetic-dreams-smoke.json').write_text(json.dumps(dict(passed=True,cli_cases=len(cases),accepted_pairs=len(good),rejected_pairs=len(bad),complete_cli_lifecycle=True,actual_allowlisted_export=True,cases=cases),indent=2)+'\n',encoding='utf-8')
    print(f'{len(cases)} Prophetic Dreams CLI cases passed;{len(good)}accepted/{len(bad)}rejected JSON/Markdown replay pairs;complete lifecycle andexport')
if __name__=='__main__':run()
