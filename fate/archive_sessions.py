"""Session-only owner/observer workflows for the two native blind ledgers."""

import base64
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
import secrets
from tempfile import TemporaryDirectory
from threading import RLock
from typing import Literal

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, Field, StrictInt

from future import prophetic_dreams as dreams, remote_viewing as remote
from .futures import ROOT


class VaultInput(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid')
    action: Literal['remote_start','remote_lock','remote_status','judge_open','judge_rank',
                    'dream_start','dream_lock','dream_observe','dream_finish','dream_status','discard']
    code: str | None = Field(default=None, pattern=r'^[A-Za-z0-9_-]{40,55}$')
    text: str | None = Field(default=None, max_length=3000)
    at: str | None = Field(default=None, pattern=r'^\d{4}-\d\d-\d\dT\d\d:\d\d(?::\d\d)?Z$')
    ranks: list[StrictInt] | None = Field(default=None, min_length=5, max_length=5)
    days: Literal[1,3,7] = 1
    rating: Literal['match','nonmatch','insufficient_information'] | None = None
    consent: bool = False
    known: bool = False


@dataclass
class Session:
    kind: str
    owner: str
    expires: float
    ledger: dict
    phase: str
    judge_code: str | None = None
    judge: str | None = None
    evidence: str | None = None


TOKEN = secrets.token_urlsafe
COOKIE = 'fate_archive_client'
PATH = '/api/archive-session'


class ArchiveSessions:
    def __init__(self, clock):
        self.clock = clock
        self.lock = RLock()
        self.sessions = {}
        self.invites = {}

    def now(self):
        return datetime.fromtimestamp(self.clock(), timezone.utc)

    def discard(self, code):
        entry = self.sessions.pop(code)
        if entry.judge_code:
            self.invites.pop(entry.judge_code, None)

    def pause(self, entry, engine, action, actor, payload=None, root=ROOT):
        events = entry.ledger['events']
        last = events[-1]['at'] if events else entry.ledger['plan']['created_at']
        stamp = max(self.now(), engine.timestamp(last) + timedelta(microseconds=1)).isoformat()
        if action == 'lock_entry':
            payload = dict(entry_id=payload['id'], digest=dreams.original_lock(payload,stamp))
        trial = engine.apply(entry.ledger, action, actor, stamp, payload or {}, root=root)
        if not trial['events'][-1]['accepted']:
            raise ValueError(trial['events'][-1]['error'])
        entry.ledger = trial

    def start_remote(self, owner):
        candidates = []
        for i in range(1,6):
            path = f'fate/data/sealed-targets-v1/plate-{i}.png'
            data = (ROOT / path).read_bytes()
            candidates.append(dict(id=f'plate-{i}',path=path,sha256=remote.bytes_hash(data),
                provenance='Original FATE geometric teaching plate v1',
                rights=dict(basis='permission',holder='FATE project',permission='Use and include in this blind study',
                            attribution='FATE original procedural art')))
        cue = 'cue-' + secrets.token_hex(8)
        plan = dict(schema_version=1,profile=remote.PROFILE,profile_sha256=remote.PROFILE_HASH,
            experiment_id='experiment-' + secrets.token_hex(8),trial_ids=[cue],trial_id=cue,
            origin='human',mode='blind_evaluation',tasker='server',viewer='viewer',monitor=None,judges=['judge'],
            knowledge=dict(tasker='aware',viewer='unaware',monitor='absent',judges='unaware'),
            separation='transferred_packets',assignment_policy='os_uniform',
            presentation_order=secrets.SystemRandom().sample(range(5),5),primary_endpoint='actual_target_rank',
            tie_policy='reject',stopping_rule='fixed_trial_ids',exclusion_rule='retain_all_attempts',
            reuse_policy='declare_dependence',created_at=self.now().isoformat(),
            pool=dict(id='fate-plates-v1',version=1,candidates=candidates))
        entry = Session('remote', owner, self.clock()+3600, remote.create(plan), 'viewing')
        self.pause(entry,remote,'commit','server')
        self.pause(entry,remote,'start','viewer')
        return entry, remote.viewer_packet(entry.ledger)

    def start_dream(self, owner, q):
        now = self.now()
        start = (now + timedelta(microseconds=1)).isoformat()
        deadline = (now + timedelta(minutes=20)).isoformat()
        end = (now + timedelta(days=q.days)).isoformat()
        universe = dict(id='nominated-event',version=1,event_ids=['nomination'],
            collector='collector',collection_rule='One expressly nominated observed event following the locked dream.',
            collection_window=dict(start=start, end=(now+timedelta(days=q.days+1)).isoformat()))
        plan = dict(schema_version=1,profile=dreams.PROFILE,profile_sha256=dreams.PROFILE_HASH,
            study_id='archive-' + secrets.token_hex(8),participant='dreamer',coordinator='coordinator',
            origin='human',created_at=now.isoformat(),slots=[dict(id='today',open_at=start,due_at=deadline)],
            universe=universe,universe_sha256=dreams.digest(universe),window=dict(start=start,end=end,boundary='closed',endpoint='occurrence'),
            features=[dict(id='declared-feature',description=q.text)],judges=['self-rater'],
            blinding='descriptive_unblinded',privacy_consent=True,**dict(dreams.DATA['plan_constants']))
        return Session('dream',owner,self.clock()+86400*(q.days+1),dreams.create(plan),'writing')

    def dream_status(self, entry):
        plan = entry.ledger['plan']
        view = dict(phase=entry.phase, due=plan['slots'][0]['due_at'], window=plan['window'],
                    planHash=entry.ledger['plan_sha256'], feature=plan['features'][0]['description'])
        lock = next((row for row in entry.ledger['events'] if row['action']=='lock_entry'), None)
        if lock:
            view['originalLock'] = lock['payload']['digest']
            view['lockedAt'] = lock['at']
        view['ratingAvailable'] = entry.phase == 'observed' and self.now() > dreams.timestamp(view['due'])
        return view

    def collect_dream(self, entry, q):
        prior = self.dream_status(entry)
        when = dreams.timestamp(q.at)
        if when <= dreams.timestamp(prior['lockedAt']) or when > self.now() or when > dreams.timestamp(prior['window']['end']):
            raise ValueError('Declare an event that already occurred after the original lock and inside the comparison window.')
        with TemporaryDirectory(prefix='fate-dream-') as name:
            root = Path(name)
            data = q.text.encode()
            (root / 'observation.txt').write_bytes(data)
            payload = dict(id='nomination',universe_id='nominated-event',universe_version=1,dedup_group='nomination',
                text=q.text,occurrence=dict(start=q.at,end=q.at,precision='reported_interval'),
                publication_at=None,discovery_at=None,common=False,coverage='complete',conflicts=[],
                evidence=dict(path='observation.txt',sha256=dreams.bytes_hash(data),holder='visitor',
                    permission='Self-authored note provided for this comparison',provenance='Visitor’s declared observation'))
            self.pause(entry,dreams,'event','collector',dict(event=payload),root)
        entry.evidence, entry.phase = q.text, 'observed'

    def finish_dream(self, entry, rating):
        if not self.dream_status(entry)['ratingAvailable']:
            raise ValueError('Wait for the recorded slot to close before rating the collected observation.')
        with TemporaryDirectory(prefix='fate-dream-') as name:
            root = Path(name)
            (root/'observation.txt').write_text(entry.evidence,encoding='utf-8',newline='')
            self.pause(entry,dreams,'seal','coordinator',root=root)
            self.pause(entry,dreams,'expose','coordinator',dict(judge_id='self-rater',knowledge='aware'),root)
            ratings = {row['pair_id']: rating for row in dreams.pairs(entry.ledger,root)}
            self.pause(entry,dreams,'rate','self-rater',dict(ratings=ratings,notes='Visitor self-rating.'),root)
            self.pause(entry,dreams,'lock_judges','coordinator',dict(digest=dreams.judge_lock(entry.ledger)),root)
            self.pause(entry,dreams,'reveal','coordinator',root=root)
            self.pause(entry,dreams,'finish','coordinator',root=root)
        entry.phase = 'reported'

    def remote_status(self, entry):
        status = remote.report(entry.ledger)
        if entry.phase == 'revealed':
            plate = next(item for item in entry.ledger['plan']['pool']['candidates'] if item['id']==status['actual_target_id'])
            return dict(phase=entry.phase,result=status,image=base64.b64encode((ROOT/plate['path']).read_bytes()).decode())
        return dict(phase=entry.phase,commitment=status['commitment'],cue=status['cue'],
                    invite=entry.judge_code if entry.phase=='judging' else None)

    def handle(self, q, owner):
        with self.lock:
            return self._handle(q,owner)

    def _handle(self, q, owner):
        for code, entry in list(self.sessions.items()):
            if self.clock() >= entry.expires:
                self.discard(code)
        action = q.action
        if action in ('remote_start','dream_start'):
            if not q.consent:
                raise ValueError('Explicit processing consent is required.')
            if len(self.sessions) >= 64 or sum(s.owner==owner for s in self.sessions.values()) >= 3:
                raise HTTPException(429,'The archive is full. Close an active session before starting another.')
            if action=='remote_start':
                entry, packet = self.start_remote(owner)
                data = dict(phase=entry.phase,packet=packet)
            else:
                if not q.text or not q.text.strip():
                    raise ValueError('Declare the comparison feature before opening a slot.')
                entry = self.start_dream(owner,q)
                data = self.dream_status(entry)
            code = TOKEN(32)
            self.sessions[code] = entry
            return dict(data,code=code)
        judge_action = action.startswith('judge_')
        code = self.invites.get(q.code) if judge_action else q.code
        entry = self.sessions.get(code)
        if not entry or (not judge_action and entry.owner != owner):
            raise HTTPException(404,'This private session is unavailable.')
        if judge_action:
            if entry.owner==owner or (entry.judge is not None and entry.judge!=owner):
                raise HTTPException(403,'The judge requires a separate browser profile or device.')
            if entry.phase != 'judging':
                raise HTTPException(409,'This invite has already been used.')
            if action=='judge_open':
                entry.judge = owner
                return dict(phase=entry.phase,packet=remote.judge_packet(entry.ledger,'judge'))
            if entry.judge!=owner or not q.ranks or sorted(q.ranks)!=list(range(1,6)):
                raise ValueError('Open the judge packet and rank all five candidates once.')
            self.pause(entry,remote,'rank','judge',dict(ranks=dict(zip(remote.ALIASES,q.ranks)),report='Judge submitted one strict rank order.'))
            self.pause(entry,remote,'lock_judge','server',dict(digest=remote.lock_digest(entry.ledger,'judge')))
            self.pause(entry,remote,'reveal','server',dict(preimage=remote.preimage(entry.ledger)))
            self.pause(entry,remote,'report','server')
            entry.phase = 'revealed'
            return self.remote_status(entry)
        if action=='discard':
            self.discard(code)
            return dict(phase='discarded')
        if entry.kind=='remote':
            if action=='remote_lock' and entry.phase=='viewing' and q.text and q.text.strip() and q.consent:
                self.pause(entry,remote,'entry','viewer',dict(text=q.text,stage=None,attachments=[]))
                self.pause(entry,remote,'lock_viewer','viewer',dict(digest=remote.lock_digest(entry.ledger,'viewer')))
                self.pause(entry,remote,'start_judge','server')
                entry.judge_code = TOKEN(32)
                self.invites[entry.judge_code] = code
                entry.phase = 'judging'
            elif action!='remote_status':
                raise ValueError('The blind session cannot move to that step.')
            return self.remote_status(entry)
        if action=='dream_lock' and entry.phase=='writing' and q.text and q.text.strip() and q.consent:
            if self.now() > dreams.timestamp(entry.ledger['plan']['slots'][0]['due_at']):
                raise ValueError('The predeclared recording slot has closed.')
            start = dreams.timestamp(entry.ledger['plan']['slots'][0]['open_at'])
            first = max(self.now(),start)
            if first > self.now():
                raise ValueError('The recording slot is opening. Try again shortly.')
            dream = dict(id='original',slot_id='today',participant='dreamer',occurrence=None,
                first_record_at=first.isoformat(),text=q.text,details={},outcome_known=q.known,attachments=[],
                privacy_consent=True,witness='none')
            self.pause(entry,dreams,'record','dreamer',dict(entry=dream))
            self.pause(entry,dreams,'lock_entry','dreamer',dream)
            entry.phase = 'awaiting'
        elif action=='dream_observe' and entry.phase=='awaiting' and q.at and q.text and q.text.strip() and q.consent:
            self.collect_dream(entry,q)
        elif action=='dream_finish' and entry.phase=='observed' and q.rating:
            self.finish_dream(entry,q.rating)
        elif action!='dream_status':
            raise ValueError('Follow the open diary step.')
        status = self.dream_status(entry)
        if entry.phase=='reported':
            with TemporaryDirectory(prefix='fate-dream-') as name:
                root = Path(name)
                (root/'observation.txt').write_text(entry.evidence,encoding='utf-8',newline='')
                status['result'] = dreams.report(entry.ledger,root)
        return status
