import { useEffect, useMemo, useRef, useState } from "react";
import { api } from "../types";
import type { Oracle } from "../hooks/useOracle";
import { TimeInstrument } from "./TimeInstrument";
import { ContactReading, TransitSources } from "./EventReading";
import { ASPECT_NAMES } from "../astrology/BirthChart";
import {
  dateLabel,
  fullTime,
  timeLabel,
  type TransitEvent,
  type TransitOrigin,
  type TurningResult,
} from "./contracts";
import { SaveTransit } from "./save";
export function TurningExperience({
  result,
  oracle,
  saved = false,
}: {
  result: TurningResult;
  oracle?: Oracle;
  saved?: boolean;
}) {
  const [day, setDay] = useState(0),
    [eventId, setEventId] = useState<string | null>(null),
    [showAll, setShowAll] = useState(false),
    [tab, setTab] = useState<"contacts" | "duration" | "repeats">("contacts");
  const heading = useRef<HTMLHeadingElement>(null),
    events = result.report.exact_events,
    frame = result.sky_samples[day],
    selected = events.find((e) => e.id === eventId) ?? null;
  useEffect(() => {
    if (saved) return;
    heading.current?.focus({ preventScroll: true });
    heading.current
      ?.closest(".turning-overview")
      ?.scrollIntoView({ block: "start", behavior: "instant" });
  }, [result, saved]);
  const configs = result.report.configurations,
    config = selected
      ? configs.find((c) => c.configuration_id === selected.configuration_id)
      : null;
  const dayEnd = Date.parse(frame.utc) + 86400000;
  const dated = events.filter(
    (e) =>
      Date.parse(e.exact_utc) >= Date.parse(frame.utc) &&
      Date.parse(e.exact_utc) < dayEnd,
  );
  const shown = showAll ? events : dated;
  const current = configs.filter((c) =>
    frame.contacts.some((x) => x.configuration_id === c.configuration_id),
  );
  const ongoing = [...configs]
    .filter((c) => c.hours_in_window >= 24)
    .sort(
      (a, b) =>
        (a.intervals[0]?.start_utc ?? "").localeCompare(
          b.intervals[0]?.start_utc ?? "",
        ) || a.configuration_id.localeCompare(b.configuration_id),
    );
  function select(e: TransitEvent | null) {
    setEventId(e?.id ?? null);
    if (e) {
      const i = result.sky_samples.findIndex(
        (f, j) =>
          Date.parse(e.exact_utc) >= Date.parse(f.utc) &&
          (j === result.sky_samples.length - 1 ||
            Date.parse(e.exact_utc) <
              Date.parse(result.sky_samples[j + 1].utc)),
      );
      if (i >= 0) setDay(i);
      oracle?.sound.cue("select");
    }
  }
  return (
    <div className={`turning-experience ${saved ? "turning-saved" : ""}`}>
      <header className="turning-overview">
        <p className="eyebrow">
          {saved
            ? "A DATED CHAPTER / SAVED NATIVE SKY"
            : "YOUR DATED SKY / A WINDOW OF DISCOVERY"}
        </p>
        <h2 ref={heading} tabIndex={-1}>
          Time makes
          <br />
          <em>new connections.</em>
        </h2>
        <p>
          {fullTime(result.report.window.start_utc)} →{" "}
          {fullTime(result.report.window.end_utc)} · end excluded
        </p>
        <div className="turning-counts">
          <p>
            <strong>{events.length}</strong>
            <span>exact contacts</span>
          </p>
          <p>
            <strong>{ongoing.length}</strong>
            <span>within orb for 24+ hours</span>
          </p>
          <p>
            <strong>
              {result.report.presentation.repeated_patterns.length}
            </strong>
            <span>repeating sequences</span>
          </p>
        </div>
        <p className="turning-promise">
          These are astronomical relationships to your natal chart. Their
          symbolic language offers a way to reflect, without predicting what
          will happen to you.
        </p>
      </header>
      <div className="turning-layout">
        <div className="turning-artifact">
          <TimeInstrument
            result={result}
            index={day}
            onDay={setDay}
            selectedEvent={selected}
            onEvent={select}
            reduced={oracle?.reduced ?? true}
            paused={oracle?.paused ?? true}
          />
          <p className="turning-sample-note">
            {selected
              ? "Exact native contact position; other transiting bodies are hidden in this focus."
              : `Native sample · ${fullTime(frame.utc)}. Dates step between calculated samples, without interpolation.`}
          </p>
        </div>
        <div className="turning-focus">
          {selected && config ? (
            <>
              <button className="text-button" onClick={() => select(null)}>
                ← Return to the daily sky
              </button>
              <ContactReading event={selected} config={config} />
            </>
          ) : (
            <section className="daily-focus" aria-live="polite">
              <p className="eyebrow">
                DAY {day + 1} / {result.sky_samples.length}
              </p>
              <h2>
                {dateLabel(frame.utc)}
                <br />
                <em>
                  {dated.length
                    ? `${dated.length} exact ${dated.length === 1 ? "contact" : "contacts"}.`
                    : "A sky between exact moments."}
                </em>
              </h2>
              <p>
                {current.length} configurations are within their declared orbs
                at this sample. Applying approaches exactness; separating
                recedes. A station can interrupt either sequence.
              </p>
              <div className="daily-contacts">
                {frame.contacts.slice(0, 4).map((c) => {
                  const conf = configs.find(
                    (x) => x.configuration_id === c.configuration_id,
                  )!;
                  const next = events.find(
                    (e) => e.configuration_id === c.configuration_id,
                  );
                  return (
                    <button
                      key={c.configuration_id}
                      disabled={!next}
                      onClick={() => next && select(next)}
                    >
                      <span>
                        {conf.transiting} / natal {conf.natal_target}
                      </span>
                      <small>
                        {ASPECT_NAMES[conf.aspect_degrees]} · {c.phase}
                        {next ? " · explore exact contact" : ""}
                      </small>
                    </button>
                  );
                })}
              </div>
              <details>
                <summary>All contacts active at this sample</summary>
                {frame.contacts.map((c) => {
                  const x = configs.find(
                    (v) => v.configuration_id === c.configuration_id,
                  )!;
                  return (
                    <p key={c.configuration_id}>
                      {x.transiting}{" "}
                      {ASPECT_NAMES[x.aspect_degrees].toLowerCase()} natal{" "}
                      {x.natal_target} · {c.phase}
                    </p>
                  );
                })}
              </details>
              <p className="scope-note">
                Shown in native configuration order, without an importance
                ranking. Some configurations stay within orb without reaching
                exactness in this window.
              </p>
            </section>
          )}
        </div>
      </div>
      <section
        className="turning-timeline"
        aria-labelledby="turning-events-title"
      >
        <div className="timeline-heading">
          <div>
            <p className="eyebrow">FOLLOW A THREAD THROUGH TIME</p>
            <h2 id="turning-events-title">
              Discover the <em>turning points.</em>
            </h2>
          </div>
          <label className="turning-check">
            <input
              type="checkbox"
              checked={showAll}
              onChange={(e) => setShowAll(e.target.checked)}
            />
            Show the entire window
          </label>
        </div>
        <div
          className="date-rail"
          role="group"
          aria-label="Choose a calculated daily sample"
        >
          {result.sky_samples.map((f, i) => {
            const count = events.filter(
              (e) =>
                Date.parse(e.exact_utc) >= Date.parse(f.utc) &&
                Date.parse(e.exact_utc) < Date.parse(f.utc) + 86400000,
            ).length;
            return (
              <button
                key={f.utc}
                aria-pressed={i === day}
                onClick={() => {
                  select(null);
                  setDay(i);
                }}
              >
                <span>{dateLabel(f.utc)}</span>
                <i aria-hidden="true">{count ? "●" : "·"}</i>
                <small>{count} exact</small>
              </button>
            );
          })}
        </div>
        <nav className="turning-tabs" aria-label="Transit views">
          {(["contacts", "duration", "repeats"] as const).map((t) => (
            <button key={t} aria-pressed={tab === t} onClick={() => setTab(t)}>
              {t === "contacts"
                ? "Dated contacts"
                : t === "duration"
                  ? "Staying in orb"
                  : "Repeated paths"}
            </button>
          ))}
        </nav>
        {tab === "contacts" ? (
          <div className="event-tracks">
            {shown.length ? (
              shown.map((e) => (
                <button
                  className={`event-track ${selected?.id === e.id ? "event-chosen" : ""}`}
                  key={e.id}
                  onClick={() => {
                    select(e);
                    document.querySelector(".turning-layout")?.scrollIntoView({
                      block: "start",
                      behavior:
                        oracle?.reduced || oracle?.paused
                          ? "instant"
                          : "smooth",
                    });
                  }}
                >
                  <time dateTime={e.exact_utc}>
                    <strong>{dateLabel(e.exact_utc)}</strong>
                    <span>{timeLabel(e.exact_utc)} UTC</span>
                  </time>
                  <span className="event-track-line" aria-hidden="true">
                    ○
                  </span>
                  <div>
                    <h3>
                      {e.transiting}{" "}
                      <em>{ASPECT_NAMES[e.aspect_degrees].toLowerCase()}</em>{" "}
                      natal {e.natal_target}
                    </h3>
                    <p>
                      {e.retrograde ? "Retrograde · " : ""}
                      {e.passes_in_window > 1
                        ? `Pass ${e.pass_in_window} of ${e.passes_in_window} · `
                        : ""}
                      {e.interpretations.direct.length
                        ? "Documented symbolic pair"
                        : "Separate source components"}
                    </p>
                  </div>
                  <span aria-hidden="true">↗</span>
                </button>
              ))
            ) : (
              <div className="empty-sky">
                <span aria-hidden="true">☽</span>
                <h3>No exact contact falls in this day’s interval.</h3>
                <p>
                  The sky still moves; this is not a missing prediction. Explore
                  another day or the contacts staying within orb.
                </p>
              </div>
            )}
          </div>
        ) : tab === "duration" ? (
          <div className="duration-tracks">
            <p>
              Within orb for at least 24 calculated hours inside this window.
              Duration is a display category, not strength, probability or
              personal importance. Ordered by interval start.
            </p>
            {ongoing.map((c) => (
              <article key={c.configuration_id}>
                <h3>
                  {c.transiting} {ASPECT_NAMES[c.aspect_degrees].toLowerCase()}{" "}
                  natal {c.natal_target}
                </h3>
                <p>
                  {c.hours_in_window.toFixed(1)} hours within {c.orb_limit}° orb
                </p>
                <div
                  className="duration-line"
                  aria-label="Calculated orb intervals"
                >
                  {c.intervals.map((w, i) => (
                    <span
                      key={i}
                      style={{
                        left: `${((Date.parse(w.start_utc) - Date.parse(result.report.window.start_utc)) / (Date.parse(result.report.window.end_utc) - Date.parse(result.report.window.start_utc))) * 100}%`,
                        width: `${((Date.parse(w.end_utc) - Date.parse(w.start_utc)) / (Date.parse(result.report.window.end_utc) - Date.parse(result.report.window.start_utc))) * 100}%`,
                      }}
                    />
                  ))}
                </div>
                <details>
                  <summary>Dates, clipping & sources</summary>
                  {c.intervals.map((w, i) => (
                    <p key={i}>
                      {fullTime(w.start_utc)} → {fullTime(w.end_utc)}
                      {w.start_clipped || w.end_clipped
                        ? " · clipped; full duration unknown"
                        : ""}
                    </p>
                  ))}
                  <TransitSources interpretation={c.interpretations} />
                </details>
              </article>
            ))}
          </div>
        ) : (
          <div className="repeated-tracks">
            {result.report.presentation.repeated_patterns.length ? (
              result.report.presentation.repeated_patterns.map((p) => (
                <article key={p.configuration_id}>
                  <p className="eyebrow">{p.kind}</p>
                  <h3>
                    {
                      configs.find(
                        (c) => c.configuration_id === p.configuration_id,
                      )?.transiting
                    }{" "}
                    / natal{" "}
                    {
                      configs.find(
                        (c) => c.configuration_id === p.configuration_id,
                      )?.natal_target
                    }
                  </h3>
                  <div>
                    {p.event_ids.map((id, i) => {
                      const e = events.find((e) => e.id === id)!;
                      return (
                        <button
                          className="secondary"
                          key={id}
                          onClick={() => select(e)}
                        >
                          Pass {i + 1} · {dateLabel(e.exact_utc)} ↗
                        </button>
                      );
                    })}
                  </div>
                  <p>{p.explanation}</p>
                  <a href={p.source} target="_blank" rel="noreferrer">
                    Sequence source · {p.locator}
                  </a>
                </article>
              ))
            ) : (
              <div className="empty-sky">
                <h3>No repeated exact sequence in this window.</h3>
                <p>
                  This count says nothing about contacts outside the selected
                  dates.
                </p>
              </div>
            )}
          </div>
        )}
      </section>
      <details className="turning-method">
        <summary>Calculation method, native export & limitations</summary>
        <p>{result.sampling}</p>
        <p>
          All times UTC. Exact events use a half-open window: start included,
          end excluded. Orb intervals and hours are clipped to this window. A
          0.25-second numerical root bracket is not a claim of absolute timing
          or predictive accuracy.
        </p>
        {result.report.limitations.map((t, i) => (
          <p key={i}>{t}</p>
        ))}
        <p>
          <a
            href={result.report.presentation.phase_context.source}
            target="_blank"
            rel="noreferrer"
          >
            Applying/separating source
          </a>{" "}
          ·{" "}
          <a
            href={result.report.presentation.grouping_source.url}
            target="_blank"
            rel="noreferrer"
          >
            Duration and repetition source
          </a>
        </p>
        {!saved && (
          <button
            className="secondary"
            onClick={() => {
              const u = URL.createObjectURL(
                new Blob([JSON.stringify(result, null, 2)], {
                  type: "application/json",
                }),
              );
              const a = document.createElement("a");
              a.href = u;
              a.download = "fate-turning-sky-native.json";
              a.click();
              setTimeout(() => URL.revokeObjectURL(u), 1000);
            }}
          >
            Export full native transit report
          </button>
        )}
      </details>
      {oracle && !saved && <SaveTransit result={result} oracle={oracle} />}
    </div>
  );
}
export default function TurningSky({
  origin,
  oracle,
  onBack,
}: {
  origin?: TransitOrigin;
  oracle: Oracle;
  onBack: () => void;
}) {
  const [start, setStart] = useState(() =>
      new Date(Date.now() + 60000).toISOString().slice(0, 16),
    ),
    [days, setDays] = useState(7),
    [result, setResult] = useState<TurningResult | null>(null),
    [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  const control = useRef<AbortController | null>(null),
    inflight = useRef(false);
  const title = useRef<HTMLHeadingElement>(null);
  useEffect(() => {
    title.current?.focus();
    return () => control.current?.abort();
  }, []);
  async function calculate() {
    if (inflight.current || !origin) return;
    inflight.current = true;
    setBusy(true);
    setError("");
    const c = new AbortController();
    control.current = c;
    const timer = setTimeout(() => c.abort("timeout"), 65000);
    try {
      const r = await api<TurningResult>(
        "/api/western/transits",
        { origin, start: start + ":00Z", days },
        c.signal,
      );
      if (c.signal.aborted) return;
      setResult(r);
      oracle.sound.cue("reveal");
    } catch (e) {
      setError(
        c.signal.aborted
          ? c.signal.reason === "timeout"
            ? "The calculation timed out. Try fewer days; your natal chart is still here."
            : "Calculation stopped. Your natal chart is still here."
          : e instanceof Error
            ? e.message
            : "The time instrument could not finish. Please retry.",
      );
    } finally {
      clearTimeout(timer);
      inflight.current = false;
      setBusy(false);
    }
  }
  return (
    <div className="turning-room page-enter">
      <div className="turning-environment" aria-hidden="true">
        <picture>
          <source
            media="(max-width:700px)"
            srcSet="/art/turning-sky-observatory-mobile-720.webp"
          />
          <img
            src="/art/turning-sky-observatory-960.webp"
            srcSet="/art/turning-sky-observatory-640.webp 640w, /art/turning-sky-observatory-960.webp 960w, /art/turning-sky-observatory-1536.webp 1536w"
            sizes="100vw"
            width="1536"
            height="1024"
            alt=""
          />
        </picture>
      </div>
      <div className="journey-top">
        <button className="text-button" onClick={onBack}>
          ← Your natal observatory
        </button>
        <span className="eyebrow">WESTERN ASTROLOGY / THROUGH TIME</span>
      </div>
      <header className="turning-heading">
        <p className="eyebrow">THE TURNING SKY</p>
        <h1 ref={title} tabIndex={-1}>
          A sky in motion.
          <br />
          <em>A moment to notice.</em>
        </h1>
        <p>Turn a real celestial instrument through the days ahead.</p>
      </header>
      <form
        className="turning-window"
        onSubmit={(e) => {
          e.preventDefault();
          void calculate();
        }}
      >
        <label>
          Start date and time · UTC
          <input
            type="datetime-local"
            required
            step="60"
            value={start}
            onChange={(e) => setStart(e.target.value)}
            disabled={busy}
          />
        </label>
        <label>
          Days to explore
          <select
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            disabled={busy}
          >
            {Array.from({ length: 30 }, (_, i) => (
              <option key={i + 1} value={i + 1}>
                {i + 1} {i ? "days" : "day"}
              </option>
            ))}
          </select>
        </label>
        <button className="primary" disabled={busy || !origin}>
          {busy
            ? "Calculating the turning sky…"
            : result
              ? "Calculate this window"
              : "Turn my sky"}{" "}
          <span aria-hidden="true">○</span>
        </button>
        {busy && (
          <button
            type="button"
            className="text-button"
            onClick={() => control.current?.abort("user")}
          >
            Stop calculation
          </button>
        )}
        <p className="window-privacy">
          Uses this visit’s already calculated natal geometry. No birth inputs
          are resent or reconstructed. One computation at a time, bounded to 60
          seconds. A 30-day search can take longer than a shorter window.
        </p>
        <p role="status" className="turning-status">
          {busy
            ? "Native positions, exact contacts and orb boundaries are being calculated. Any previous reading below retains its own dated window until this completes."
            : error}
        </p>
        {!origin && (
          <p className="scope-note">
            A fresh natal calculation is required. A saved chapter cannot supply
            missing birth information.
          </p>
        )}
      </form>
      {result ? (
        <TurningExperience
          key={result.report.window.start_utc + result.report.window.end_utc}
          result={result}
          oracle={oracle}
        />
      ) : (
        <section className="turning-threshold">
          <span aria-hidden="true">○</span>
          <h2>
            Dates become <em>discoveries.</em>
          </h2>
          <p>
            Choose a window to reveal actual contacts, ongoing intervals and
            repeating paths. Astronomical relationships come first; source
            meanings stay clearly separate.
          </p>
        </section>
      )}
    </div>
  );
}
