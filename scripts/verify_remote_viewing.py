"""Frozen pre-engine order-position oracle and sixteen procedural fixture families."""
import copy
import hashlib
import itertools
import json
from pathlib import Path
import unittest
from future import remote_viewing as r
from tests.test_remote_viewing import RemoteViewingTests


def run():
    f=json.loads(Path('tests/fixtures/remote_viewing_reference_v1.json').read_text(encoding='utf-8'))
    frozen=json.loads(Path('data/remote-viewing-fixture-freeze.json').read_text(encoding='utf-8'))
    assert hashlib.sha256(Path('tests/fixtures/remote_viewing_reference_v1.json').read_bytes()).hexdigest()==frozen['fixture_raw_sha256']
    assert r.digest(f)==frozen['fixture_sha256'] and not frozen['production_exists']
    assert f['profile_sha256']==r.PROFILE_HASH
    checks=0;null_sum=0;null_hits=0
    for row in f['arithmetic']['permutations']:
        order=row['best_to_worst']
        for target in f['arithmetic']['targets']:
            # Source of expectations is position in a pre-engine candidate order,
            # not the production alias/rank mapping or a production report.
            expected=row['expected_rank_by_target'][target]
            assert expected==order.index(target)+1
            null_sum+=expected;null_hits+=expected==1
            for display in f['arithmetic']['display_permutations']:
                ranks={alias:order.index(candidate)+1 for alias,candidate in zip(['c1','c2','c3','c4','c5'],display)}
                assert r.rank_result(ranks,target,display)==expected
                checks+=1
    assert checks==72000 and null_sum==1800 and null_hits==120
    k=f['known_answer'];t=k['reported_trial']
    assert r.preimage(t)==k['preimage'] and r.digest(k['preimage'])==k['commitment']
    ctx=r.verify_trial(t)
    assert ctx['viewer_lock']==k['viewer_lock'] and ctx['judge_lock']==k['judge_lock']
    assert r.report(t)['judge_results'][0]['actual_target_rank']==k['expected_rank']
    # Independent canonical serialization of lock inputs, no production lock helper.
    for kind,actions in [('viewer',['entry','feedback']),('judge',['rank'])]:
        records=[e for e in t['events'] if e['accepted'] and e['action'] in actions]
        v=dict(domain='future.remote-viewing.lock.v1',kind=kind,trial_id=t['plan']['trial_id'],records=records)
        b=json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
        assert hashlib.sha256(b).hexdigest()==k[kind+'_lock']
    groups={
        'concealment':['concealment','judge_packet','public_status','pre_reveal_markdown_no_private_replay','export_viewer_only_packet'],
        'transcript-lock':['transcript_mutation','rehashed_transcript_still_breaks_lock','attachment_lock_and_neutral_export','no_silent_amendment'],
        'metadata-leak':['metadata_chunk_eXIf','metadata_chunk_tEXt','metadata_chunk_iTXt','metadata_chunk_zTXt','metadata_chunk_tIME','packet_does_not_copy_sidecars','export_fresh_directory'],
        'permutations':['actual_target_rank_1','actual_target_rank_3','actual_target_rank_5','duplicate_alias'],
        'replay':['known_commitment','known_source_locks','replay','original_whitespace'],
        'score-precommit':['scoring_precommitment','frozen_primary_endpoint','frozen_tie_policy','frozen_stopping_rule','frozen_exclusion_rule'],
        'premature-reveal':['premature_reveal_retained','unauthorized_reveal','wrong_opening'],
        'duplicate-reuse':['duplicate_judge_assignment','duplicate_trial_ledger','target_reuse_rejected','declared_dependence','repeated_ranking_rejected'],
        'times':['timezone_missing_attempt','reverse_chronology','offset_comparison'],
        'conflicts':['role_collision','aware_blind_viewer','judge_lock_requires_every_judge'],
        'wrong-pool':['wrong_pool','wrong_asset_digest','asset_mutation'],
        'zero-information':['chance_space','private_os_rejection_sampling','malformed_uniform_log'],
        'judges':['judge_disagreement_one_trial','judge_mutation','judge_public_text_mutation'],
        'simulated':['simulated_every_packet','human_manual_no_uniform_claim','human_cannot_predictable_seed'],
        'rights':['rights_holder','rights_permission','rights_basis','rights_attribution'],
        'failure-history':['failure_then_success_preserved','full_ledger_required','terminal_aborted','terminal_invalid','terminal_leaked','terminal_excluded','terminal_conflicted','unblinded_training','blind_feedback_rejected']}
    assert set(groups)=={x['id'] for x in f['procedural_families']}
    results=[]
    for family,names in groups.items():
        suite=unittest.TestSuite(RemoteViewingTests('test_'+name) for name in names)
        result=unittest.TestResult();suite.run(result)
        assert result.wasSuccessful(),(family,result.errors,result.failures)
        results.append(dict(family=family,passed=True,checks=result.testsRun,tests=names))
    out=dict(passed=True,profile=r.PROFILE,profile_sha256=r.PROFILE_HASH,fixture_sha256=frozen['fixture_sha256'],fixture_freeze_commit='752210e',rank_permutations=120,target_identities=5,display_permutations=120,independent_rank_checks=checks,null_cases=600,null_rank_sum=null_sum,null_hits=null_hits,null_expected_rank={'numerator':3,'denominator':1},null_top_rank={'numerator':1,'denominator':5},known_answer_commitment=True,known_answer_viewer_lock=True,known_answer_judge_lock=True,procedural_families=results,source_stage_labels=['I','II','III','IV','V','VI'],empirical_validation=False,qualification='Frozen pre-engine expectations; no real human/ESP benchmark. Procedural family tests exercise public file export,metadata,locks,chronology,all-attempt ledger and truthfully bounded declarations.')
    Path('data/remote-viewing-verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    print('72000 independent target/ranking/display checks;600-case uniform null;16 procedural fixture families passed')

if __name__=='__main__':run()
