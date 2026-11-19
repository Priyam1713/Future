"""Freeze only versioned, rights-scoped reference data from the native engines."""
import json
from .ritual import ENGINES, bibliomancy_request
from .western import ROOT
from future import bibliomancy, dream, geomancy, mirror, oracle, pendulum, scrying

OUT = ROOT / 'fate/web/src/ritual'


def build():
    _, corpus, index = bibliomancy._assets()
    pages = []
    for offset, page in enumerate(index['shelves'][0]['books'][0]['pages'], 1):
        if not page['sentences']:
            continue
        chapter = corpus['chapters'][page['chapter']-1]
        passages = [dict(bibliomancy._passage(sentence, chapter, page), path=[1, 1, offset, pos])
                    for pos, sentence in enumerate(page['sentences'], 1)]
        pages.append(dict(id=page['id'], chapter=chapter['chapter'], passages=passages))
    base = dict(profiles={str(room): engine.PROFILE for room, engine in ENGINES.items()},
                cards=list(oracle.ORDER), motifs=list(dream.MOTIFS),
                sentences=[p['sentence_id'] for page in pages for p in page['passages']],
                parents=[list(row) for row in geomancy.PARENTS])
    guides = {}
    for room, engine in [(21, scrying), (22, mirror)]:
        native = engine.read(dict(schema_version=1, profile=engine.PROFILE, mode='manual',
            task='guided_journal' if room == 21 else 'guided_mirror_journal'))
        guides[str(room)] = dict(steps=native['guidance'], source=native['sources'][0], types=list(engine.TYPES),
            surfaces=list(engine.DATA['surfaces']))
    archive = dict(
        cards=[oracle.card(key) for key in oracle.ORDER], cardSource=oracle._thaw(oracle.DATA['source']),
        pendulum=dict(source=pendulum.thaw(pendulum.DATA['source']), rules=pendulum.thaw(pendulum.DATA['rules']),
                      signals=pendulum.thaw(pendulum.DATA['signals']), quality=list(pendulum.DATA['observations']['quality'])),
        guides=guides,
        dream=dict(source=dream.thaw(dream.DATA['source']), greek=dream.thaw(dream.DATA['greek_source']),
                   motifs={key:dream.lookup(key,{}) for key in dream.MOTIFS}),
        geo=dict(figures=geomancy.thaw(geomancy.DATA['figures']), source=geomancy.thaw(geomancy.DATA['source']),
                 locator=geomancy.DATA['construction_locator']),
        book=dict(pages=pages, source=corpus['source'], procedure=bibliomancy.thaw(bibliomancy.DATA['procedure_source']),
                  edition=corpus['edition'], pin=bibliomancy_request()),
    )
    return base, archive


if __name__ == '__main__':
    for name, data in zip(('edition-v1.json', 'reference-v1.json'), build()):
        path = OUT / name
        content = json.dumps(data, ensure_ascii=False, separators=(',', ':'))+'\n'
        if path.exists() and path.read_text(encoding='utf-8') != content:
            raise SystemExit('Frozen Ritual Wing source differs. Create a new edition.')
        path.write_text(content, encoding='utf-8')
