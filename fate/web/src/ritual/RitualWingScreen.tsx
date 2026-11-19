import { useCallback, useEffect, useRef, useState } from "react";
import type { Oracle } from "../hooks/useOracle";
import { chapterFor } from "../codex/records";
import { api } from "../types";
import { RITUAL_ROOMS, type RitualEnvelope, type RitualId } from "./contracts";
import { RitualEntry } from "./Entries";
import { RitualReading, SourceDepth } from "./Readings";

const storageText: Record<RitualId, string> = {
  17: "Keep just the selected card IDs in their original order.",
  20: "Keep the symbolic category and whether it came from a digital draw or a manual report.",
  21: "Keep the Crystal Ball guide only. Your observations and session inputs stay outside My Fate.",
  22: "Keep the Mirror Scrying guide only. Your observations and session inputs stay outside My Fate.",
  23: "Keep the selected public motif references. Your dream text and personal context stay outside My Fate.",
  33: "Keep only the shield’s fifteen figures.",
  36: "Keep the pinned passage ID and the selected context radius.",
};
function SaveRitual({
  data,
  oracle,
}: {
  data: RitualEnvelope;
  oracle: Oracle;
}) {
  const chapter = chapterFor(data.result, data.snapshot);
  const saved = oracle.codex.chapters.some((c) => c.id === chapter.id);
  const [error, setError] = useState(false);
  return (
    <section className="ritual-save">
      <div>
        <h3>
          Keep this{" "}
          {data.snapshot.oracle === 21 || data.snapshot.oracle === 22
            ? "guide"
            : "chapter"}
        </h3>
        <p>
          {storageText[data.snapshot.oracle]} This browser stores it locally
          without encryption.
        </p>
      </div>
      <div>
        <button
          className="secondary"
          disabled={saved}
          onClick={() => setError(!oracle.codex.save(chapter))}
        >
          {saved
            ? "Saved to this device"
            : "Save ritual chapter to this device"}
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
        {error && (
          <p role="alert">
            My Fate could not write this chapter. Check browser storage or
            export a copy.
          </p>
        )}
      </div>
    </section>
  );
}

function download(value: object, name: string) {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(value, null, 2)], { type: "application/json" }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = name;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

export default function RitualScreen({
  id,
  oracle,
}: {
  id: RitualId;
  oracle: Oracle;
}) {
  const room = RITUAL_ROOMS[id];
  const [data, setData] = useState<RitualEnvelope | null>(null),
    [busy, setBusy] = useState(false),
    [error, setError] = useState(""),
    [finished, setFinished] = useState(false),
    [revision, setRevision] = useState(0);
  const controller = useRef<AbortController | null>(null),
    resultTarget = useRef<HTMLElement>(null),
    oracleRef = useRef(oracle);
  oracleRef.current = oracle;
  useEffect(() => () => controller.current?.abort(), []);
  useEffect(() => {
    if (!data || !resultTarget.current) return;
    resultTarget.current.focus({ preventScroll: true });
    resultTarget.current.scrollIntoView({
      block: "start",
      behavior: "instant",
    });
  }, [data]);
  const complete = useCallback(() => {
    setFinished(true);
    oracleRef.current.markExplored(id);
  }, [id]);
  async function start(input: object) {
    if (controller.current) return;
    const c = new AbortController();
    controller.current = c;
    setBusy(true);
    setError("");
    try {
      const result = await api<RitualEnvelope>(
        "/api/ritual-wing",
        { oracle: id, input },
        c.signal,
      );
      if (c.signal.aborted) return;
      setData(result);
      if (id !== 17 && id !== 33) complete();
    } catch (err) {
      if (!c.signal.aborted)
        setError(
          err instanceof Error
            ? err.message
            : "This ritual didn’t finish. Try again.",
        );
    } finally {
      if (controller.current === c) controller.current = null;
      if (!c.signal.aborted) setBusy(false);
    }
  }
  function reset() {
    setData(null);
    setFinished(false);
    setRevision((n) => n + 1);
    setError("");
    requestAnimationFrame(() =>
      document
        .querySelector(".ritual-stage")
        ?.scrollIntoView({ block: "start", behavior: "instant" }),
    );
  }
  const still = oracle.paused || oracle.reduced;
  return (
    <div
      className={`ritual-room page-enter ritual-${room.slug}`}
      data-ritual-still={still}
    >
      <header className="ritual-hero">
        <picture>
          <source
            media="(max-width:640px)"
            srcSet={`/art/ritual-${room.slug}-720.webp`}
          />
          <img
            src={`/art/ritual-${room.slug}-1440.webp`}
            width="1440"
            height="960"
            alt=""
            fetchPriority="high"
          />
        </picture>
        <div className="ritual-intro">
          <button
            className="text-button"
            onClick={() => oracle.navigate("gallery")}
          >
            ← Oracle Gallery
          </button>
          <p className="eyebrow">{room.name}</p>
          <h1 tabIndex={-1} ref={oracle.heading}>
            {room.title}
          </h1>
          <p>{room.prompt}</p>
        </div>
      </header>
      {!data ? (
        <section
          className="ritual-stage"
          key={revision}
          aria-label={room.name + " ritual"}
        >
          <RitualEntry id={id} busy={busy} still={still} submit={start} />
          {busy && <p role="status">Opening the reading…</p>}
          {error && (
            <p className="ritual-error" role="alert">
              {error}
            </p>
          )}
        </section>
      ) : (
        <section
          className="ritual-stage ritual-result"
          tabIndex={-1}
          ref={resultTarget}
          aria-label={room.name + " reading"}
        >
          <RitualReading
            s={data.snapshot}
            native={data.result}
            still={still}
            complete={complete}
            cue={() => oracle.sound.cue("reveal")}
          />
          {finished && (
            <>
              <SourceDepth s={data.snapshot} />
              <SaveRitual data={data} oracle={oracle} />
              <details className="ritual-depth">
                <summary>Native reading export</summary>
                <p>
                  The full file can include private notes, observations and
                  original request details.
                </p>
                <button
                  className="secondary"
                  onClick={() =>
                    download(data.result, `fate-${room.slug}-native.json`)
                  }
                >
                  Export full native reading
                </button>
              </details>
            </>
          )}
          <button className="text-button ritual-reset" onClick={reset}>
            ↶ Start a fresh visit
          </button>
        </section>
      )}
    </div>
  );
}
