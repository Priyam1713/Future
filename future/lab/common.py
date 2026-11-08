"""Shared bounded Lab metadata and exact arithmetic; no forecasting engine here."""
import hashlib,json,re
from datetime import datetime,timezone
from fractions import Fraction
from pathlib import Path
from ..remote_viewing import digest,obj,integer,identifier
from ..scrying import load_input
ROOT=Path(__file__).resolve().parents[2]
PROFILE_HASH='5b8b09b98f1f3a46a24db9fc6b334e7ea776f7e03d6646e2e05fa8907e95a3a3'
REGISTRY_HASH='2b2c0a4f372b8861b1471b50acc2313b6cc2882293273c2924a84aac3a0ccf2d'
class LabError(ValueError):pass
class IntegrityError(LabError):pass
def profile():
    p=load_input(ROOT/'knowledge/future_lab_profile_v2.json')
    if digest(p)!=PROFILE_HASH or p['registry_sha256']!=REGISTRY_HASH:raise IntegrityError('Lab profile identity mismatch')
    return p
def fields(value,name):obj(value,profile()['schema'][name])
def nonempty(value,limit=4000):
    if not isinstance(value,str) or not value.strip() or len(value)>limit:raise LabError('Nonempty bounded text required')
    return value
def sequence(value,limit):
    if not isinstance(value,list) or len(value)>limit:raise LabError('Bounded list required')
    return value
def at(value):
    if not isinstance(value,str) or re.fullmatch(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,6})?Z',value) is None:raise LabError('UTC-Z timestamp required')
    return datetime.fromisoformat(value.replace('Z','+00:00')).astimezone(timezone.utc)
def checked(value):
    if max(value.numerator.bit_length(),value.denominator.bit_length())>8192:raise LabError('Exact Fraction bit limit exceeded')
    return value
def rational(value):
    if not isinstance(value,str) or len(value)>5002 or re.fullmatch(r'-?(?:0|[1-9][0-9]{0,2499})(?:/[1-9][0-9]{0,2499}|\.[0-9]{1,2500})?',value) is None:raise LabError('Finite bounded rational string required')
    return checked(Fraction(value))
def snapshot(value):
    nonempty(value['attribution']);nonempty(value['snapshot'],64000)
    if value['rights'] not in ['self_authored','public_domain','permission_granted']:raise LabError('Explicit data rights required')
    if value['snapshot_sha256']!=hashlib.sha256(value['snapshot'].encode('utf-8')).hexdigest():raise IntegrityError('Data/source snapshot hash mismatch')
def bounded_json(value):
    if len(json.dumps(value,ensure_ascii=False,allow_nan=False).encode('utf-8'))>2097152:raise LabError('Lab input exceeds2MiB')
def code_sha(path):return hashlib.sha256((ROOT/path).read_bytes().replace(b'\r\n',b'\n')).hexdigest()
