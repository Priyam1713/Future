import { useEffect, useRef, useState } from "react";
import { api } from "../types";
import type { Oracle } from "../hooks/useOracle";
import { ArchiveInstrument } from "./ArchiveInstrument";
import {
  EDITION,
  options,
  ROOMS,
  type ArchiveId,
  type Envelope,
} from "./contracts";
import { ResultActions, ViewCard } from "./Result";

export function ArchiveRoom({ id, oracle }: { id: ArchiveId; oracle: Oracle }) {
  const title = ROOMS[id][1];
  const catalog = options[id];
  const groups = [...new Set(catalog.map(([, group]) => group))];
  const [group, setGroup] = useState(id === 8 ? "" : groups[0]);
  const [entry, setEntry] = useState("");
  const [side, setSide] = useState<"left" | "right" | "">("");
  const [data, setData] = useState<Envelope>();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [query, setQuery] = useState("");
  const pending = useRef<AbortController | null>(null);
  const resultHeading = useRef<HTMLElement>(null);
  useEffect(() => () => pending.current?.abort(), []);
  useEffect(() => {
    if (data) resultHeading.current?.focus({ preventScroll: true });
  }, [data]);
  function pickGroup(next: string) {
    setGroup(next);
    setQuery("");
    setEntry("");
    setData(undefined);
    setError("");
  }
  async function open(key: string) {
    if (pending.current || (id === 8 && !side)) return;
    const c = new AbortController();
    pending.current = c;
    setEntry(key);
    setBusy(true);
    setError("");
    setData(undefined);
    try {
      const output = await api<Envelope>(
        "/api/sky-manuscript",
        { oracle: id, selection: key, ...(id === 8 ? { hand: side } : {}) },
        c.signal,
      );
      if (c.signal.aborted) return;
      setData(output);
      oracle.markExplored(id);
      oracle.sound.cue("reveal");
    } catch (e) {
      if (!c.signal.aborted) setError((e as Error).message);
    } finally {
      if (!c.signal.aborted) {
        pending.current = null;
        setBusy(false);
      }
    }
  }
  const filtered = catalog.filter(([, name, label]) =>
    query
      ? label.toLowerCase().includes(query.trim().toLowerCase())
      : name === group,
  );
  return (
    <div className="folio-work archive-work">
      <ArchiveInstrument
        id={id}
        group={group}
        groups={groups}
        entry={entry}
        side={side}
        onGroup={(next) => {
          if (!busy) pickGroup(next);
        }}
      />
      <div className="folio-desk">
        {data?.view ? (
          <section
            tabIndex={-1}
            ref={resultHeading}
            aria-label={`${title} result`}
          >
            <ViewCard view={data.view} />
            <ResultActions
              result={data.result}
              oracle={oracle}
              name={ROOMS[id][0]}
              snapshot={
                data.reference
                  ? { oracle: id, profile: EDITION, entries: [data.reference] }
                  : undefined
              }
            />
            <button
              className="text-button"
              onClick={() => {
                setData(undefined);
                setEntry("");
              }}
            >
              Browse the index ←
            </button>
          </section>
        ) : (
          <>
            <p className="eyebrow">
              {id === 8 ? "Manual observation" : "Source index"}
            </p>
            <h2>
              {id === 8
                ? group || "Choose a line on the hand"
                : "Open a reference"}
            </h2>
            {id === 8 && group && (
              <div
                className="folio-picks"
                role="group"
                aria-label="Observed hand"
              >
                {(["left", "right"] as const).map((item) => (
                  <button
                    key={item}
                    aria-pressed={item === side}
                    disabled={busy}
                    onClick={() => setSide(item)}
                  >
                    {item === "left" ? "Left hand" : "Right hand"}
                  </button>
                ))}
              </div>
            )}
            {id !== 8 && groups.length > 1 && (
              <div className="folio-index">
                <label>
                  Index section{" "}
                  <select
                    value={group}
                    onChange={(e) => pickGroup(e.target.value)}
                    disabled={busy}
                  >
                    {groups.map((name) => (
                      <option key={name}>{name}</option>
                    ))}
                  </select>
                </label>
                {catalog.length > 12 && (
                  <label>
                    Find an entry{" "}
                    <input
                      type="search"
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      disabled={busy}
                    />
                  </label>
                )}
              </div>
            )}
            {(id !== 8 || side) && (
              <div
                className="folio-picks archive-entries"
                role="group"
                aria-label={id === 8 ? "Line descriptions" : "Source entries"}
              >
                {filtered.map(([key, , label]) => (
                  <button
                    key={key}
                    disabled={busy}
                    onClick={() => void open(key)}
                  >
                    {label}
                  </button>
                ))}
                {!filtered.length && id !== 8 && (
                  <p>No entries match this search.</p>
                )}
              </div>
            )}
            {busy && <p role="status">Opening the source…</p>}
            {error && <p role="alert">{error}</p>}
          </>
        )}
        <details className="folio-depth">
          <summary>About this edition</summary>
          <p>
            {id === 8
              ? "The illustrated lines guide manual choices. The book’s associations are historical and symbolic."
              : "These archival entries document an edition and its terminology. Discredited historical claims are presented here for study, rather than as assessments of people."}
          </p>
        </details>
      </div>
    </div>
  );
}
