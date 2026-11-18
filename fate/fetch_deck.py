"""One-time verified illustration acquisition. No runtime external requests.

Only the complete original Pam-A scan set is accepted. Resizing/encoding is a
lossy delivery derivative, with no cropping, recoloring or generative alteration.
"""
import hashlib
import html
import io
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image
from future.tarot_catalog import ORDER, card

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'web/public/art/deck/pam-a-v1'
API = 'https://commons.wikimedia.org/w/api.php?'
HEADERS = {'User-Agent': 'FATE-Offline-Art-Archive/1.0 (original artwork attribution; no runtime hotlinking)'}


def get(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS), timeout=45) as response:
                return response.read()
        except Exception:
            if attempt == 3:
                raise
            time.sleep(2 + attempt * 2)


def query(**params):
    return json.loads(get(API + urllib.parse.urlencode(dict(action='query', format='json', **params))))['query']


def plain(value):
    return html.unescape(re.sub('<[^>]+>', '', value))


def main():
    category = 'Category:Rider-Waite-Smith tarot deck (TaionWC)'
    titles = [item['title'] for item in query(list='categorymembers', cmtitle=category, cmlimit=100)['categorymembers']]
    assert len(titles) == 78 and all(title.startswith('File:') for title in titles)
    pages = []
    for i in range(0, len(titles), 20):
        pages += list(query(titles='|'.join(titles[i:i+20]), prop='imageinfo', iiprop='url|extmetadata|sha1|timestamp', iiurlwidth=720)['pages'].values())
    indexed = {p['title']: p for p in pages}
    majors = {int(re.search(r'RWS Tarot (\d\d)', title)[1]): title for title in titles if 'RWS Tarot' in title}
    prefix = {'wands': 'Wands', 'cups': 'Cups', 'swords': 'Swords', 'pentacles': 'Pents'}
    source_rows, entries = {}, {}
    OUT.mkdir(parents=True, exist_ok=True)
    cache = ROOT.parent/'tmp/fate-illustration-downloads'
    cache.mkdir(parents=True, exist_ok=True)
    for card_id in ORDER:
        native = card(card_id)
        title = majors[native['number']] if native['arcana'] == 'major' else f"File:{prefix[native['suit']]}{native['rank_number']:02d}.jpg"
        page = indexed[title]
        info = page['imageinfo'][0]
        meta = info['extmetadata']
        value = lambda key: plain(str(meta.get(key, {}).get('value', '')))
        assert value('License') == 'pd' and value('LicenseShortName') == 'Public domain', title
        assert value('Copyrighted').lower() == 'false' and not value('Restrictions'), title
        assert 'Pamela Colman Smith' in value('Artist') and '1910' == value('DateTimeOriginal'), title
        assert 'Rider-Waite-Smith tarot deck (TaionWC)' in value('Categories'), title
        raw_path = cache/(card_id+'.jpg')
        url = info['thumburl'].split('?')[0]
        if not raw_path.exists():
            raw_path.write_bytes(get(url))
            time.sleep(.12)
        raw = raw_path.read_bytes()
        original = Image.open(io.BytesIO(raw)).convert('RGB')
        assert original.width >= 360 and original.height > original.width
        variants = []
        for width in [360, 720]:
            image = original.copy()
            image.thumbnail((width, 1600), Image.Resampling.LANCZOS)
            filename = f'{card_id}-{width}.webp'
            image.save(OUT/filename, 'WEBP', quality=86, method=6)
            variants.append(dict(src=f'/art/deck/pam-a-v1/{filename}', width=image.width, height=image.height, sha256=hashlib.sha256((OUT/filename).read_bytes()).hexdigest()))
        entries[card_id] = dict(cardId=card_id, name=native['name'], src=variants[0]['src'], srcSet=', '.join(f"{v['src']} {v['width']}w" for v in variants), width=variants[0]['width'], height=variants[0]['height'], credit='Pamela Colman Smith · Pam-A, 1910', source=info['descriptionurl'])
        source_rows[card_id] = dict(file_title=title, page_id=page['pageid'], source_page=info['descriptionurl'], original_url=info['url'].split('?')[0], downloaded_url=url, original_commons_sha1=info['sha1'], revision_timestamp=info['timestamp'], downloaded_sha256=hashlib.sha256(raw).hexdigest(), artist=value('Artist'), date=value('DateTimeOriginal'), license=value('LicenseShortName'), license_code=value('License'), categories=value('Categories'), credit=value('Credit'), restrictions=value('Restrictions'), derivative='Resize and WebP encoding only; full scan retained, no artistic edits', variants=variants)
        print('Verified illustration '+card_id, flush=True)
    runtime = dict(id='fate-pam-a-archive-v1', version=1, title='The Archive Edition', artist='Pamela Colman Smith', year=1910, coverage='complete_78_card_deck', cards=entries)
    (ROOT/'web/src/artwork').mkdir(parents=True, exist_ok=True)
    (ROOT/'web/src/artwork/deck-manifest.json').write_text(json.dumps(runtime, indent=2)+'\n', encoding='utf-8')
    (ROOT/'artwork-sources.json').write_text(json.dumps(dict(schema_version=1, category='https://commons.wikimedia.org/wiki/'+urllib.parse.quote(category), checked_on='2026-11-19', collection='Complete 78-card Pam-A set; no modern recolored/restored deck substitution', cards=source_rows), indent=2)+'\n', encoding='utf-8')
    print('Complete verified illustration registry: 78 cards, 156 delivery derivatives')


if __name__ == '__main__':
    main()
