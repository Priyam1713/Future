import { useEffect, useRef, useState } from "react";
import { BirthForm } from "../astrology/BirthForm";
import type { WesternInput } from "../astrology/contracts";
import { chapterFor } from "../codex/records";
import type { Oracle } from "../hooks/useOracle";
import { api } from "../types";
import {
  ROOMS,
  type ChamberEnvelope,
  type ChamberId,
  type ChamberSnapshot,
} from "./contracts";
import { chamberEvidence, chapterName } from "./reference";
import { JadePillars, Sources, VedicDial } from "./ChartInstruments";
import { Coins, Stones } from "./CastInstruments";

export function Instrument({
  snapshot,
  envelope,
  compact,
  oracle,
  complete,
}: {
  snapshot: ChamberSnapshot;
  envelope?: ChamberEnvelope;
  compact?: boolean;
  oracle?: Oracle;
  complete?: () => void;
}) {
  const cue = () => oracle?.sound.cue("reveal");
  switch (snapshot.oracle) {
    case 2:
      return (
        <>
          <VedicDial s={snapshot} compact={compact} live={!!envelope} />
          {!compact && (
            <Sources
              rows={chamberEvidence(snapshot)}
              title="Sidereal, Navamsa and Vimshottari sources"
            />
          )}
        </>
      );
    case 3:
      return <JadePillars s={snapshot} compact={compact} />;
    case 18:
      return (
        <Coins
          s={snapshot}
          cast={envelope?.result.replay?.casting?.raw}
          compact={compact}
          cue={cue}
          complete={complete}
        />
      );
    case 19:
      return (
        <Stones
          s={snapshot}
          drawing={!!envelope}
          compact={compact}
          cue={cue}
          complete={complete}
        />
      );
  }
}

function download(data: object, name: string) {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(data, null, 2)], { type: "application/json" }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = name;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function Save({
  envelope,
  oracle,
}: {
  envelope: ChamberEnvelope;
  oracle: Oracle;
}) {
  const chapter = chapterFor(envelope.result, envelope.snapshot);
  const saved = oracle.codex.chapters.some((c) => c.id === chapter.id);
  const [error, setError] = useState("");
  return (
    <section className="chamber-save">
      <h3>Keep this chapter</h3>
      <p>
        Save a small, unencrypted record on this device.{" "}
        {envelope.snapshot.oracle === 2
          ? "The chart and UTC period boundary days remain personal. The raw birth details and selected timing date are excluded."
          : envelope.snapshot.oracle === 3
            ? "The four pillar identifiers are personal. The original birth details are excluded."
            : "This keeps only the selected symbols and their order."}{" "}
        Replay seeds and Gemini commentary are excluded.
      </p>
      {error && <p role="alert">{error}</p>}
      <button
        className="secondary"
        disabled={saved}
        onClick={() => {
          if (!oracle.codex.save(chapter))
            setError(
              "My Fate could not write this chapter. Check browser storage or export a copy.",
            );
          else setError("");
        }}
      >
        {saved ? "Saved to this device" : "Save chamber chapter to this device"}
      </button>
      {saved && (
        <button
          className="text-button"
          onClick={() => {
            oracle.codex.setSelectedId(chapter.id);
            oracle.navigate("codex");
          }}
        >
          Open in My Fate →
        </button>
      )}
    </section>
  );
}

type Comment = { themes: { id: string; reflection: string }[] };
function Commentary({ draw, receipt }: { draw: object; receipt: string }) {
  const [checked, setChecked] = useState(false),
    [busy, setBusy] = useState(false);
  const [result, setResult] = useState<Comment | null>(null),
    [error, setError] = useState("");
  const pending = useRef<AbortController | null>(null);
  useEffect(() => () => pending.current?.abort(), []);
  async function ask() {
    if (!checked || pending.current) return;
    const controller = new AbortController();
    pending.current = controller;
    setBusy(true);
    setError("");
    try {
      const reply = await api<Comment>(
        "/api/chambers/explain",
        { draw, receipt, cloud_consent: true },
        controller.signal,
      );
      if (!controller.signal.aborted) setResult(reply);
    } catch (e) {
      if (!controller.signal.aborted)
        setError(e instanceof Error ? e.message : "Commentary is unavailable.");
    } finally {
      if (!controller.signal.aborted) setBusy(false);
      if (pending.current === controller) pending.current = null;
    }
  }
  return (
    <details className="chamber-depth">
      <summary>Optional Gemini reflection</summary>
      <p>
        Gemini receives the selected symbolic excerpts. Provider commentary is
        separate from the reading and isn’t saved.
      </p>
      <label>
        <input
          type="checkbox"
          checked={checked}
          onChange={(e) => setChecked(e.target.checked)}
        />{" "}
        Send these source excerpts to Gemini.
      </label>
      <button className="secondary" disabled={!checked || busy} onClick={ask}>
        {busy ? "Requesting…" : "Request commentary"}
      </button>
      {error && <p role="alert">{error}</p>}
      {result && (
        <section aria-label="AI commentary">
          <p className="eyebrow">AI commentary</p>
          {result.themes.map((row) => (
            <p key={row.id}>{row.reflection}</p>
          ))}
        </section>
      )}
    </details>
  );
}

