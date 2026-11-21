"""Verify or initialize the frozen Codex interpretation references."""
import json
from pathlib import Path

from future.chinese import SOURCES as BAZI_SOURCES
from future.chinese_readings import CATALOG
from . import jyotish_reading as jyotish
from . import natal_rules as natal

OUT = Path(__file__).parent / "web/src/codex/narrative-reference-v1.json"


def build():
    western = {}
    for rule in (*natal.HOUSES.values(), *natal.SIGNS.values(),
                 *natal.ASCENDANT.values(), *natal.ASPECTS.values(),
                 natal.RULERSHIP, natal.CHART_RULER):
        ref = rule.reference()
        western[rule.id] = {key: ref[key] for key in
                            ("url", "locator", "edition", "text", "exceptions")}

    vedic = {key: dict(url=f"{jyotish.URL}#page={page}", locator=locator,
                       edition=jyotish.EDITION, text="", exceptions=[])
             for key, (page, locator) in jyotish.SOURCES.items()}

    sources = {row["id"]: row for row in BAZI_SOURCES}
    bazi = {}

    def add(rule_id, row, text="", exceptions=()):
        source = sources[row["source_id"]]
        bazi[rule_id] = dict(url=source["url"] or "", locator=row["locator"],
                             edition=source["edition"], text=text, exceptions=exceptions)

    for row in CATALOG["day_master_components"] + CATALOG["pillar_components"]:
        add(row["id"], row, row["text"], [row["limitation"]])
    add("chinese.ten-gods", CATALOG["relations"])
    hidden = CATALOG["hidden_stems"]
    add("chinese.hidden-stems", hidden, exceptions=[hidden["exception"]])
    return {"fate-western-natal-v1": western, jyotish.VERSION: vedic, "fate-bazi-reading-v1": bazi}


if __name__ == "__main__":
    encoded = json.dumps(build(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if OUT.exists():
        if OUT.read_text(encoding="utf-8") != encoded:
            raise SystemExit("Narrative references differ from the frozen edition.")
    else:
        OUT.write_text(encoded, encoding="utf-8")
