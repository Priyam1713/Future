"""Versioned, provenance-preserving SQLite registry. No remote model required."""
from dataclasses import dataclass, asdict
import hashlib
import json
from pathlib import Path
import re
import sqlite3


@dataclass(frozen=True)
class Rule:
    id: str
    version: int
    technique_id: int
    variation: str
    tradition: str
    source_id: str
    locator: str
    statement: str
    operation: str
    parameters: dict
    status: str
    evidence_kind: str
    fixture_ids: list[str]

    def __post_init__(self):
        if self.status not in {'proposed', 'verified', 'rejected'}:
            raise ValueError('Invalid verification status')
        if not 1 <= self.technique_id <= 60 or self.version < 1:
            raise ValueError('Invalid technique/version')
        if any(not str(getattr(self, k)).strip() for k in
               ('id', 'variation', 'tradition', 'source_id', 'locator', 'statement', 'operation')):
            raise ValueError('Missing scope or provenance')
        if self.evidence_kind not in {'computational', 'traditional', 'empirical', 'hypothetical'}:
            raise ValueError('Invalid evidence kind')
        if self.status == 'verified' and not self.fixture_ids:
            raise ValueError('Verified rules require fixture references')


class Registry:
    def __init__(self, path=':memory:'):
        self.db = sqlite3.connect(path)
        self.db.row_factory = sqlite3.Row
        self.db.execute('PRAGMA foreign_keys=ON')
        self.db.executescript('''
            CREATE TABLE IF NOT EXISTS sources(id TEXT PRIMARY KEY, record TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS documents(
                id TEXT PRIMARY KEY, source_id TEXT NOT NULL REFERENCES sources(id),
                locator TEXT NOT NULL, digest TEXT NOT NULL, content_kind TEXT NOT NULL, text TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS rules(
                id TEXT NOT NULL, version INTEGER NOT NULL, source_id TEXT NOT NULL REFERENCES sources(id),
                record TEXT NOT NULL, PRIMARY KEY(id,version));
            CREATE VIRTUAL TABLE IF NOT EXISTS document_search USING fts5(id UNINDEXED, text);
        ''')

    def close(self):
        self.db.close()

    def add_source(self, source):
        for key in ('id', 'author', 'edition', 'url', 'ingestion', 'rights_note'):
            if not source.get(key):
                raise ValueError(f'Missing source field: {key}')
        self._immutable('sources', source['id'], json.dumps(source, sort_keys=True))

    def _immutable(self, table, identifier, record):
        # table is internal, never supplied by a caller.
        row = self.db.execute(f'SELECT record FROM {table} WHERE id=?', (identifier,)).fetchone()
        if row and row['record'] != record:
            raise ValueError('Existing record differs; use a new versioned identifier')
        with self.db:
            self.db.execute(f'INSERT OR IGNORE INTO {table} VALUES (?,?)', (identifier, record))

    def ingest_text(self, identifier, source_id, path, locator, *, content_kind):
        source = self.db.execute('SELECT record FROM sources WHERE id=?', (source_id,)).fetchone()
        if source is None:
            raise ValueError('Unknown source')
        policy = json.loads(source['record'])['ingestion']
        allowed = (policy == 'facts_only' and content_kind == 'original_research_notes') or (
            policy in {'public_domain', 'permission_granted'} and content_kind == 'source_text')
        if not allowed:
            raise ValueError('Source policy does not permit this ingestion')
        if not locator.strip():
            raise ValueError('A source locator is required')
        text = Path(path).read_text(encoding='utf-8').strip()
        if not text:
            raise ValueError('Empty document')
        digest = hashlib.sha256(text.encode()).hexdigest()
        values = (identifier, source_id, locator, digest, content_kind, text)
        existing = self.db.execute('SELECT * FROM documents WHERE id=?', (identifier,)).fetchone()
        if existing:
            if tuple(existing) != values:
                raise ValueError('Document changed; use a new versioned identifier')
            return digest
        with self.db:
            self.db.execute('INSERT INTO documents VALUES (?,?,?,?,?,?)', values)
            self.db.execute('INSERT INTO document_search VALUES (?,?)', (identifier, text))
        return digest

    def add_rule(self, rule):
        record = json.dumps(asdict(rule), sort_keys=True)
        row = self.db.execute('SELECT record FROM rules WHERE id=? AND version=?',
                              (rule.id, rule.version)).fetchone()
        if row and row['record'] != record:
            raise ValueError('Rule version is immutable')
        with self.db:
            self.db.execute('INSERT OR IGNORE INTO rules VALUES (?,?,?,?)',
                            (rule.id, rule.version, rule.source_id, record))

    def select_rules(self, technique_id, variation, tradition):
        # No cross-tradition fallbacks. A later proposed/rejected version does not
        # silently replace a previously verified version.
        selected = {}
        for row in self.db.execute('SELECT record FROM rules ORDER BY version'):
            r = json.loads(row['record'])
            if (r['technique_id'], r['variation'], r['tradition'], r['status']) == (
                    technique_id, variation, tradition, 'verified'):
                selected[r['id']] = r
        return list(selected.values())

    def search(self, query, source_ids, limit=5):
        tokens = re.findall(r'\w+', query, re.UNICODE)
        if not tokens or not source_ids:
            return []
        if not 1 <= limit <= 50:
            raise ValueError('limit must be 1..50')
        expression = ' OR '.join('"' + t + '"' for t in tokens)
        placeholders = ','.join('?' for _ in source_ids)
        rows = self.db.execute(f'''
            SELECT d.*, s.record AS source FROM document_search f
            JOIN documents d ON d.id=f.id JOIN sources s ON s.id=d.source_id
            WHERE document_search MATCH ? AND d.source_id IN ({placeholders})
            ORDER BY bm25(document_search), d.id LIMIT ?
        ''', (expression, *source_ids, limit))
        return [dict(r) for r in rows]
