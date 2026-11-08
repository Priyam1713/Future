"""Explicit SQLite migrations and atomic, idempotent local writes."""
import json, os, sqlite3, threading, uuid
from contextlib import contextmanager
from pathlib import Path
from datetime import datetime, timezone
from future.lab.common import digest

LOCK = threading.RLock()
def now(): return datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00','Z')
def uid(): return str(uuid.uuid4())
def dumps(v): return json.dumps(v, ensure_ascii=False, allow_nan=False, separators=(',',':'))

class Store:
    def __init__(self, directory=None):
        self.home=Path(directory or os.environ.get('FUTURE_WORKBENCH_HOME',Path.home()/'.future-workbench')).resolve()
        self.home.mkdir(parents=True,exist_ok=True)
        self.path=self.home/'workbench.sqlite3'
        with self.connect() as db:
            db.execute('PRAGMA journal_mode=WAL')
            db.execute('CREATE TABLE IF NOT EXISTS migrations(version INTEGER PRIMARY KEY, applied_at TEXT NOT NULL)')
            if not db.execute('SELECT 1 FROM migrations WHERE version=1').fetchone():
                db.executescript('''
                CREATE TABLE records(id TEXT PRIMARY KEY, kind TEXT NOT NULL, parent TEXT, created_at TEXT NOT NULL, body TEXT NOT NULL);
                CREATE INDEX records_kind ON records(kind);
                CREATE INDEX records_parent ON records(parent);
                CREATE TABLE secrets(id TEXT PRIMARY KEY REFERENCES records(id) ON DELETE CASCADE, body TEXT NOT NULL);
                CREATE TABLE receipts(key TEXT PRIMARY KEY, request_hash TEXT NOT NULL, response TEXT NOT NULL);
                ''')
                db.execute('INSERT INTO migrations VALUES(1,?)',(now(),))
    @contextmanager
    def connect(self):
        db=sqlite3.connect(self.path,timeout=60); db.row_factory=sqlite3.Row
        db.execute('PRAGMA foreign_keys=ON'); db.execute('PRAGMA secure_delete=ON')
        try:
            with db:yield db
        finally:db.close()
    @contextmanager
    def transaction(self):
        with LOCK, self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            yield db
    def get(self,db,id,kind=None):
        row=db.execute('SELECT body FROM records WHERE id=?',(id,)).fetchone()
        if not row: raise ValueError('Record not found')
        v=json.loads(row[0])
        if kind and v['kind']!=kind: raise ValueError('Incorrect record kind')
        return v
    def rows(self,db,kind=None):
        rows=db.execute('SELECT body FROM records WHERE kind=? ORDER BY created_at DESC',(kind,)) if kind else db.execute('SELECT body FROM records ORDER BY created_at DESC')
        return [json.loads(r[0]) for r in rows]
    def put(self,db,v):
        db.execute('INSERT INTO records VALUES(?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET body=excluded.body,parent=excluded.parent',(v['id'],v['kind'],v.get('parent'),v['created_at'],dumps(v)))
        return v
    def new(self,db,kind,body,parent=None):
        return self.put(db,dict(body,id=uid(),kind=kind,parent=parent,created_at=now()))
    def write(self,key,payload,fn):
        if not isinstance(key,str) or not 8<=len(key)<=200: raise ValueError('An Idempotency-Key of 8–200 characters is required')
        h=digest(payload)
        with self.transaction() as db:
            previous=db.execute('SELECT * FROM receipts WHERE key=?',(key,)).fetchone()
            if previous:
                if previous['request_hash']!=h: raise ValueError('Idempotency key conflicts with a different request')
                return json.loads(previous['response'])
            result=fn(db)
            # Receipts must not duplicate participant data or hidden answers. Store only record IDs.
            db.execute('INSERT INTO receipts VALUES(?,?,?)',(key,h,dumps(result)))
            return result
