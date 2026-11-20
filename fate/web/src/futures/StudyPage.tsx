import { useEffect, useRef, useState } from "react";
import { api } from "../types";
import { chapterFor } from "../codex/records";
import type { Oracle } from "../hooks/useOracle";
import { ResultLeaf } from "../components/ResultLeaf";
import { ArtifactSurface } from "../components/ArtifactSurface";
import { labReadout } from "./labPresentation";
import { CONTROLS } from "./controls";
import { Instrument, Scrubber } from "./Instruments";
import {
  edition,
  index,
  ROOMS,
  type Source,
  type Study,
  type StudyId,
  type Readout,
  type FutureBookmark,
} from "./contracts";
import { savedStudy } from "./reference";

export function download(name: string, body: object) {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(body, null, 2)], { type: "application/json" }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = name + ".json";
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export function Sources({
  sources,
  notes = [],
}: {
  sources: Source[];
  notes?: string[];
}) {
  return (
    <details className="lab-depth">
      <summary>Sources and method</summary>
      {notes.map((note, i) => (
        <p key={i}>{note}</p>
      ))}
      <ul>
        {sources.map((source) => (
          <li key={source.id}>
            {source.url.startsWith("https://") ||
            source.url.startsWith("http://") ? (
              <a href={source.url} target="_blank" rel="noreferrer">
                {source.title}
              </a>
            ) : (
              source.title
            )}
            {source.locator && <small>{source.locator}</small>}
          </li>
        ))}
      </ul>
    </details>
  );
}

export function FutureChapter({
  s,
  compact = false,
}: {
  s: FutureBookmark;
  compact?: boolean;
}) {
  const { view, sources } = savedStudy(s);
  const name = ROOMS[s.oracle][1];
  if (compact)
    return (
      <div className="future-bookmark future-bookmark-mini">
        <span aria-hidden="true">{s.oracle >= 49 ? "⊙" : "◇"}</span>
        <strong>{view.title}</strong>
      </div>
    );
  return (
    <section className="future-bookmark">
      <header className="folio-heading">
        <p className="eyebrow">{name} · Public study</p>
        <h2 tabIndex={-1}>{view.title}</h2>
      </header>
      <p>{view.lead}</p>
      <Sources sources={sources} />
    </section>
  );
}

export function Payoff({ view }: { view: Readout }) {
  return (
    <ResultLeaf status={view.status} title={view.title}>
      <p className="future-lead">{view.lead}</p>
    </ResultLeaf>
  );
}

function StudyActions({
  data,
  option,
  oracle,
  customSeed,
}: {
  data: Study;
  option: number;
  oracle: Oracle;
  customSeed: boolean;
}) {
  const chapter =
    !data.private && !customSeed
      ? chapterFor(data.result, {
          oracle: data.oracle,
          profile: edition,
          option,
        })
      : null;
  const saved =
    chapter && oracle.codex.chapters.some((c) => c.id === chapter.id);
  const [error, setError] = useState(false);
  return (
    <div className="future-actions">
      {chapter &&
        (saved ? (
          <button
            className="text-button"
            onClick={() => {
              oracle.codex.setSelectedId(chapter.id);
              oracle.navigate("codex");
            }}
          >
            Open in My Fate →
          </button>
        ) : (
          <button
            className="secondary"
            onClick={() => setError(!oracle.codex.save(chapter))}
          >
            Save public study to this device
          </button>
        ))}
      {!(data.oracle === 46 && data.private) && (
        <details className="lab-depth">
          <summary>Native result and privacy</summary>
          <p>
            {data.private
              ? "The native download includes your words."
              : "A bookmark contains the public study setting and source edition."}
          </p>
          <button
            className="secondary"
            onClick={() =>
              download("fate-" + ROOMS[data.oracle][0] + "-native", data.result)
            }
          >
            Export native result
          </button>
        </details>
      )}
      {error && <p role="alert">My Fate could not save this study.</p>}
    </div>
  );
}

const memoryLabels = [
  "Leave details open",
  "Specific dream and recalled time",
  "Familiarity without a specific episode",
  "Present dream-like state",
];

