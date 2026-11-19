import type { Result } from "../types";
import type { NumberResult } from "../experiences/contracts";
import { DECK } from "../artwork/registry";

export const STORAGE_KEY = "fate.codex.v1";
export const REFERENCE = "fate-codex-reference-v1";
export const MAX_CHAPTERS = 50;
const MAX_LENGTH = 65536;
export type Snapshot =
  | {
      oracle: 16;
      profile: "waite-1922-text-v1";
      spread: "one" | "three";
      cards: { id: string; orientation: "upright" | "reversed" }[];
    }
  | {
      oracle: 4;
      profile: "decoz-component-reduction";
      expression: number;
      personalYear: number;
      lifePath: number;
    };
export interface Chapter {
  id: string;
  savedAt: string;
  reference: typeof REFERENCE;
  snapshot: Snapshot;
}
export interface CodexDocument {
  schemaVersion: 1;
  chapters: Chapter[];
}
export interface StoragePort {
  getItem(key: string): string | null;
  setItem(key: string, value: string): void;
  removeItem(key: string): void;
}
function object(value: unknown): value is Record<string, unknown> {
  return !!value && typeof value === "object" && !Array.isArray(value);
}
function keys(value: Record<string, unknown>, expected: string[]) {
  return (
    Object.keys(value).length === expected.length &&
    expected.every((k) => Object.hasOwn(value, k))
  );
}
function core(value: unknown) {
  return (
    Number.isInteger(value) &&
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 22, 33] as unknown[]).includes(value)
  );
}
export function validSnapshot(s: unknown): s is Snapshot {
  if (!object(s)) return false;
  if (s.oracle === 16) {
    if (
      !keys(s, ["oracle", "profile", "spread", "cards"]) ||
      s.profile !== "waite-1922-text-v1" ||
      !Array.isArray(s.cards) ||
      !["one", "three"].includes(String(s.spread)) ||
      s.cards.length !== (s.spread === "one" ? 1 : 3)
    )
      return false;
    return (
      new Set(s.cards.map((c) => (object(c) ? c.id : null))).size ===
        s.cards.length &&
      s.cards.every(
        (c) =>
          object(c) &&
          keys(c, ["id", "orientation"]) &&
          typeof c.id === "string" &&
          Object.hasOwn(DECK.cards, c.id) &&
          ["upright", "reversed"].includes(String(c.orientation)),
      )
    );
  }
  return (
    s.oracle === 4 &&
    keys(s, ["oracle", "profile", "expression", "personalYear", "lifePath"]) &&
    s.profile === "decoz-component-reduction" &&
    core(s.expression) &&
    core(s.lifePath) &&
    Number.isInteger(s.personalYear) &&
    Number(s.personalYear) >= 1 &&
    Number(s.personalYear) <= 9
  );
}
export function validChapter(c: unknown): c is Chapter {
  return (
    object(c) &&
    keys(c, ["id", "savedAt", "reference", "snapshot"]) &&
    typeof c.id === "string" &&
    /^[a-f0-9-]{36}$/.test(c.id) &&
    typeof c.savedAt === "string" &&
    /^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z$/.test(c.savedAt) &&
    Number.isFinite(Date.parse(c.savedAt)) &&
    c.reference === REFERENCE &&
    validSnapshot(c.snapshot)
  );
}
export function parseDocument(raw: string | null): CodexDocument {
  if (raw === null) return { schemaVersion: 1, chapters: [] };
  if (raw.length > MAX_LENGTH)
    throw new Error(
      "This Codex exceeds this edition’s safe reading limit. The stored record has been left untouched.",
    );
  let value: unknown;
  try {
    value = JSON.parse(raw);
  } catch {
    throw new Error(
      "This device’s Codex could not be read. Its stored record has been left untouched.",
    );
  }
  if (!object(value) || value.schemaVersion !== 1)
    throw new Error(
      "This Codex uses an unavailable version. Its stored record has been left untouched.",
    );
  if (
    !keys(value, ["schemaVersion", "chapters"]) ||
    !Array.isArray(value.chapters) ||
    value.chapters.length > MAX_CHAPTERS ||
    !value.chapters.every(validChapter) ||
    new Set(value.chapters.map((c) => c.id)).size !== value.chapters.length
  )
    throw new Error(
      "This Codex contains an unrecognized chapter. Its stored record has been left untouched.",
    );
  return value as unknown as CodexDocument;
}
export function readDocument(storage: StoragePort) {
  return parseDocument(storage.getItem(STORAGE_KEY));
}
export function saveChapter(
  storage: StoragePort,
  chapter: Chapter,
): CodexDocument {
  if (!validChapter(chapter))
    throw new Error(
      "This reading cannot be saved in the current Codex edition.",
    );
  const document = readDocument(storage);
  if (document.chapters.some((c) => c.id === chapter.id)) return document;
  if (document.chapters.length >= MAX_CHAPTERS)
    throw new Error(
      "This edition holds 50 chapters. Export your Codex, then delete a chapter to make room.",
    );
  const next: CodexDocument = {
    schemaVersion: 1,
    chapters: [...document.chapters, chapter],
  };
  const encoded = JSON.stringify(next);
  if (encoded.length > MAX_LENGTH)
    throw new Error("This Codex is full. Export it before making room.");
  storage.setItem(STORAGE_KEY, encoded);
  return next;
}
export function deleteChapter(storage: StoragePort, id: string): CodexDocument {
  const current = readDocument(storage);
  const next: CodexDocument = {
    schemaVersion: 1,
    chapters: current.chapters.filter((c) => c.id !== id),
  };
  if (next.chapters.length) storage.setItem(STORAGE_KEY, JSON.stringify(next));
  else storage.removeItem(STORAGE_KEY);
  return next;
}
export function tarotSnapshot(result: Result): Snapshot {
  return {
    oracle: 16,
    profile: result.profile as "waite-1922-text-v1",
    spread: result.spread as "one" | "three",
    cards: result.readings.map((r) => ({
      id: r.card.id,
      orientation: r.orientation,
    })),
  };
}
export function numberSnapshot(result: NumberResult): Snapshot {
  return {
    oracle: 4,
    profile: result.profile as "decoz-component-reduction",
    expression: result.expression.result!,
    personalYear: result.cycles.year.result!,
    lifePath: result.life_path.result!,
  };
}
const identities = new WeakMap<object, string>();
export function chapterFor(native: object, snapshot: Snapshot): Chapter {
  let id = identities.get(native);
  if (!id) {
    id = crypto.randomUUID();
    identities.set(native, id);
  }
  return {
    id,
    savedAt: new Date().toISOString(),
    reference: REFERENCE,
    snapshot,
  };
}
