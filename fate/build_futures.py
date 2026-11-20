"""Freeze public study bookmarks, with the native archive inputs kept server-side."""
import json
from pathlib import Path

from .futures import DEFAULTS, LIMITS, StudyInput, read


OUT = Path(__file__).parent / 'web/src/futures'


def build():
    index, folios = {}, {}
    for oracle, maximum in LIMITS.items():
        if oracle == 46:
            maximum = 0
        index[oracle] = dict(maximum=maximum,default=DEFAULTS.get(oracle,0))
        choices = {}
        for option in range(maximum+1):
            result = read(StudyInput(oracle=oracle,option=option),lambda:0)
            choices[option] = {key: result['view'][key] for key in ('status','title','lead')}
        folios[oracle] = dict(choices=choices,sources=result['sources'])
    return index, folios


if __name__ == '__main__':
    OUT.mkdir(exist_ok=True)
    for name, value in zip(('index-v1.json','folios-v1.json'),build()):
        target = OUT / name
        output = json.dumps(value,ensure_ascii=False,separators=(',',':'))+'\n'
        if target.exists() and target.read_text(encoding='utf-8') != output:
            raise SystemExit(f'Frozen {name} differs. Create a new edition.')
        target.write_text(output,encoding='utf-8')
