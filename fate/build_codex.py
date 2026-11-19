"""Versioned source reference for reopening minimal local chapters, never inputs."""
import json
from pathlib import Path
from future.tarot_catalog import DATA, thaw

ROOT = Path(__file__).resolve().parents[1]


def build():
    tarot = thaw(DATA)
    numbers = json.loads((ROOT/'knowledge/numerology_readings_v1.json').read_text(encoding='utf-8'))
    return dict(version='fate-codex-reference-v1', tarot=dict(profile=tarot['profile'], source=tarot['source'], cards=tarot['cards']), numerology=numbers)


if __name__ == '__main__':
    path = ROOT/'fate/web/src/codex/reference-v1.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    reference = build()
    if path.exists() and json.loads(path.read_text(encoding='utf-8')) != reference:
        raise SystemExit('Reference v1 is frozen. Create a new source edition; never overwrite saved chapters’ reference.')
    path.write_text(json.dumps(reference, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
