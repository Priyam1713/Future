"""Immutable source-specific24-mark identity/account catalog; no casting or randomness."""
import unicodedata
from pathlib import Path
from .scrying import freeze,thaw,digest,load_input,_raw

ROOT=Path(__file__).resolve().parents[1]
PROFILE='opsopaus-greek-alphabet-manual-lot-v1'
PROFILE_HASH='c88e527692c1e5bd4a127bffbab087294e9de4e57d2ed50a70732698fb6ec33d'
DATA=freeze(load_input(ROOT/'knowledge/cleromancy_profile_v1.json'))
CATALOG_HASH=DATA['catalog_sha256']

def normalize(value):
    if not _raw(value,80):raise ValueError('Mark must be bounded valid UTF8 text, not a number/list or invalid Unicode')
    stripped=value.strip(' \t\r\n');nfc=unicodedata.normalize('NFC',stripped)
    if not nfc:raise ValueError('Empty mark rejected')
    key=nfc.lower() if nfc.isascii() else nfc
    return dict(raw=value,trimmed=stripped,nfc=nfc,alias_key=key,policy='NFC; ASCII trim/case only; explicit Greek glyph table; no NFKC or confusable folding')

def alias_index(catalog):
    ids=set(catalog['source_order']);result={}
    for alias,identifier in catalog['aliases'].items():
        key=normalize(alias)['alias_key']
        if identifier not in ids:raise ValueError('Alias points to an unknown mark')
        if key in result and result[key]!=identifier:raise ValueError('Ambiguous normalized alias in catalog')
        result[key]=identifier
    return result

def assets():
    p=load_input(ROOT/'knowledge/cleromancy_profile_v1.json')
    if digest(p)!=PROFILE_HASH:raise ValueError('Pinned Cleromancy profile integrity mismatch; unknown edition')
    c=load_input(ROOT/'knowledge/cleromancy_catalog_v1.json')
    if digest(c)!=CATALOG_HASH:raise ValueError('Pinned Cleromancy catalog hash mismatch; changed order/meaning/aliases require new profile')
    ids=[r['id'] for r in c['marks']]
    if len(ids)!=24 or len(set(ids))!=24 or c['source_order']!=ids or [r['order'] for r in c['marks']]!=list(range(1,25)):raise ValueError('Complete24-record source order required')
    alias_index(c)
    return p,c

def identify(value):
    _,c=assets();trace=normalize(value);identifier=alias_index(c).get(trace['alias_key'])
    if identifier is None:raise ValueError('Unknown or ambiguous mark; use a canonical gao-ID, verified Latin name or exact Greek glyph; no confusable fallback')
    trace['canonical_id']=identifier
    return trace

def lookup(value):
    _,c=assets();trace=identify(value);record=next(r for r in c['marks'] if r['id']==trace['canonical_id'])
    return dict(record=record,normalization=trace)

def catalog():return assets()[1]['marks']

def integrity():
    p,c=assets()
    return dict(verified=True,profile_sha256=PROFILE_HASH,catalog_sha256=CATALOG_HASH,source_record_sha256=p['source_record_sha256'],source_html_sha256=p['source_html_sha256'],marks=24,aliases=len(c['aliases']))
