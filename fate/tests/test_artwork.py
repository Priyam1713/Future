"""Offline asset acceptance, independent of presentation/LLM interpretations."""
import hashlib
import json
import unittest
from pathlib import Path
from PIL import Image
from future.tarot_catalog import ORDER, card

ROOT=Path(__file__).resolve().parents[1]

class ArtworkAcceptance(unittest.TestCase):
    def test_complete_identity_registry_and_rights(self):
        manifest=json.loads((ROOT/'web/src/artwork/deck-manifest.json').read_text(encoding='utf-8'))
        sources=json.loads((ROOT/'artwork-sources.json').read_text(encoding='utf-8'))
        self.assertEqual(set(manifest['cards']),set(ORDER))
        self.assertEqual(set(sources['cards']),set(ORDER))
        for key in ORDER:
            row=manifest['cards'][key];source=sources['cards'][key]
            self.assertEqual(row['cardId'],key);self.assertEqual(row['name'],card(key)['name'])
            self.assertEqual(source['license_code'],'pd');self.assertEqual(source['restrictions'],'')
            self.assertIn('Pamela Colman Smith',source['artist'])
            self.assertEqual(source['date'],'1910')
            self.assertIn('Rider-Waite-Smith tarot deck (TaionWC)',source['categories'])
            self.assertTrue(source['source_page'].startswith('https://commons.wikimedia.org/wiki/File:'))

    def test_every_delivery_file_matches_its_immutable_hash(self):
        sources=json.loads((ROOT/'artwork-sources.json').read_text(encoding='utf-8'))
        hashes=[]
        for row in sources['cards'].values():
            for variant in row['variants']:
                path=ROOT/'web/public'/variant['src'].lstrip('/')
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),variant['sha256'])
                with Image.open(path) as image:self.assertEqual(image.size,(variant['width'],variant['height']))
                hashes.append(variant['sha256'])
        self.assertEqual(len(hashes),156);self.assertEqual(len(set(hashes)),156)

    def test_independent_major_numbering_and_court_images(self):
        rows=json.loads((ROOT/'artwork-sources.json').read_text(encoding='utf-8'))['cards']
        self.assertIn('08 Strength',rows['major-08']['file_title'])
        self.assertIn('11 Justice',rows['major-11']['file_title'])
        self.assertEqual(rows['cups-page']['file_title'],'File:Cups11.jpg')
        self.assertEqual(rows['cups-knight']['file_title'],'File:Cups12.jpg')
        self.assertEqual(rows['cups-queen']['file_title'],'File:Cups13.jpg')
        self.assertEqual(rows['cups-king']['file_title'],'File:Cups14.jpg')

if __name__=='__main__':unittest.main()
