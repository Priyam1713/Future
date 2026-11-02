"""Lossless cell-value import and reproducible structural audit of the source inventory."""
import hashlib
import json
from collections import Counter
from pathlib import Path
import openpyxl

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'resources/Prediction_Techniques_Resource_Inventory_v1.xlsx'

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def build():
    workbook = openpyxl.load_workbook(SOURCE, data_only=False)
    sheets = {s.title: list(s.values) for s in workbook}
    tables = {name: [dict(zip(rows[0], row)) for row in rows[1:]]
              for name, rows in sheets.items() if name != 'Start Here'}
    methods = tables['60 Methods']
    variations = tables['Variations']
    sources = tables['Ranked Sources']
    edges = tables['Dependencies & Blends']
    exclusions = tables['6 Exclusions']
    assert len(sheets) == 6
    assert [m['ID'] for m in methods] == list(range(1, 61))
    assert (len(variations), len(sources), len(edges)) == (260, 151, 91)
    excluded = {x['ID'] for x in exclusions}
    assert excluded == {25, 27, 41, 42, 47, 48}
    assert {m['ID'] for m in methods if m['Disposition'].startswith('EXCLUDE')} == excluded
    by_id = {m['ID']: m for m in methods}
    for rows in (variations, sources):
        for row in rows:
            assert row['Method ID'] in by_id
            assert row['Technique'] == by_id[row['Method ID']]['Technique']
    for edge in edges:
        for prefix in ('From', 'To'):
            assert edge[f'{prefix} ID'] in by_id
            assert edge[f'{prefix} technique'] == by_id[edge[f'{prefix} ID']]['Technique']
        assert edge['From ID'] != edge['To ID']
    prerequisites = [e for e in edges if e['Type'] == 'Prerequisite']
    # Numerical order is a topological ordering iff every prerequisite points forward.
    assert all(e['From ID'] < e['To ID'] for e in prerequisites)
    assert all(e['From ID'] not in excluded and e['To ID'] not in excluded for e in prerequisites)
    for method in methods:
        mid = method['ID']
        ranks = [s['Rank (within method)'] for s in sources if s['Method ID'] == mid]
        assert ranks == list(range(1, len(ranks) + 1))
        declared = {int(v.strip()) for v in str(method['Prerequisite IDs'] or '').split(',') if v.strip()}
        actual = {e['From ID'] for e in prerequisites if e['To ID'] == mid}
        assert declared == actual, (mid, declared, actual)
    warnings = []
    for method in methods:
        mid = method['ID']
        leads = [s for s in sources if s['Method ID'] == mid]
        variants = [v for v in variations if v['Method ID'] == mid]
        warnings.append({
            'technique_id': mid, 'name': method['Technique'],
            'retained': mid not in excluded,
            'status': 'Researching' if mid == 1 else 'Not Started',
            'variation_count': len(variants), 'source_count': len(leads),
            'missing_source_urls': [s['Rank (within method)'] for s in leads if not s['URL / catalog']],
            'coverage_status': 'unverified',
            'gaps': ['Edition and chapter coverage unverified', 'Ingestion rights unverified',
                     'No verified executable rule fixtures in original inventory'],
            'provisional_variation_sources_not_in_ranked_list': sorted({v[k] for v in variants
                for k in ('Source #1 (provisional)', 'Source #2 (provisional)')
                if v[k] and v[k] not in {s['Resource title'] for s in leads}}),
        })
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    write(ROOT / 'knowledge/inventory.json', {'source_sha256': digest, 'sheets': sheets})
    write(ROOT / 'knowledge/gaps.json', warnings)
    report = {'source_sha256': digest, 'sheets': len(sheets), 'techniques': len(methods),
              'retained': 60-len(excluded), 'excluded_ids': sorted(excluded),
              'variations': len(variations), 'ranked_sources': len(sources),
              'relationships': len(edges), 'prerequisites': len(prerequisites),
              'prerequisite_graph_acyclic_and_in_sequence': True,
              'missing_source_urls': sum(not s['URL / catalog'] for s in sources),
              'source_verification': 'Structural audit only; bibliographic claims remain provisional'}
    write(ROOT / 'knowledge/inventory_audit.json', report)
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    build()
