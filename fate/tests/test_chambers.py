import json
from datetime import datetime, timezone
from unittest import TestCase

from fastapi.testclient import TestClient

from fate.api import create_app
from fate.build_chambers import build, OUT
from fate.chambers import GRAHAS, PILLARS
from fate.western import ROOT
from future import chinese, chinese_readings, iching, runes, vedic, vedic_timing
from future.iching_cast import PROTOCOL as COINS
from future.natal import SkyfieldEphemeris

BIRTH = dict(local='1990-07-15T14:30:00', zone='Europe/London', latitude=51.50853, longitude=-0.12574, fold=None)
TARGET = '2026-11-20'
SEED = 'fate-block06-parity-v1'


class ChambersTest(TestCase):
    def setUp(self):
        self.client = TestClient(create_app())
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)

    def chamber(self, request):
        response = self.client.post('/api/chambers', json=request)
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()

    def test_native_d1_d9_dasha(self):
        envelope = self.chamber(dict(BIRTH, oracle=2, target=TARGET))
        engine = SkyfieldEphemeris(ROOT/'data/de440s.bsp')
        try:
            native = vedic_timing.enrich(vedic.d1(engine, *BIRTH.values()), datetime.fromisoformat(TARGET).replace(tzinfo=timezone.utc), include_d9=True)
            self.assertEqual(envelope['result'], json.loads(json.dumps(native)))
        finally:
            engine.kernel.close()
        s = envelope['snapshot']
        self.assertEqual(set(s), {'oracle', 'profile', 'asc', 'd9Asc', 'planets', 'mansion', 'year', 'main', 'sub', 'active'})
        self.assertEqual([p[0] for p in s['planets']], [native['planets'][name]['longitude'] for name in GRAHAS])
        self.assertEqual([p[3] for p in s['planets']], [native['d9']['planets'][name]['longitude_symbolic'] for name in GRAHAS])
        self.assertEqual(s['sub'][s['active']][0], native['vimshottari']['current']['antardasha']['lord'])
        self.assertEqual(s['main'][0][1], native['vimshottari']['current']['mahadasa']['start_inclusive_utc'][:10])

    def test_native_bazi_pillars_and_component_readings(self):
        envelope = self.chamber(dict(BIRTH, oracle=3, profile='standard-zi23'))
        engine = SkyfieldEphemeris(ROOT/'data/de440s.bsp')
        try:
            native = chinese_readings.enrich(chinese.chart(engine, *BIRTH.values(), 'standard-zi23'))
            self.assertEqual(envelope['result'], json.loads(json.dumps(native)))
        finally:
            engine.kernel.close()
        self.assertEqual(envelope['snapshot'], dict(oracle=3, profile='standard-zi23',
            pairs=[native['pillars'][name]['sexagenary_index'] for name in PILLARS]))

    def test_native_seeded_coins_and_change_rules(self):
        envelope = self.chamber(dict(oracle=18, seed=SEED))
        native = iching.read(dict(schema_version=1, profile=iching.PROFILE, reading_policy=iching.POLICY,
            task='symbolic_reading', mode='seeded', method='three-coin', line_order='bottom_to_top', protocol=COINS, seed=SEED))
        self.assertEqual(envelope['result'], native)
        self.assertEqual(envelope['snapshot'], dict(oracle=18, profile=iching.PROFILE,
            values=native['calculation']['values'], figures=[native['calculation'][key]['number'] for key in ('initial', 'resulting')]))

    def test_native_seeded_runes_both_spreads(self):
        for spread in ('one', 'three'):
            envelope = self.chamber(dict(oracle=19, seed=SEED, spread=spread))
            native = runes.read(dict(schema_version=1, task='symbolic_reading', mode='seeded', seed=SEED,
                profile=runes.PROFILE, protocol=runes.PROTOCOL, orientation_policy='upright_only', spread=spread))
            self.assertEqual(envelope['result'], native)
            self.assertEqual(envelope['snapshot'], dict(oracle=19, profile=runes.PROFILE,
                runes=[row['rune_id'] for row in native['replay']['selected']]))

    def test_missing_time_convention_domain_and_extra_data_rejected(self):
        for request in (
            dict(BIRTH, oracle=2, target=TARGET, local='1990-07-15'),
            dict(BIRTH, oracle=2, target=TARGET, latitude=66),
            dict(BIRTH, oracle=2, target='1900-01-01'),
            dict(BIRTH, oracle=3, local='1890-01-01T12:00'),
            dict(BIRTH, oracle=3, profile='guessed'),
            dict(BIRTH, oracle=3, zone='London'),
            dict(BIRTH, oracle=3, fold=True),
            dict(oracle=18, seed=SEED, question='private'),
            dict(oracle=19, seed=SEED, spread='five'),
        ):
            with self.subTest(request=request):
                self.assertEqual(self.client.post('/api/chambers', json=request).status_code, 422)

    def test_frozen_source_projections(self):
        for name, expected in zip(('edition-v1.json', 'reference-v1.json'), build()):
            self.assertEqual(json.loads((OUT/name).read_text(encoding='utf-8')), expected)

    def test_consent_signed_request_and_provider_data_minimization(self):
        prompts = []
        def generate(prompt):
            prompts.append(prompt)
            payload = json.loads(prompt.split('DATA: ', 1)[1])
            return {'themes': [dict(id=row['id'], reflection='Consider the source wording.') for row in payload]}, {}
        draw = dict(BIRTH, oracle=2, target=TARGET)
        with TestClient(create_app(provider=generate)) as client:
            response = client.post('/api/chambers', json=draw)
            self.assertEqual(response.status_code, 200, response.text)
            request = dict(draw=draw, receipt=response.json()['receipt'])
            self.assertEqual(client.post('/api/chambers/explain', json=dict(request, cloud_consent=False)).status_code, 422)
            tampered = dict(request, draw=dict(draw, target='2026-11-21'), cloud_consent=True)
            self.assertEqual(client.post('/api/chambers/explain', json=tampered).status_code, 403)
            self.assertEqual(prompts, [])
            result = client.post('/api/chambers/explain', json=dict(request, cloud_consent=True))
            self.assertEqual(result.status_code, 200, result.text)
            self.assertEqual(len(prompts), 1)
            for field in (BIRTH['local'], BIRTH['zone'], str(BIRTH['latitude']), TARGET):
                self.assertNotIn(field, prompts[0])
