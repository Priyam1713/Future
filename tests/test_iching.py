import copy
import hashlib
import itertools
import json
from pathlib import Path
import tempfile
import unittest
from future import iching as i
from future import iching_cast as casting
from future import iching_catalog as catalog
from future.knowledge import Registry

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = json.loads((ROOT/'tests/fixtures/iching_structure_reference.json').read_text(encoding='utf-8'))
BASE = dict(schema_version=1, profile=i.PROFILE, reading_policy=i.POLICY, task='symbolic_reading',
    mode='manual', method='manual', line_order='bottom_to_top', lines=[6,7,8,9,7,8])


def seeded(method='three-coin', seed='Future-IChing-v1'):
    return {k:v for k,v in BASE.items() if k!='lines'} | dict(mode='seeded',method=method,seed=seed,protocol=casting.PROTOCOL)


class IChingTests(unittest.TestCase):
    def test_all_64_independent_diagrams(self):
        seen=set()
        for n,pattern in enumerate(REFERENCE['patterns_by_king_wen'],1):
            h=catalog.hexagram(n)
            self.assertEqual(''.join(map(str,h['pattern_bottom_to_top'])),pattern)
            self.assertEqual(h['number'],n);seen.add(pattern)
        self.assertEqual(seen,{''.join(p) for p in itertools.product('01',repeat=6)})

    def test_all_eight_trigrams(self):
        aliases={'111':'Qian','000':'Kun','100':'Zhen','010':'Kan','001':'Gen','110':'Dui','101':'Li','011':'Xun'}
        self.assertEqual(set(catalog.TRIGRAMS),set(aliases))
        for pattern,name in aliases.items():self.assertEqual(catalog.TRIGRAMS[pattern]['alias'],name)
        for h in catalog.HEXAGRAMS.values():
            p=''.join(map(str,h['pattern_bottom_to_top']))
            self.assertEqual(h['lower_trigram'],catalog.TRIGRAMS[p[:3]]['id'])
            self.assertEqual(h['upper_trigram'],catalog.TRIGRAMS[p[3:]]['id'])

    def test_exhaustive_4096_cast_states(self):
        # Independent membership arithmetic;no production state table used for expectations.
        numbers={s:n for n,s in enumerate(REFERENCE['patterns_by_king_wen'],1)}
        for values in itertools.product((6,7,8,9),repeat=6):
            before=''.join('1' if v in (7,9) else '0' for v in values)
            after=''.join('1' if v in (6,7) else '0' for v in values)
            moving=[n for n,v in enumerate(values,1) if v in (6,9)]
            r=i.transform(values)
            self.assertEqual(r['initial']['number'],numbers[before])
            self.assertEqual(r['resulting']['number'],numbers[after])
            self.assertEqual(r['moving_lines'],moving)
            self.assertEqual([x['moving'] for x in r['trace']],[v%3==0 for v in values])
            self.assertEqual(r['change_mask'],sum(2**(p-1) for p in moving))

    def test_exhaustive_64_by_64_masks_and_inverse(self):
        lookup={p:n for n,p in enumerate(REFERENCE['patterns_by_king_wen'],1)}
        values={(0,False):8,(1,False):7,(0,True):6,(1,True):9}
        for number,pattern in enumerate(REFERENCE['patterns_by_king_wen'],1):
            for mask in range(64):
                change=f'{mask:06b}'[::-1]
                target=''.join(str((int(p)+int(m))%2) for p,m in zip(pattern,change))
                expected=[values[int(p),m=='1'] for p,m in zip(pattern,change)]
                supplied=i.values_for(list(map(int,pattern)),mask)
                self.assertEqual(supplied,expected)
                result=i.transform(supplied)
                self.assertEqual(result['initial']['number'],number)
                self.assertEqual(result['resulting']['number'],lookup[target])
                self.assertEqual(result['change_mask'],mask)

    def test_coin_enumeration_exact(self):
        counts={v:0 for v in range(6,10)}
        for bits in itertools.product((0,1),repeat=3):counts[casting.coin_line(bits)]+=1
        self.assertEqual(counts,{6:1,7:3,8:3,9:1})
        self.assertEqual(casting.coin_line([0,0,0]),6)
        self.assertEqual(casting.coin_line([1,1,1]),9)

    def test_yarrow_enumeration_exact_and_assumptions(self):
        counts={v:0 for v in range(6,10)}
        for index in range(16):counts[casting.yarrow_value(index)]+=1
        self.assertEqual(counts,{6:1,7:5,8:7,9:3})
        # Independent enumeration of conventional residue classes:first1/4 vs3/4,then halves.
        sums=[(2 if a==0 else 3)+(2 if b==0 else 3)+(2 if c==0 else 3)
              for a in range(4) for b in range(2) for c in range(2)]
        self.assertEqual({v:sums.count(v) for v in range(6,10)},counts)
        r=i.read(seeded('yarrow-marginal'))
        self.assertTrue(r['probabilities']['conventional_residue_assumptions'])
        self.assertFalse(r['probabilities']['physical_stalk_simulation'])

    def test_independent_dotnet_vectors(self):
        vs=json.loads((ROOT/'tests/fixtures/iching_seed_vectors.json').read_text(encoding='utf-8'))['vectors']
        self.assertEqual(len(vs),14)
        self.assertEqual(len({(v['seed'],v['method']) for v in vs}),14)
        for v in vs:
            lines,trace=casting.cast(v['seed'],v['method'])
            self.assertEqual(lines,v['lines']);self.assertEqual(trace['raw'],v['raw'])
            stream=casting.CastingStream(v['seed'],v['method'])
            self.assertEqual(hashlib.sha256(stream.prefix+bytes(8)).hexdigest(),v['first_block'])
            self.assertEqual(trace['words_used'],18 if v['method']=='three-coin' else 6)

    def test_source_text_coverage_and_polarities(self):
        ids=[]
        for h in catalog.HEXAGRAMS.values():
            self.assertEqual(len(h['lines']),6)
            for position,text in enumerate([h['judgment'],*h['lines']]):
                self.assertTrue(text['text'] and text['locator'] and text['pdf_pages'])
                self.assertEqual(text['source_id'],catalog.DATA['source']['id']);ids.append(text['rule_id'])
                if position:
                    self.assertIn('undivided' if h['pattern_bottom_to_top'][position-1] else 'divided',text['text'][:125])
        self.assertEqual(len(ids),448);self.assertEqual(len(set(ids)),448)

    def test_independent_source_examples(self):
        f=json.loads((ROOT/'tests/fixtures/iching_source_examples.json').read_text(encoding='utf-8'))
        for c in f['cases']:
            h=catalog.hexagram(c['number'])
            text=h['judgment'] if c['part']=='judgment' else h['special_all_changing'] if c['part']=='special' else h['lines'][c['part']-1]
            for phrase in c['contains']:self.assertIn(phrase,text['text'])
            self.assertIn(c['page']+36,text['pdf_pages'])
        example=f['published_transformation'];r=i.transform([9]*6)
        self.assertEqual((r['initial']['number'],r['resulting']['number']),(example['initial'],example['result']))

    def test_known_manual_transformations(self):
        for c in REFERENCE['examples']:
            r=i.transform(c['lines'])
            self.assertEqual(r['initial']['number'],c['initial'])
            self.assertEqual(r['resulting']['number'],c['result'])

    def test_zero_one_multiple_all_moving(self):
        for values,count in [([7]*6,0),([9,7,7,7,7,7],1),([6,7,8,9,7,8],2),([9]*6,6)]:
            r=i.read(BASE|dict(lines=values))
            self.assertEqual(len(r['changing_line_texts']),count)
            self.assertEqual([t['position'] for t in r['changing_line_texts']],r['calculation']['moving_lines'])
            self.assertEqual(r['summary']['coverage'],'compositional')
            self.assertFalse(r['factual_prediction'])

    def test_specials_append_without_suppressing_six_lines(self):
        for values,number in [([9]*6,1),([6]*6,2)]:
            r=i.read(BASE|dict(lines=values))
            self.assertEqual(r['special_all_changing']['rule_id'],f'iching.legge1882.{number:02d}.special')
            self.assertEqual(len(r['changing_line_texts']),6)
        self.assertIsNone(i.read(BASE|dict(lines=[9,7,7,7,7,7]))['special_all_changing'])
        self.assertIsNone(i.read(BASE|dict(lines=[6,9,6,9,6,9]))['special_all_changing'])

    def test_hexagram64_dispute_not_rewritten(self):
        r=i.read(BASE|dict(lines=[8,7,6,7,8,7]))
        self.assertEqual(r['calculation']['initial']['number'],64)
        self.assertIn('But there will be advantage',r['changing_line_texts'][0]['text'])
        self.assertIn('not advantageous',r['variants'][0]['text'])
        self.assertFalse(r['variants'][0]['automatic_reconciliation'])

    def test_bottom_up_diagram_and_trigrams(self):
        r=i.transform([7,7,7,8,8,8])['initial']
        self.assertEqual(r['number'],11)
        self.assertEqual(r['diagram_top_to_bottom'],['--- ---']*3+['-------']*3)
        self.assertEqual([t['id'] for t in r['trigrams']],['heaven','earth'])

    def test_manual_has_no_seed_probability_metadata(self):
        r=i.read(BASE)
        self.assertIsNone(r['probabilities']);self.assertIsNone(r['replay']['protocol'])
        self.assertNotIn('seed',r['replay']['casting'])

    def test_invalid_lines_masks_patterns(self):
        for v in [[],[6]*5,[6]*7,[True]*6,[6.0]*6,[5]*6,[10]*6,'678978',None]:
            with self.assertRaises(ValueError):i.transform(v)
        for mask in [-1,64,True,1.0,'0']:
            with self.assertRaises(ValueError):i.values_for([0]*6,mask)
        for p in [[False]*6,[2]*6,[0]*5,None]:
            with self.assertRaises(ValueError):i.values_for(p,0)
        for n in [0,65,True,'1',None]:
            with self.assertRaises(ValueError):catalog.hexagram(n)

    def test_invalid_modes_methods_profiles(self):
        bad=[BASE|dict(schema_version=True),BASE|dict(profile='Wilhelm'),BASE|dict(reading_policy='priority_line'),
             BASE|dict(line_order='top_to_bottom'),BASE|dict(method='three-coin'),BASE|dict(seed='x'),
             BASE|dict(mode='auto'),BASE|dict(task='prediction'),BASE|dict(photo='x'),
             seeded()|dict(method='physical-yarrow'),seeded()|dict(method=[]),seeded()|dict(lines=[7]*6),
             seeded()|dict(protocol='future-cards-sha256-fy-v1'),BASE|dict(question='\n'),BASE|dict(question='\ud800')]
        for request in bad:
            with self.assertRaises(ValueError):i.read(request)

    def test_seed_and_serialization_boundaries(self):
        for seed in ['',None,1,'x'*257,'é'*129,'\ud800']:
            with self.assertRaises(ValueError):i.read(seeded(seed=seed))
        for seed in ['x','x'*256,'é'*128,'\0',' seed ']:self.assertEqual(i.read(seeded(seed=seed))['replay']['casting']['seed'],seed)
        self.assertNotEqual(casting.cast('Café','three-coin'),casting.cast('Cafe\u0301','three-coin'))

    def test_protocol_domain_isolation_and_counter(self):
        from future.card_random import Stream
        a=casting.CastingStream('x','three-coin');b=casting.CastingStream('x','yarrow-marginal')
        self.assertNotEqual(a.word(),b.word())
        self.assertNotEqual(casting.CastingStream('x','three-coin').word(),Stream('x','deck').word())
        a.pending=[];a.counter=1<<64
        with self.assertRaises(ValueError):a.word()
        with self.assertRaises(ValueError):casting.CastingStream('x','deck')

    def test_coin_and_yarrow_invalid_bits(self):
        for b in [[0,0],[0,0,2],[True,0,1],None]:
            with self.assertRaises(ValueError):casting.coin_line(b)
        for v in [-1,16,True,1.0]:
            with self.assertRaises(ValueError):casting.yarrow_value(v)

    def test_exact_json_markdown_replay_and_escaping(self):
        for request in [BASE,seeded(),seeded('yarrow-marginal')]:
            r=i.read(request|dict(question='<script>|reflection'))
            self.assertEqual(i.read(json.loads(json.dumps(r))['replay']['request']),r)
            md=i.markdown(r);replay=json.loads(md.split('```json\n')[1].split('\n```')[0])
            self.assertEqual(i.read(replay['request']),r)
            self.assertEqual(md,i.markdown(r));self.assertIn('&lt;script&gt;',md)

    def test_immutable_catalog_and_request(self):
        with self.assertRaises(TypeError):catalog.HEXAGRAMS['1']['number']=2
        h=catalog.hexagram(1);h['judgment']['text']='changed'
        self.assertNotEqual(catalog.hexagram(1)['judgment']['text'],'changed')
        value=copy.deepcopy(BASE);r=i.read(value);value['lines'][0]=7
        self.assertEqual(r['replay']['request'],BASE)

    def test_portable_catalog_hash(self):
        path=ROOT/'knowledge/iching_legge1882_v1.json';text=path.read_text(encoding='utf-8')
        self.assertEqual(catalog.digest(json.loads(text)),catalog.digest(json.loads(text.replace('\n','\r\n'))))
        self.assertEqual(catalog.digest(json.loads(text)),catalog.CATALOG_DIGEST)

    def test_strict_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp,'input.json')
            for text in ['{"seed":"a","seed":"b"}','{"seed":NaN}','{"seed":Infinity}']:
                p.write_text(text,encoding='utf-8')
                with self.assertRaises(ValueError):i.load_input(p)
            p.write_text(json.dumps(BASE),encoding='utf-8-sig');self.assertEqual(i.load_input(p),BASE)

    def test_registry_source_isolation(self):
        registry=Registry()
        try:
            i.read(BASE,registry);catalog.register_knowledge(registry)
            self.assertEqual(registry.db.execute('select count(*) from rules').fetchone()[0],450)
            self.assertEqual(registry.select_rules(18,'Mei Hua Yi Shu','Wilhelm'),[])
        finally:registry.close()


if __name__=='__main__':unittest.main()
