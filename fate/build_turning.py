"""Immutable archive of native transit source identities; old Codex editions stay intact."""
import json
from pathlib import Path
from future.core_readings import DATA
ROOT=Path(__file__).resolve().parents[1]


def build():
    rows=json.loads((ROOT/'knowledge/western_rules.json').read_text(encoding='utf-8'))+json.loads((ROOT/'knowledge/transit_rules.json').read_text(encoding='utf-8'))+[r for r in DATA['records'] if r['kind'] in ('house','planet_symbol')]
    return dict(id='fate-transit-reference-v1',records=[r for r in rows if r['tradition']=='modern psychological' and r['kind']!='methodology'])


if __name__=='__main__':
    p=ROOT/'fate/web/src/turning/reference-v1.json';out=build()
    if p.exists() and json.loads(p.read_text(encoding='utf-8'))!=out:
        raise SystemExit('Refusing to overwrite a saved transit source edition. Add a new edition.')
    p.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
