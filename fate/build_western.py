"""Freeze the native modern natal source edition; never replace a saved edition."""
import json
from pathlib import Path
from future.core_readings import DATA

ROOT=Path(__file__).resolve().parents[1]


def build():
    rows=json.loads((ROOT/'knowledge/western_rules.json').read_text(encoding='utf-8'))+DATA['records']
    return dict(id='fate-western-reference-v1',tradition='modern psychological',records=[r for r in rows if r['tradition']=='modern psychological' and r['kind'] in ('planet','planet_symbol','sign','house','aspect')])


def main():
    target=ROOT/'fate/web/src/astrology/reference-v1.json'
    document=build()
    if target.exists() and json.loads(target.read_text(encoding='utf-8'))!=document:
        raise SystemExit('Refusing to change the frozen Western v1 source edition. Add a new edition instead.')
    target.write_text(json.dumps(document,indent=2)+'\n',encoding='utf-8')


if __name__=='__main__':main()
