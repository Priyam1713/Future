import json
from datetime import datetime, timezone
from unittest import TestCase

from fastapi.testclient import TestClient
from future import astrocartography, feng_shui, horary, mundane

from fate.api import create_app
from fate.build_manuscript import OUT, build
from fate.manuscript import MANUSCRIPTS, archive_request, compass_request, CompassInput
from fate.western import WesternService


SITE = dict(latitude=51.5072, longitude=-0.1276, zone='Europe/London')
MOMENT = dict(SITE, local='1990-07-15T14:30', fold=None)
QUESTION = 'QA example for source diagnostics.'
ENTRIES = {
    8: 'head.curvature.very_sloping', 9: 'forehead', 10: 'frontis-frontal/9',
    11: 'arm', 12: 'sole_many_long_lines', 13: 'ascending', 14: 'pale_rose',
    15: 'right-stomach',
}


class ManuscriptTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = WesternService()
        cls.addClassCleanup(cls.engine.close)
        cls.client = TestClient(create_app())
        cls.client.__enter__()
        cls.addClassCleanup(cls.client.__exit__, None, None, None)

    def submit(self, oracle, **values):
        response = self.client.post('/api/sky-manuscript', json=dict(oracle=oracle, **values))
        self.assertEqual(response.status_code, 200, response.text[:1000])
        self.assertEqual(response.headers['cache-control'], 'no-store')
        return response.json()

    def parity(self, envelope, expected):
        self.assertEqual(envelope['result'], json.loads(json.dumps(expected)))

    def test_all_eight_manuscripts_match_pinned_profiles(self):
        for oracle, entry in ENTRIES.items():
            with self.subTest(oracle=oracle):
                extra = {'hand': 'left'} if oracle == 8 else {}
                envelope = self.submit(oracle, selection=entry, **extra)
                args = archive_request(oracle, entry, **extra)
                engine = MANUSCRIPTS[oracle]
                self.parity(envelope, (engine.read if oracle == 8 else engine.reference)(args))
                self.assertEqual(envelope['reference'], entry)
                if oracle > 8:
                    self.assertFalse(envelope['result']['inference_enabled'])
                self.assertTrue(all(n['sourceId'] and n['locator'] for n in envelope['view']['sources']))

    def test_frozen_archive_equals_native_results(self):
        for name, expected in zip(('catalog-v1.json', 'reference-v1.json'), build()):
            actual = json.loads((OUT / name).read_text(encoding='utf-8'))
            self.assertEqual(actual, json.loads(json.dumps(expected)))

    def test_horary_scope_and_chart_parity(self):
        payload = self.submit(5, question=QUESTION, moment=MOMENT)
        expected = horary.assess(self.engine.get_ephemeris(), QUESTION, 'advice-intent', MOMENT['local'],
                                 SITE['zone'], SITE['latitude'], SITE['longitude'])
        self.parity(payload, expected)
        self.assertEqual(payload['result']['classification'], 'indeterminate')
        self.assertFalse(payload['result']['judgment_certified'])
        self.assertNotIn('reference', payload)

    def test_ingresses_and_planetary_cycle_parity(self):
        engine = self.engine.get_ephemeris()
        site = (SITE['zone'], SITE['latitude'], SITE['longitude'])
        self.parity(self.submit(6, cycle='ingresses', year=2026, site=SITE),
                    mundane.ingresses(engine, 2026, *site))
        start, end = (datetime(y, 1, 1, tzinfo=timezone.utc) for y in (2020, 2021))
        self.parity(self.submit(6, cycle='conjunctions', year=2020, site=SITE),
                    mundane.conjunctions(engine, start, end, *site))

    def test_angular_lines_and_compass_parity(self):
        mapped = self.submit(7, moment=MOMENT)
        self.parity(mapped, astrocartography.generate(self.engine.get_ephemeris(),
            MOMENT['local'], SITE['zone'], SITE['latitude'], SITE['longitude'],
            bodies=list(astrocartography.BODIES)))
        self.assertEqual(len(mapped['result']['geojson']['features']), 40)
        args = dict(bearing=975, uncertainty=2, north='magnetic', role='door')
        compass = self.submit(40, **args)
        self.parity(compass, feng_shui.read(compass_request(CompassInput(oracle=40, **args))))
        heading = compass['result']['readings'][0]
        self.assertTrue(heading['uncertainty_crosses_boundary'])
        self.assertIsNone(heading['declination_conversion'])
        self.assertEqual(compass['references'], heading['possible_mountain_ids'])

    def test_private_and_unsupported_inputs_are_rejected(self):
        for payload in (
            dict(oracle=9, selection='forehead', photo='x'),
            dict(oracle=10, selection='frontis-frontal/9', person='x'),
            dict(oracle=13, selection='ascending', writing_sample='x'),
            dict(oracle=15, selection='right-stomach', symptoms='x'),
            dict(oracle=8, selection='head.curvature.very_sloping'),
            dict(oracle=5, question=QUESTION, moment=dict(MOMENT, zone='Acting/Unknown')),
            dict(oracle=7, moment=dict(MOMENT, local='2024-10-27T01:30')),
            dict(oracle=7, moment=dict(MOMENT, local='2024-10-27T01:30', fold=True)),
            dict(oracle=40, bearing=975.5, uncertainty=0, north='true', role='door'),
        ):
            with self.subTest(payload=payload):
                self.assertEqual(self.client.post('/api/sky-manuscript', json=payload).status_code, 422)
