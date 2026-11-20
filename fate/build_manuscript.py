"""Build the pinned bookshelf from verified native source lookups."""

import json
from pathlib import Path

from .manuscript import MANUSCRIPTS, MOUNTAINS, archive_options, mountain_view, read_archive


OUT = Path(__file__).parent / 'web/src/manuscript'


def build():
    catalog = {}
    views = {}
    for oracle in MANUSCRIPTS:
        catalog[oracle] = archive_options(oracle)
        views[oracle] = {}
        for key, _, _ in catalog[oracle]:
            _, view = read_archive(oracle, key, 'left' if oracle == 8 else None)
            if oracle == 8:
                assert read_archive(oracle, key, 'right')[1] == view
            views[oracle][key] = view
    catalog[40] = [(row['id'], row['source_group_label'], row['source_label']) for row in MOUNTAINS]
    views[40] = {row['id']: mountain_view(row) for row in MOUNTAINS}
    mountains = [{key: row[key] for key in ('id', 'source_label', 'lower_tenths', 'upper_tenths', 'wraps_north')}
                 for row in MOUNTAINS]
    return dict(options=catalog, mountains=mountains), views


def main():
    OUT.mkdir(exist_ok=True)
    for name, data in zip(('catalog-v1.json', 'reference-v1.json'), build()):
        path = OUT / name
        content = json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n'
        if path.exists() and json.loads(path.read_text(encoding='utf-8')) != json.loads(content):
            raise SystemExit(f'Frozen {name} differs. Create a new source edition.')
        path.write_text(content, encoding='utf-8')


if __name__ == '__main__':
    main()
