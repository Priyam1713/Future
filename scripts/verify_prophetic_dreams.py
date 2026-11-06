"""Pre-engine integer-time/version and manually enumerated denominator oracles."""
import hashlib,json,unittest
from datetime import datetime,timedelta
from pathlib import Path
from future import prophetic_dreams as p
from tests.test_prophetic_dreams import F,build,PropheticDreamsTests

def run():
    frozen=json.loads(Path('data/prophetic-dreams-fixture-freeze.json').read_text(encoding='utf-8'))
    raw=Path('tests/fixtures/prophetic_dreams_reference_v1.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==frozen['raw_sha256'] and not frozen['production_exists']
    assert p.digest(F)==frozen['fixture_sha256'] and F['profile_sha256']==p.PROFILE_HASH
    base=datetime.fromisoformat('2026-11-07T00:00:00+00:00')
    time=lambda m:(base+timedelta(minutes=m)).isoformat()
    for row in F['chronology_grid']:
        interval=dict(start=time(row['start_minute']),end=time(row['end_minute']),precision='minute')
        assert p.window_status(interval,dict(start=time(10),end=time(20)))==row['expected_window']
        assert p.chronology(time(5),time(6),interval,time(30))==row['expected_chronology']
    for row in F['timezone_cases']:
        interval=dict(start=row['event_start'],end=row['event_end'],precision='second')
        assert p.chronology(row['record'],row['lock'],interval,time(30))==row['expected']
    ledger=build();report=p.report(ledger)
    # Hand-authored eight-row Cartesian truth predates production;no expected pair helper calls.
    expected=[(x['dream_id'],x['event_id'],x['eligible'],x['duplicate'],x['common']) for x in F['pair_oracle']]
    actual=[(x['dream_id'],x['event_id'],x['eligible'],x['duplicate'],x['common']) for x in report['pairs']]
    assert expected==actual
    d=F['denominators'];assert len(report['slots'])==d['planned_slots']
    for key in ('recorded','nonrecall','unsubmitted'):assert report['slot_counts'][key]==d[key]
    for key,field in [('total_pairs','total'),('eligible_pairs','eligible'),('excluded_pairs','excluded'),('duplicate_pairs','duplicates'),('common_pairs','common')]:assert report['pair_counts'][field]==d[key]
    for j,values in F['judge_expected'].items():
        for key,count in values.items():assert report['per_judge_category_counts'][j][key]==count
    for entry,expected_hash,lock in zip(F['entries'],F['original_sha256'],F['lock_sha256']):
        # Independent serializer/hash of the literal frozen values.
        value=dict(domain='future.prophetic-dreams.version.v1',entry=entry)
        raw=json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
        assert hashlib.sha256(raw).hexdigest()==expected_hash
        found=report['original_entries'][entry['id']]
        assert found['original_sha256']==expected_hash and found['lock_sha256']==lock
    groups={
      'prospective-lock':['prospective_lock','known_original_hashes','known_lock_hashes'],
      'occurrence-vs-record':['occurrence_vs_record','invalid_dream_occurrence'],
      'occurrence-vs-discovery':['occurrence_vs_discovery','publication_endpoint_separate'],
      'version-mutation':['version_mutation','mutation_text','mutation_details','mutation_first_record_at','mutation_occurrence'],
      'after-outcome-edit':['after_outcome_edit','amend_wrong_parent','no_amend_original_replacement'],
      'window-boundaries':['window_boundaries','uncertain_window','unknown_event_time'],
      'missing-conflicting-time':['missing_conflicting_time','missing_timezone'],
      'criteria-precommit':['criteria_precommit','invalid_plan_primary_endpoint'],
      'universe-version':['universe_version','wrong_universe_hash','complete_events_required'],
      'nonmatches-denominator':['nonmatches_denominator','late_entry','withdrawn_entry'],
      'duplicate-common-event':['duplicate_common_event','coverage_omissions'],
      'one-to-many':['one_to_many'],
      'judge-blinding':['judge_blinding','packet_leak_answer_flag','packet_leak_filename','packet_leak_caption','exported_bytes','public_packet_mutation'],
      'judge-disagreement':['judge_disagreement','all_judges_required','after_reveal_rating_rejected'],
      'feedback-contamination':['feedback_contamination','premature_reveal'],
      'zero-information':['zero_information','known_outcome_capture'],
      'replay-rights':['replay_rights','unicode_whitespace','wrong_local_bytes','rights_permission','privacy_gate'],
      'source-isolation':['source_isolation']}
    assert set(groups)=={x['id'] for x in F['families']}
    results=[]
    for family,names in groups.items():
        result=unittest.TestResult();unittest.TestSuite(PropheticDreamsTests('test_'+name) for name in names).run(result)
        assert result.wasSuccessful(),(family,result.errors,result.failures)
        results.append(dict(family=family,passed=True,checks=result.testsRun,tests=names))
    out=dict(passed=True,profile=p.PROFILE,profile_sha256=p.PROFILE_HASH,fixture_sha256=frozen['fixture_sha256'],fixture_commit='2c69e33',chronology_intervals=300,independent_interval_and_chronology_checks=600,timezone_cases=2,manual_pair_space=8,manual_eligible_pairs=2,manual_excluded_pairs=6,planned_slots=4,known_original_and_lock_hashes=4,procedural_families=results,null_model=None,empirical_validation=False,qualification='Frozen pre-engine integer-time andhand-enumerated pair/status/version expectations;source/user/editorial layers distinct. Familymutation/leak checks supplementindependenttruth,notan empiricalprecognitionbenchmark.')
    Path('data/prophetic-dreams-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('600 independent interval/chronology checks;2timezone cases;8hand-enumerated pairs;18procedural families passed')
if __name__=='__main__':run()