export function StudyPage({
  id,
  oracle,
  demoOnly = false,
}: {
  id: StudyId;
  oracle: Oracle;
  demoOnly?: boolean;
}) {
  const [option, setOption] = useState(index[id].default);
  const [data, setData] = useState<Study>();
  const [seed, setSeed] = useState<number[] | null>(null);
  const [shownOption, setShownOption] = useState(option);
  const [customSeed, setCustomSeed] = useState(false);
  const [text, setText] = useState("");
  const [memory, setMemory] = useState(0);
  const [consent, setConsent] = useState(false);
  const [journal, setJournal] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const controller = useRef<AbortController | null>(null);
  const model = id >= 49;
  const canWrite = id === 24 || id === 26 || id === 46;
  const control = CONTROLS[id];
  const kind = ROOMS[id][3];
  const polished = id === 50 || id === 58 || id === 59;
  async function run(selected: number, personal = false) {
    if (controller.current) return;
    const c = new AbortController();
    controller.current = c;
    setBusy(true);
    setError("");
    try {
      const response = await api<Study>(
        "/api/future-study",
        {
          oracle: id,
          option: selected,
          ...(seed ? { cells: seed } : {}),
          ...(personal ? { text, consent } : {}),
        },
        c.signal,
      );
      if (c.signal.aborted) return;
      setData(response);
      setShownOption(selected);
      setCustomSeed(Boolean(seed));
      setSeed(null);
      oracle.markExplored(id);
      if (personal) oracle.sound.cue("reveal");
    } catch (e) {
      if (!c.signal.aborted) setError((e as Error).message);
    } finally {
      if (!c.signal.aborted) {
        controller.current = null;
        setBusy(false);
      }
    }
  }
  useEffect(() => {
    if (model) void run(option);
    return () => controller.current?.abort();
    // One explicit public preset is loaded for each remounted lab.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  return (
    <div className={`future-work future-work-${kind}`}>
      <section
        className="future-apparatus"
        aria-label={ROOMS[id][2] + " instrument"}
        aria-busy={busy}
      >
        <ArtifactSurface
          still={!polished || oracle.reduced || oracle.paused}
          className={polished ? "laboratory-surface" : ""}
        >
          <Instrument
            key={data && !polished ? data.view.title + "-" + shownOption : kind}
            kind={kind}
            data={data?.view.instrument}
            seed={seed}
            setSeed={setSeed}
            setting={shownOption}
          />
        </ArtifactSurface>
        {control && (
          <div className="apparatus-controls">
            {control.choices ? (
              <div
                className="lab-picks"
                role="group"
                aria-label={control.label}
              >
                {control.choices.map((choice, n) => (
                  <button
                    type="button"
                    key={choice}
                    className="tactile"
                    disabled={busy}
                    aria-pressed={option === n}
                    onClick={() => {
                      if (polished) oracle.sound.cue("select");
                      setOption(n);
                      if (id !== 26 || !journal) void run(n);
                    }}
                  >
                    {choice}
                  </button>
                ))}
              </div>
            ) : (
              <Scrubber
                value={option}
                max={control.max ?? 0}
                onChange={setOption}
                label={control.label}
                caption={control.map?.(option)}
              />
            )}
            {control.max !== undefined && (
              <button
                className="primary tactile"
                disabled={busy}
                onClick={() => {
                  if (polished) oracle.sound.cue("select");
                  void run(option);
                }}
              >
                {control.commit}
              </button>
            )}
          </div>
        )}
        {!model && !data && (
          <button
            className="primary"
            disabled={busy}
            onClick={() => void run(option)}
          >
            Open the example
          </button>
        )}
        {busy && (
          <p role="status" className="instrument-note">
            Computing native result…
          </p>
        )}
      </section>
      <div className="future-reading" aria-live="polite">
        {data ? (
          <>
            <div
              className={
                polished
                  ? `lab-payoff lab-payoff-${kind} artifact-arrival`
                  : undefined
              }
              key={polished ? shownOption : undefined}
            >
              <Payoff view={labReadout(data)} />
            </div>
            <Sources
              sources={data.sources}
              notes={
                polished
                  ? [data.view.lead, ...(data.view.instrument.notes ?? [])]
                  : data.view.instrument.notes
              }
            />
            <StudyActions
              key={`${shownOption}-${data.private}-${customSeed}`}
              data={data}
              option={shownOption}
              oracle={oracle}
              customSeed={customSeed}
            />
          </>
        ) : (
          <>
            <p className="eyebrow">
              {model ? "Native instrument" : "The Dream Archive"}
            </p>
            <h2>{ROOMS[id][2]}</h2>
            {demoOnly && (
              <p>
                Open a clearly labeled synthetic ledger to examine its locked
                entries and event chronology.
              </p>
            )}
          </>
        )}
        {canWrite && (
          <details
            className="lab-depth private-entry"
            open={journal}
            onToggle={(e) => setJournal(e.currentTarget.open)}
          >
            <summary>
              {id === 24
                ? "Write your own page"
                : id === 46
                  ? "Annotate a recollection"
                  : "Add a reflective question"}
            </summary>
            <label>
              {id === 24
                ? "Your draft"
                : id === 46
                  ? "Your recollection"
                  : "Your question"}
              <textarea
                rows={4}
                maxLength={4000}
                value={text}
                onChange={(e) => setText(e.target.value)}
                disabled={busy}
              />
            </label>
            {id === 46 && (
              <label>
                Describe what you recall
                <select
                  value={memory}
                  onChange={(e) => setMemory(Number(e.target.value))}
                >
                  {memoryLabels.map((label, i) => (
                    <option key={label} value={i}>
                      {label}
                    </option>
                  ))}
                </select>
              </label>
            )}
            <label className="future-check">
              <input
                type="checkbox"
                checked={consent}
                onChange={(e) => setConsent(e.target.checked)}
              />
              Process my words for this visit
            </label>
            <button
              className="primary"
              onClick={() => void run(id === 46 ? memory : option, true)}
              disabled={busy || !text.trim() || !consent}
            >
              {id === 24
                ? "Read my draft"
                : id === 46
                  ? "Annotate this recollection"
                  : "Open the selected reference"}
            </button>
          </details>
        )}
        {error && <p role="alert">{error}</p>}
      </div>
    </div>
  );
}
