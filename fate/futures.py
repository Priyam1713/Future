"""Bounded consumer studies over the frozen native operation profiles."""

from datetime import datetime, timezone
from fractions import Fraction
from functools import lru_cache
from pathlib import Path
from typing import Literal
import json

from pydantic import BaseModel, ConfigDict, Field, StrictInt

from future import (agent_based, ai_predictive_modeling as modeling, akashic, automatic_writing,
                    brain_intention, causal_ai, chaos_theory, collective_intelligence as collective,
                    deja_reve, digital_twin, intuitive_prediction, multiverse, prediction_markets,
                    prophetic_dreams, psychohistory, quantum_probability_forecasting as quantum,
                    superforecasting)
from future.lab.registry import capability

ROOT = Path(__file__).resolve().parents[1]
MODULES = {
    24: automatic_writing, 26: akashic, 44: prophetic_dreams, 45: intuitive_prediction,
    46: deja_reve, 49: modeling, 50: quantum, 51: superforecasting, 52: psychohistory,
    53: digital_twin, 54: agent_based, 55: brain_intention, 56: causal_ai,
    57: collective, 58: prediction_markets, 59: chaos_theory, 60: multiverse,
}
FIXTURES = {
    24: 'automatic-writing-complete', 44: 'prophetic-dreams',
    45: 'intuitive-prediction-third-cue', 46: 'deja-reve-specific-prior-dream',
    49: 'ai-predictive-modeling-naive', 50: 'quantum-probability-forecasting-cli/bell',
    51: 'superforecasting-cli/bayes-positive', 52: 'psychohistory-cli/path',
    53: 'digital-twin-cli/missing', 54: 'agent-based-cli/glider',
    55: 'brain-intention-features-benchmark', 56: 'causal-ai-cli/confounding',
    57: 'collective-intelligence-cli/equal', 58: 'prediction-markets-cli/buy-one',
    59: 'chaos-theory-cli/symmetric', 60: 'multiverse-small-benchmark',
}
CONCEPTS = ('records', 'pathway', 'describe', 'question_framing', 'scope_limits')
LIMITS = {24: 0, 26: 4, 44: 0, 45: 2, 46: 3, 49: 4, 50: 3, 51: 4, 52: 2,
          53: 1, 54: 12, 55: 8, 56: 1, 57: 10, 58: 8, 59: 3, 60: 100}
DEFAULTS = {54: 4, 55: 5, 57: 8, 58: 1, 59: 1, 60: 50}


