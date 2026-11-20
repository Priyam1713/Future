"""Freeze a consumer discovery projection without changing the source inventory."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'knowledge/inventory.json'
HISTORICAL = {9, 10, 13, 15}


def build():
    inventory = json.loads(SOURCE.read_text(encoding='utf-8'))
    methods = []
    for row in inventory['sheets']['60 Methods'][1:]:
        if row[0] in (25, 27, 41, 42, 47, 48):
            continue
        methods.append(dict(id=row[0], phase=int(row[1][0]), name=row[2],
                            status='available' if row[0] in (1, 2, 3, 4, 16, 17, 18, 19, 20, 21, 22, 23, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39) else 'historical' if row[0] in HISTORICAL else 'upcoming',
                            variations=row[5], mechanism=row[6], limits=row[8], evidence=row[9],
                            source=dict(title=row[10], author=row[11], url=row[12])))
    # Git may check text out with CRLF; hash the same UTF-8/LF source on every OS.
    return dict(version=1, source='knowledge/inventory.json', source_sha256=hashlib.sha256(SOURCE.read_bytes().replace(b'\r\n', b'\n')).hexdigest(),
                excluded_ids=[25, 27, 41, 42, 47, 48], methods=methods)


if __name__ == '__main__':
    (ROOT / 'fate/web/src/gallery/inventory.json').write_text(json.dumps(build(), ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
