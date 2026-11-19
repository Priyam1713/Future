"""Protocol adapters and minimal public anchors for FATE's Ritual Wing."""
from typing import Literal

from pydantic import BaseModel, ConfigDict
from future import bibliomancy, dream, geomancy, mirror, oracle, pendulum, scrying

ENGINES = {17: oracle, 20: pendulum, 21: scrying, 22: mirror, 23: dream, 33: geomancy, 36: bibliomancy}


class RitualInput(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)
    oracle: Literal[17, 20, 21, 22, 23, 33, 36]
    input: dict


def bibliomancy_request():
    fields = ('corpus_id', 'corpus_sha256', 'index_id', 'index_sha256')
    return {**{key: bibliomancy.DATA[key] for key in fields}, 'corpus_version': 1, 'index_version': 1}


def native_request(room, inputs):
    base = dict(schema_version=1, profile=ENGINES[room].PROFILE, mode='manual')
    if room == 17:
        if set(inputs) != {'seed', 'spread'}:
            raise ValueError('Provide a seed and one, three or five cards.')
        base.update(task='symbolic_reading', mode='seeded', protocol=oracle.PROTOCOL, orientation_policy='upright_only')
    elif room == 20:
        base['task'] = 'symbolic_response'
        if set(inputs) == {'seed'}:
            base.update(mode='seeded', protocol=pendulum.PROTOCOL, distribution=pendulum.DISTRIBUTION)
        elif set(inputs) != {'calibration', 'observations'}:
            raise ValueError('Supply either a symbolic seed or a calibration and manual observation.')
    elif room in (21, 22):
        base['task'] = 'guided_journal' if room == 21 else 'guided_mirror_journal'
    elif room == 23:
        base['task'] = 'historical_reflection'
    elif room == 33:
        if set(inputs) != {'mothers'}:
            raise ValueError('Supply four manually set top-to-bottom Mother patterns.')
        base.update(task='shield', input_mode='patterns', figure_convention=geomancy.CONVENTION)
    else:
        if set(inputs) != {'selections', 'context'}:
            raise ValueError('Pick passages and nearby context from the pinned edition.')
        base.update(mode='manual_coarse', **bibliomancy_request())
    if base.keys() & inputs.keys():
        raise ValueError('The chamber profile and protocol are fixed.')
    return dict(base, **inputs)


def snapshot(room, result):
    if room == 17:
        result_values = [row['card']['id'] for row in result['readings']]
    elif room == 20:
        result_values = [result['mode'], result['outcome']['symbolic_response']]
    elif room in (21, 22):
        # A guide bookmark, never a persisted report that implies a real observation.
        result_values = []
    elif room == 23:
        # Preserve public motif references only. Condition choices and all notes stay in the visit.
        result_values = [row['motif_id'] for row in result['motif_references'] if row['status'] != 'unsupported']
    elif room == 33:
        result_values = [row['pattern'] for row in result['positions']]
    else:
        result_values = [str(result['replay']['request']['context']), *[row['sentence_id'] for row in result['selections']]]
    return dict(oracle=room, profile=ENGINES[room].PROFILE, values=result_values)


def read(q):
    result = ENGINES[q.oracle].read(native_request(q.oracle, q.input))
    return dict(result=result, snapshot=snapshot(q.oracle, result))