class StudyInput(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid')
    oracle: Literal[24, 26, 44, 45, 46, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60]
    option: StrictInt | None = None
    text: str | None = Field(default=None, max_length=4000)
    consent: bool = False
    cells: list[StrictInt] | None = Field(default=None, max_length=49)


def fixture(name):
    return json.loads((ROOT / 'data' / f'{name}-input.json').read_text(encoding='utf-8-sig'))


@lru_cache(maxsize=18)
def sources(oracle):
    rows = []
    for entry in capability(oracle)['sources']:
        values = json.loads((ROOT / entry['path']).read_text(encoding='utf-8-sig'))
        if isinstance(values, dict):
            values = values.get('sources', [values])
        if not isinstance(values, list):
            continue
        for row in values:
            if isinstance(row, dict) and row.get('id'):
                rows.append(dict(id=row['id'], title=row.get('title') or row.get('author') or row['id'],
                                 url=row.get('url', ''), locator=row.get('locator') or row.get('edition') or ''))
    return rows


def selection(q):
    option = DEFAULTS.get(q.oracle, 0) if q.option is None else q.option
    if not 0 <= option <= LIMITS[q.oracle]:
        raise ValueError('Choose a supported instrument setting.')
    if q.text is not None and (q.oracle not in (24, 26, 46) or not q.consent or not q.text.strip()):
        raise ValueError('Enter your own text and explicitly permit processing.')
    if q.cells is not None and (q.oracle != 54 or len(q.cells) != 49 or any(bit not in (0,1) for bit in q.cells)):
        raise ValueError('The cell loom accepts exactly 49 binary values.')
    if q.oracle == 46 and q.text is None and option:
        raise ValueError('Write a recollection before choosing a manual description.')
    return option


def utc_now(clock):
    return datetime.fromtimestamp(clock(), timezone.utc).isoformat()


def native_request(q, clock):
    i, n = q.oracle, selection(q)
    if i == 26:
        request = dict(schema_version=1, profile=akashic.PROFILE, task='reference_reflection',
                       mode='manual', concept_ids=[CONCEPTS[n]])
        if q.text:
            request['question'] = dict(text=q.text, purpose='personal_reflection', form='open')
        return request
    request = fixture(FIXTURES[i])
    if i == 24 and q.text:
        request['events'] = [dict(id='begin', type='begin'), dict(id='page', type='append',
            segment=dict(id='draft', order=1, text=q.text, authorship='user')),
            dict(id='stop', type='stop'), dict(id='complete', type='complete')]
        request.pop('intention', None)
        request['session_id'] = 'visitor-draft'
    if i == 45:
        decision = request['decision']
        decision.pop('notes', None)
        decision['notes'] = 'Synthetic cue ordering exercise.'
        decision['cues'][-1]['values'] = [('positive','negative'), ('negative','positive'), ('positive','positive')][n]
        decision['cues'][-1]['values'] = list(decision['cues'][-1]['values'])
    if i == 46 and q.text:
        stamp = utc_now(clock)
        original = request['record']['original']
        flags = [(None, None, None, None, 'unknown'), (True, True, True, False, 'specific'),
                 (True, False, True, False, 'vague'), (False, False, False, True, 'none')][n]
        attrs = dict(zip(('dream_association','specific_recollection','familiarity','present_dreamy_state','temporal_context'), flags))
        original.update(pseudonym='visitor', source_ref='participant-declaration', occurrence=None,
            first_record_at=stamp, lock_at=stamp, narrative=q.text,
            narrative_sha256=deja_reve.bytes_hash(q.text.encode()), attributes=dict(
                **attrs, subjective_confidence='', reviewer='self', proposal=None, uncertain=False))
        request['record']['original_sha256'] = deja_reve.digest(original)
    if i == 49:
        if n == 4:
            benchmark = fixture('ai-predictive-modeling-noaa-benchmark')
            benchmark.pop('resource_evidence', None)
            return benchmark
        request['model'] = ('naive','drift','mean','ses_alpha0.5_initial_y1')[n]
    if i == 50:
        circuit = request['circuit']
        programs = [circuit['gates'], [dict(op='h', target=0), dict(op='h', target=1)],
                    [dict(op='x', target=1)], [dict(op='ry', target=0, angle=1.5707963267948966)]]
        circuit['gates'] = programs[n]
    if i == 51:
        record = request['payload']['record']
        ratio = ('3','1','0','1/2','5')[n]
        record['bayes']['ratio'] = ratio
        record['probability'] = str(superforecasting.posterior('1/5', ratio))
    if i == 52:
        request['scenarios'][0]['initial']['fixed_seeds'] = [request['population']['nodes'][n]]
    if i == 53 and n == 1:
        row = request['records'][-1]
        row.update(value='4', available_at=row['timestamp'])
    if i == 54:
        request['ticks'] = n
        if q.cells is not None:
            request['scenarios'][0]['initial_grid'] = [q.cells[x:x+7] for x in range(0,49,7)]
    if i == 55:
        request['trials'][-1]['values'][0] = n
    if i == 56 and n == 1:
        request['adjustment'] = []
    if i == 57:
        request['forecasts'][-1]['probability'] = str(Fraction(n, 10))
    if i == 58:
        if n == 0:
            request['events'] = []
        else:
            request['events'][0]['delta'] = str(n)
    if i == 59:
        request.update(initial=['1','1','1'], perturbed_initial=['101/100','1','1'])
        request['integration'].update(steps=(300,900,1500,2100)[n], trace_stride=12)
    if i == 60:
        for node in request['nodes']:
            if node['id'] in ('A','B'):
                node['weight'] = str(Fraction(n if node['id']=='A' else 100-n,100))
    return request


def read(q, clock):
    from .future_views import project
    request = native_request(q, clock)
    report = MODULES[q.oracle].read(request)
    private = q.text is not None
    view = project(q.oracle, request, report, private)
    output = dict(oracle=q.oracle, result=report, view=view, sources=sources(q.oracle), private=private)
    if not private:
        output['request'] = request
    # The native Déjà Rêvé edition restricts private records to local processing.
    if private and q.oracle == 46:
        output['result'] = dict(status=report['status'], task=report['task'],
                                result=dict(compatibility=report['result']['compatibility']),
                                report_sha256=report['report_sha256'])
    return output
