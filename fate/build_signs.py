"""Freeze the bounded consumer edition by evaluating every selectable native input."""
from itertools import product
import json

from .signs import AIR_SETTINGS, ENGINES, FIELDS, SignInput, allowed, read_sign
from .western import ROOT

OUT = ROOT/'fate/web/src/signs'


def build():
    edition = dict(profiles={str(room):m.PROFILE for room,m in ENGINES.items()},
                   fields={str(room):f for room,f in FIELDS.items()},air=AIR_SETTINGS)
    rows = {}
    for room,spec in FIELDS.items():
        records = {}
        for combination in product(*(dict(field['options']) for field in spec)):
            if not allowed(room,combination):
                continue
            evidence = read_sign(SignInput(oracle=room,values=list(combination)))
            if evidence['snapshot'] is not None:
                records['|'.join(combination)] = evidence['view']
        rows[str(room)] = records
    return edition, rows


if __name__=='__main__':
    for name, data in zip(('edition-v1.json','reference-v1.json'),build()):
        path = OUT/name
        output = json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n'
        if path.exists() and path.read_text(encoding='utf-8')!=output:
            raise SystemExit(f'Frozen {name} differs. Create a new edition.')
        path.write_text(output,encoding='utf-8')
