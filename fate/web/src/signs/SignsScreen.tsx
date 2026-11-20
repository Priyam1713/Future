import { useEffect, useRef, useState } from "react";
import { chapterFor } from "../codex/records";
import type { Oracle } from "../hooks/useOracle";
import { api } from "../types";
import { Artifact, hasArtifactControls } from "./Artifact";
import { archivedView } from "./reference";
import {
  choicesTitle,
  ENVIRONMENTS,
  fields,
  options,
  SIGNS,
  validValues,
  type SignEnvelope,
  type SignId,
  type SignSnapshot,
  type SignView,
} from "./contracts";

function SourceDepth({ view }: { view: SignView }) {
  if (!view.excerpts.length) return null;
  return (
    <details className="ritual-depth sign-depth">
      <summary>Sources and conditions</summary>
      {view.excerpts.map((e, i) => (
        <blockquote key={i}>
          <p>{e.text}</p>
          <cite>
            {e.status} ·{" "}
            {e.url ? (
              <a href={e.url} target="_blank" rel="noreferrer">
                {e.locator}
              </a>
            ) : (
              e.locator
            )}
          </cite>
        </blockquote>
      ))}
    </details>
  );
}
const directionLabels: Record<string, string> = {
  same_x: "same x",
  same_y: "same y",
  left: "left",
  right: "right",
  above: "above",
  below: "below",
};
function Reading({
  id,
  values,
  view,
  compact = false,
}: {
  id: SignId;
  values: string[];
  view: SignView;
  compact?: boolean;
}) {
  return (
    <article className={"sign-reading " + (compact ? "sign-compact" : "")}>
      <div className="sign-display">
        <Artifact id={id} values={values} compact={compact} />
      </div>
      {!compact && (
        <div className="sign-interpretation">
          <p className="eyebrow">{view.status}</p>
          <h2>{choicesTitle({ oracle: id, values })}</h2>
          <p className="sign-lead">
            {view.lead.replace(/([,;])(?=[A-Za-z])/g, "$1 ")}
          </p>
          {view.metric && (
            <p
              className="sign-metric"
              data-distance={view.metric.distanceSquared}
            >
              {view.metric.direction.map((d) => directionLabels[d]).join(" · ")}{" "}
              · distance squared {view.metric.distanceSquared}
            </p>
          )}
          <SourceDepth view={view} />
          <details className="ritual-depth sign-selections">
            <summary>Your selections</summary>
            <dl className="sign-declaration">
              {fields(id).map((field, i) => (
                <div key={field.label}>
                  <dt>{field.label}</dt>
                  <dd>
                    {
                      options(id, i, values).find(
                        ([value]) => value === values[i],
                      )?.[1]
                    }
                  </dd>
                </div>
              ))}
            </dl>
          </details>
        </div>
      )}
    </article>
  );
}
export function SavedSign({
  s,
  index,
  compact = false,
}: {
  s: SignSnapshot;
  index?: number;
  compact?: boolean;
}) {
  const room = SIGNS[s.oracle];
  return (
    <div
      className={`${compact ? "sign-study" : "sign-folio"} sign-${room.stage} sign-${room.slug}`}
      data-sign-still="true"
    >
      {!compact && (
        <header className="folio-heading">
          <p className="eyebrow">
            Chapter {(index ?? 0) + 1} · {room.name}
          </p>
          <h2 tabIndex={-1}>{choicesTitle(s)}</h2>
        </header>
      )}
      <Reading
        id={s.oracle}
        values={s.values}
        view={archivedView(s)}
        compact={compact}
      />
    </div>
  );
}
function saveNative(payload: object, slug: string) {
  const url = URL.createObjectURL(
    new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" }),
  );
  const link = document.createElement("a");
  link.href = url;
  link.download = `fate-${slug}-native.json`;
  link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function Save({ data, oracle }: { data: SignEnvelope; oracle: Oracle }) {
  const s = data.snapshot;
  const [issue, setIssue] = useState(false);
  if (!s) return null;
  const chapter = chapterFor(data.result, s);
  const saved = oracle.codex.chapters.some((c) => c.id === chapter.id);
  return (
    <section className="ritual-save">
      <div>
        <h3>Keep this chapter</h3>
        <p>
          Keep these selections and the source edition in this browser. The
          chapter is stored unencrypted.
        </p>
      </div>
      <div>
        <button
          className="secondary"
          disabled={saved}
          onClick={() => setIssue(!oracle.codex.save(chapter))}
        >
          {saved ? "Saved to this device" : "Save sign chapter to this device"}
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
        {issue && <p role="alert">My Fate could not save this chapter.</p>}
      </div>
    </section>
  );
}
export default function SignsScreen({
  id,
  oracle,
}: {
  id: SignId;
  oracle: Oracle;
}) {
  const room = SIGNS[id],
    spec = fields(id);
  const [step, setStep] = useState(0),
    [values, setValues] = useState<string[]>([]),
    [data, setData] = useState<SignEnvelope | null>(null);
  const [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  const inflight = useRef<AbortController | null>(null),
    target = useRef<HTMLElement>(null),
    stepHeading = useRef<HTMLHeadingElement>(null);
  useEffect(() => () => inflight.current?.abort(), []);
  useEffect(() => {
    if (data) {
      target.current?.focus({ preventScroll: true });
      target.current?.scrollIntoView({ block: "start", behavior: "instant" });
    }
  }, [data]);
  function choose(value: string) {
    setValues([...values.slice(0, step), value]);
    setStep(step + 1);
    setError("");
    oracle.sound.cue("select");
    requestAnimationFrame(() =>
      stepHeading.current?.focus({ preventScroll: true }),
    );
  }
  function restart() {
    setStep(0);
    setValues([]);
    setData(null);
    setError("");
    requestAnimationFrame(() =>
      document
        .querySelector(".sign-stage")
        ?.scrollIntoView({ block: "start", behavior: "instant" }),
    );
  }
  async function read() {
    if (inflight.current || !validValues(id, values)) return;
    const request = new AbortController();
    inflight.current = request;
    setBusy(true);
    setError("");
    try {
      const output = await api<SignEnvelope>(
        "/api/world-of-signs",
        { oracle: id, values },
        request.signal,
      );
      if (!request.signal.aborted) {
        setData(output);
        oracle.markExplored(id);
        oracle.sound.cue("reveal");
      }
    } catch (e) {
      if (!request.signal.aborted)
        setError(
          e instanceof Error
            ? e.message
            : "The source comparison did not finish.",
        );
    } finally {
      if (inflight.current === request) inflight.current = null;
      if (!request.signal.aborted) setBusy(false);
    }
  }
  const selected = step === spec.length;
  const artifactControl = hasArtifactControls(id, step);
  return (
    <div
      className={`sign-room page-enter sign-${room.stage} sign-${room.slug}`}
      data-sign-still={oracle.reduced || oracle.paused}
    >
      <header className="sign-hero">
        <picture>
          <source
            media="(max-width:640px)"
            srcSet={`/art/signs-${room.stage}-720.webp`}
          />
          <img
            alt=""
            src={`/art/signs-${room.stage}-1440.webp`}
            width={1440}
            height={960}
            fetchPriority="high"
          />
        </picture>
        <div className="sign-intro">
          <button
            className="text-button"
            onClick={() => oracle.navigate("gallery")}
          >
            ← Oracle Gallery
          </button>
          <p className="eyebrow">
            {ENVIRONMENTS[room.stage]} · {room.name}
          </p>
          <h1 ref={oracle.heading} tabIndex={-1}>
            {room.title}
          </h1>
          <p>{room.prompt}</p>
        </div>
      </header>
      {!data ? (
        <section className="sign-stage" aria-label={room.name + " entry"}>
          <div className="sign-station">
            <div className="sign-display">
              <Artifact id={id} values={values} step={step} choose={choose} />
            </div>
            <div className="sign-step">
              <p className="eyebrow">
                {id === 35 || id === 39
                  ? "Documentary comparison"
                  : "Your declaration"}{" "}
                · {Math.min(step + 1, spec.length)} of {spec.length}
              </p>
              <h2 tabIndex={-1} ref={stepHeading}>
                {selected ? "Ready to compare." : spec[step].label}
              </h2>
              {selected ? (
                <>
                  <ul className="sign-selection">
                    {spec.map((field, i) => (
                      <li key={field.label}>
                        <small>{field.label}</small>
                        {
                          options(id, i, values).find(
                            ([value]) => value === values[i],
                          )?.[1]
                        }
                      </li>
                    ))}
                  </ul>
                  <button className="primary" disabled={busy} onClick={read}>
                    {busy ? "Comparing…" : room.action}
                  </button>
                </>
              ) : artifactControl ? (
                <p className="sign-hint">Choose directly on the diagram.</p>
              ) : (
                <div
                  className={`sign-options ${id === 35 ? "case-options" : ""}`}
                  role="group"
                  aria-label={spec[step].label}
                >
                  {options(id, step, values).map(([key, label]) => (
                    <button key={key} onClick={() => choose(key)}>
                      {label}
                    </button>
                  ))}
                </div>
              )}
              {step > 0 && (
                <button
                  className="text-button"
                  disabled={busy}
                  onClick={() => {
                    setStep(step - 1);
                    setValues(values.slice(0, step - 1));
                    setError("");
                  }}
                >
                  ← Edit previous choice
                </button>
              )}
              {error && <p role="alert">{error}</p>}
            </div>
          </div>
          <p className="sign-caption">
            The diagram illustrates selections you make.
          </p>
        </section>
      ) : (
        <section
          className="sign-stage sign-result"
          ref={target}
          tabIndex={-1}
          aria-label={room.name + " reading"}
        >
          <Reading id={id} values={values} view={data.view} />
          <Save data={data} oracle={oracle} />
          <details className="ritual-depth">
            <summary>Native comparison export</summary>
            <button
              className="secondary"
              onClick={() => saveNative(data.result, room.slug)}
            >
              Export full native reading
            </button>
          </details>
          <button className="text-button" onClick={restart}>
            ↶ Make another declaration
          </button>
        </section>
      )}
    </div>
  );
}