export default function ChamberScreen({
  id,
  oracle,
}: {
  id: ChamberId;
  oracle: Oracle;
}) {
  const room = ROOMS[id];
  const [spread, setSpread] = useState<"one" | "three">("three");
  const [target, setTarget] = useState(() =>
    new Date().toISOString().slice(0, 10),
  );
  const [year, setYear] = useState("pvr-2000-savana"),
    [profile, setProfile] = useState("civil-zi23");
  const [envelope, setEnvelope] = useState<ChamberEnvelope | null>(null);
  const [request, setRequest] = useState<object | null>(null);
  const [finished, setFinished] = useState(false),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  const current = useRef<AbortController | null>(null);
  const seed = useRef(crypto.randomUUID());
  const artifact = useRef<HTMLElement>(null);
  const [visible, setVisible] = useState(false),
    [hidden, setHidden] = useState(document.hidden);
  useEffect(() => () => current.current?.abort(), []);
  useEffect(() => {
    const update = () => setHidden(document.hidden);
    document.addEventListener("visibilitychange", update);
    return () => document.removeEventListener("visibilitychange", update);
  }, []);
  useEffect(() => {
    if (!envelope || !artifact.current) return;
    const ob = new IntersectionObserver(([entry]) =>
      setVisible(entry.isIntersecting),
    );
    ob.observe(artifact.current);
    artifact.current.focus({ preventScroll: true });
    artifact.current.scrollIntoView({ block: "start", behavior: "instant" });
    return () => ob.disconnect();
  }, [envelope]);
  const complete = () => {
    setFinished(true);
    oracle.markExplored(id);
  };
  async function begin(draw: object) {
    if (current.current) return;
    const controller = new AbortController();
    current.current = controller;
    setBusy(true);
    setError("");
    try {
      const data = await api<ChamberEnvelope>(
        "/api/chambers",
        draw,
        controller.signal,
      );
      if (controller.signal.aborted) return;
      setEnvelope(data);
      setRequest(draw);
      if (id === 2 || id === 3) complete();
    } catch (e) {
      if (!controller.signal.aborted)
        setError(
          e instanceof Error
            ? e.message
            : "The chamber couldn’t open. Try again.",
        );
    } finally {
      if (!controller.signal.aborted) setBusy(false);
      if (current.current === controller) current.current = null;
    }
  }
  function birth({ houses: _houses, ...q }: WesternInput) {
    void begin(
      id === 2
        ? { ...q, oracle: id, target, year_key: year }
        : { ...q, oracle: id, profile },
    );
  }
  function reset() {
    seed.current = crypto.randomUUID();
    setFinished(false);
    setEnvelope(null);
    setRequest(null);
    requestAnimationFrame(() => {
      oracle.heading.current?.focus({ preventScroll: true });
      window.scrollTo({ top: 0, behavior: "instant" });
    });
  }
  const still =
    oracle.paused ||
    oracle.reduced ||
    hidden ||
    !visible ||
    navigator.hardwareConcurrency <= 2 ||
    ((navigator as Navigator & { deviceMemory?: number }).deviceMemory ?? 8) <=
      2;
  return (
    <div
      className={"chamber-room page-enter chamber-" + room.slug}
      data-motion={still ? "still" : "active"}
    >
      <header className="chamber-hero">
        <picture>
          <source
            media="(max-width: 620px)"
            srcSet={"/art/chamber-" + room.slug + "-720.webp"}
          />
          <img
            src={"/art/chamber-" + room.slug + "-1440.webp"}
            alt=""
            width="1440"
            height="960"
            fetchPriority="high"
          />
        </picture>
        <div className="chamber-intro">
          <button
            className="text-button"
            onClick={() => oracle.navigate("gallery")}
          >
            ← Oracle Gallery
          </button>
          <p className="eyebrow">
            {room.name} · {room.index}
          </p>
          <h1 ref={oracle.heading} tabIndex={-1}>
            {room.title}
          </h1>
          <p>{room.prompt}</p>
        </div>
      </header>
      {!envelope &&
        (id === 2 || id === 3 ? (
          <BirthForm
            chamber={room.slug as "vedic" | "bazi"}
            onSubmit={birth}
            busy={busy}
            error={error}
          >
            <fieldset className="chamber-options">
              <legend>
                {id === 2 ? "Vimshottari timing" : "BaZi clock convention"}
              </legend>
              {id === 2 ? (
                <>
                  <label>
                    Explore periods on this UTC day
                    <input
                      type="date"
                      required
                      value={target}
                      onChange={(e) => setTarget(e.target.value)}
                    />
                  </label>
                  <label>
                    Year convention
                    <select
                      value={year}
                      onChange={(e) => setYear(e.target.value)}
                    >
                      <option value="pvr-2000-savana">
                        360-day savana year
                      </option>
                      <option value="solar-365.2425">365.2425-day year</option>
                    </select>
                  </label>
                  <p>
                    Uses midnight UTC. The target must be after birth and within
                    120 selected years.
                  </p>
                </>
              ) : (
                <label>
                  Clock convention
                  <select
                    value={profile}
                    onChange={(e) => setProfile(e.target.value)}
                  >
                    <option value="civil-zi23">
                      Civil time · day changes at 23:00
                    </option>
                    <option value="civil-split-zi">
                      Civil time · split late Zi hour
                    </option>
                    <option value="standard-zi23">
                      Standard time · day changes at 23:00
                    </option>
                  </select>
                </label>
              )}
            </fieldset>
          </BirthForm>
        ) : (
          <section className="chamber-start">
            <div className="artifact-preview" aria-hidden="true" />
            <div>
              <h2>
                {id === 18
                  ? "Let the first line fall."
                  : "Choose how many stones to turn."}
              </h2>
              {id === 19 && (
                <div
                  className="chamber-switch"
                  role="group"
                  aria-label="Rune spread"
                >
                  <button
                    aria-pressed={spread === "one"}
                    onClick={() => setSpread("one")}
                  >
                    One rune
                  </button>
                  <button
                    aria-pressed={spread === "three"}
                    onClick={() => setSpread("three")}
                  >
                    Three runes
                  </button>
                </div>
              )}
              <p>
                {id === 18
                  ? "Six digital casts, each with three coins. You can turn each line at your own pace."
                  : "One focus, or a three-stone layout for situation, challenge and reflection."}
              </p>
              <button
                className="primary"
                disabled={busy}
                onClick={() =>
                  begin(
                    id === 18
                      ? { oracle: id, seed: seed.current }
                      : { oracle: id, seed: seed.current, spread },
                  )
                }
              >
                {busy
                  ? "Preparing…"
                  : id === 18
                    ? "Begin the six-line cast"
                    : "Draw the runestones"}
              </button>
              {error && (
                <p className="birth-error" role="alert">
                  {error}
                </p>
              )}
            </div>
          </section>
        ))}
      {envelope && (
        <section
          className="chamber-result"
          ref={artifact}
          tabIndex={-1}
          aria-label={room.name + " instrument"}
        >
          <Instrument
            snapshot={envelope.snapshot}
            envelope={envelope}
            oracle={oracle}
            complete={complete}
          />
          {finished && (
            <>
              <Save envelope={envelope} oracle={oracle} />
              {oracle.gemini && request && (
                <Commentary draw={request} receipt={envelope.receipt} />
              )}
              <details className="chamber-depth">
                <summary>Calculation, conventions & export</summary>
                <p>
                  {envelope.snapshot.profile}. The full native export includes
                  the original request or birth details.
                </p>
                <button
                  className="secondary"
                  onClick={() =>
                    download(
                      envelope.result,
                      "fate-" + room.slug + "-native.json",
                    )
                  }
                >
                  Export full native reading
                </button>
              </details>
            </>
          )}
          <button className="text-button chamber-reset" onClick={reset}>
            ↶ Start a fresh {id === 18 ? "cast" : id === 19 ? "draw" : "chart"}
          </button>
        </section>
      )}
    </div>
  );
}

export function ChamberChapter({
  s,
  index,
}: {
  s: ChamberSnapshot;
  index: number;
}) {
  return (
    <div
      className={"chamber-folio chamber-" + ROOMS[s.oracle].slug}
      data-motion="still"
    >
      <header className="folio-heading">
        <p className="eyebrow">
          CHAPTER {String(index + 1).padStart(2, "0")} · {ROOMS[s.oracle].name}
        </p>
        <h2 tabIndex={-1}>{chapterName(s)}</h2>
      </header>
      <div className="chamber-result">
        <Instrument snapshot={s} />
      </div>
    </div>
  );
}
