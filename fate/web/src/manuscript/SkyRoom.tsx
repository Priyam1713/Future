import { useEffect, useRef, useState } from "react";
import { api } from "../types";
import type { Oracle } from "../hooks/useOracle";
import { BirthChart } from "../astrology/BirthChart";
import { degree, type Geometry } from "../astrology/contracts";
import { ResultLeaf } from "../components/ResultLeaf";
import { ROOMS, type Envelope, type NativeResult } from "./contracts";
import { MeridianMap, type MapLine } from "./MeridianMap";
import { ResultActions } from "./Result";
import { SkySite, type Site } from "./SkySite";

type SkyId = 5 | 6 | 7;
type Source = { author: string; edition: string; url: string };
type Note = { text: string; locator: string; rule_id: string };
type HoraryReport = NativeResult & {
  technique_id: 5;
  classification: string;
  judgment_certified: boolean;
  question_chart: Geometry;
  significators: { querent: string; co_significator: string };
  planetary_hour: { lord?: string };
  rule_diagnostics: {
    id: string;
    value: boolean | null;
    reason: string;
    locator: string;
  }[];
  source: Source;
};
type SkyEvent = {
  sign?: string;
  bodies?: string[];
  utc: string;
  chart: Geometry;
  rule: Note;
  reading: {
    placements: {
      planet: string;
      house: number;
      components: Note[];
      coverage: string;
    }[];
  };
};
type MundaneReport = NativeResult & {
  technique_id: 6;
  events: SkyEvent[];
  motion_changes?: { type: string; utc: string; body: string }[];
  source: Source;
};
type MapReport = NativeResult & {
  technique_id: 7;
  geojson: { features: MapLine[] };
};
type SkyReport = HoraryReport | MundaneReport | MapReport;
const london = { latitude: 51.5072, longitude: -0.1276, zone: "Europe/London" };
const sampleMoment = { ...london, local: "1990-07-15T14:30", fold: null };
const readable = (text: string) =>
  text.replaceAll("_", " ").replace(/^./, (s) => s.toUpperCase());
const utc = (instant: string) =>
  new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "long",
    timeZone: "UTC",
  }).format(new Date(instant));

function InstrumentCover({ id }: { id: 5 | 6 }) {
  return (
    <div className="court-cover">
      <svg viewBox="0 0 320 320" aria-hidden="true">
        <circle cx="160" cy="160" r="148" />
        <circle cx="160" cy="160" r="137" className="court-ticks" />
        <circle cx="160" cy="160" r="102" />
        <circle cx="160" cy="160" r="76" className="court-ticks" />
        <path d="M160 21V300 M21 160h279 M57 57l206 206 M57 263L263 57" />
        {id === 5 ? (
          <>
            <path className="court-mark" d="M160 73L228 160 160 247 92 160Z" />
            <path
              className="court-mark"
              d="M127 173Q160 121 193 173Q160 195 127 173Z"
            />
            <circle cx="160" cy="169" r="9" />
          </>
        ) : (
          <>
            <circle cx="160" cy="160" r="35" className="court-mark" />
            {[0, 1, 2, 3].map((i) => (
              <path
                key={i}
                className="court-mark"
                d="M160 49l7 16-7 11-7-11Z"
                transform={`rotate(${i * 90} 160 160)`}
              />
            ))}
          </>
        )}
      </svg>
      <span>{id === 5 ? "THE ADVICE BEGINS" : "THE COLLECTIVE SKY"}</span>
    </div>
  );
}

function HoraryReading({
  result,
  oracle,
}: {
  result: HoraryReport;
  oracle: Oracle;
}) {
  const [selected, setSelected] = useState(result.significators.querent);
  const unknown = result.rule_diagnostics.filter(
    (row) => row.value === null,
  ).length;
  return (
    <div className="folio-work sky-reading">
      <BirthChart
        chart={result.question_chart}
        onSelect={setSelected}
        selected={selected}
        label="Calculated question chart with native planetary longitudes and houses"
        reduced={oracle.reduced}
        paused={oracle.paused}
      />
      <ResultLeaf
        status="Advice-intent diagnostics"
        title={
          result.judgment_certified
            ? readable(result.classification)
            : "Judgment indeterminate"
        }
        evidence={
          <details className="folio-depth">
            <summary>Open the Lilly diagnostics</summary>
            <p>
              <a href={result.source.url} target="_blank" rel="noreferrer">
                {result.source.author} · {result.source.edition}
              </a>
            </p>
            <ul className="diagnostic-list">
              {result.rule_diagnostics.map((row) => (
                <li key={row.id}>
                  <b>
                    {row.value === null
                      ? "Unresolved"
                      : row.value
                        ? "Condition met"
                        : "Condition absent"}
                  </b>
                  <p>
                    {row.reason} <small>{row.locator}</small>
                  </p>
                </li>
              ))}
            </ul>
          </details>
        }
      >
        <p className="folio-lead">
          The native chart can trace individual testimonies. Lilly’s full
          judgment remains unresolved.
        </p>
        <dl className="sky-glance">
          <div>
            <dt>First-house ruler</dt>
            <dd>{result.significators.querent}</dd>
          </div>
          <div>
            <dt>Planetary hour</dt>
            <dd>{result.planetary_hour.lord || "Unavailable"}</dd>
          </div>
          <div>
            <dt>Open diagnostics</dt>
            <dd>{unknown}</dd>
          </div>
        </dl>
      </ResultLeaf>
    </div>
  );
}

function MundaneReading({
  result,
  oracle,
}: {
  result: MundaneReport;
  oracle: Oracle;
}) {
  const [index, setIndex] = useState(0);
  const [planet, setPlanet] = useState("Sun");
  const event = result.events[index];
  const row = event?.reading.placements.find((pick) => pick.planet === planet);
  const label = (item: SkyEvent) =>
    item.sign
      ? `${item.sign} ingress`
      : item.bodies?.join("–") + " conjunction";
  return (
    <div className="cycle-exhibit">
      {result.events.length > 0 && (
        <div
          className="folio-picks cycle-tabs"
          role="group"
          aria-label="Calculated events"
        >
          {result.events.map((item, i) => (
            <button
              key={item.utc}
              aria-pressed={i === index}
              onClick={() => setIndex(i)}
            >
              <time dateTime={item.utc}>{utc(item.utc)}</time>
              {label(item)}
            </button>
          ))}
        </div>
      )}
      {event ? (
        <div className="folio-work sky-reading">
          <BirthChart
            chart={event.chart}
            selected={planet}
            onSelect={setPlanet}
            reduced={oracle.reduced}
            paused={oracle.paused}
            label="Calculated ingress or conjunction chart with native planetary positions"
          />
          <ResultLeaf
            status="Calculated event · UTC"
            title={label(event)}
            evidence={
              <details className="folio-depth">
                <summary>Green’s source components</summary>
                <p>
                  <a href={result.source.url} target="_blank" rel="noreferrer">
                    {result.source.author} · {result.source.edition}
                  </a>
                </p>
                <p>
                  {event.rule.text} <small>{event.rule.locator}</small>
                </p>
                {row?.components.map((note) => (
                  <p key={note.rule_id}>
                    {note.text} <small>{note.locator}</small>
                  </p>
                ))}
              </details>
            }
          >
            <p className="folio-lead">
              <time dateTime={event.utc}>{utc(event.utc)}</time>
            </p>
            {row && (
              <p>
                {row.planet} occupies house {row.house} at the selected site
                {event.chart.planets[row.planet]
                  ? `, at ${degree(event.chart.planets[row.planet].longitude)}`
                  : ""}
                .
              </p>
            )}
            <p>
              Green’s historical topics are available as individual components.
            </p>
          </ResultLeaf>
        </div>
      ) : (
        <ResultLeaf
          status="Native search"
          title="No exact Jupiter–Saturn contact this year"
        >
          <p className="folio-lead">
            The search still found the following motion changes in the selected
            window.
          </p>
        </ResultLeaf>
      )}
      {result.motion_changes && (
        <details className="folio-depth">
          <summary>Stations and sign crossings</summary>
          <ol>
            {result.motion_changes.map((change, i) => (
              <li key={i}>
                {change.body} · {readable(change.type)} · {utc(change.utc)}
              </li>
            ))}
          </ol>
        </details>
      )}
    </div>
  );
}

export function SkyRoom({ id, oracle }: { id: SkyId; oracle: Oracle }) {
  const [custom, setCustom] = useState(false);
  const [question, setQuestion] = useState("");
  const [local, setLocal] = useState("");
  const [fold, setFold] = useState("");
  const [year, setYear] = useState("");
  const [cycle, setCycle] = useState<"ingresses" | "conjunctions">("ingresses");
  const [site, setSite] = useState<Site>();
  const [result, setResult] = useState<SkyReport>();
  const [example, setExample] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const controller = useRef<AbortController | null>(null);
  const target = useRef<HTMLElement>(null);
  useEffect(() => () => controller.current?.abort(), []);
  useEffect(() => {
    if (result) target.current?.focus({ preventScroll: true });
  }, [result]);
  async function calculate(demo: boolean) {
    if (controller.current || (!site && !demo)) return;
    const chosenSite = demo ? london : site!;
    const moment = demo
      ? sampleMoment
      : { ...chosenSite, local, fold: fold === "" ? null : Number(fold) };
    const questionText = demo
      ? "What can be examined about this advice?"
      : question.trim();
    const body =
      id === 5
        ? { oracle: id, moment, question: questionText }
        : id === 6
          ? {
              oracle: id,
              cycle,
              year: demo ? (cycle === "ingresses" ? 2026 : 2020) : Number(year),
              site: chosenSite,
            }
          : { oracle: id, moment };
    const c = new AbortController();
    controller.current = c;
    setBusy(true);
    setError("");
    try {
      const output = await api<Envelope<SkyReport>>(
        "/api/sky-manuscript",
        body,
        c.signal,
      );
      if (!c.signal.aborted) {
        setResult(output.result);
        setExample(demo);
        oracle.markExplored(id);
        oracle.sound.cue("reveal");
      }
    } catch (e) {
      if (!c.signal.aborted) setError((e as Error).message);
    } finally {
      if (!c.signal.aborted) {
        controller.current = null;
        setBusy(false);
      }
    }
  }
  return result ? (
    <section
      ref={target}
      className="sky-results"
      tabIndex={-1}
      aria-label="Calculated sky result"
    >
      {example && (
        <p className="sky-example">
          Teaching example · London ·{" "}
          {id === 6
            ? cycle === "ingresses"
              ? "2026"
              : "2020"
            : "15 July 1990"}
        </p>
      )}
      {result.technique_id === 5 ? (
        <HoraryReading result={result} oracle={oracle} />
      ) : result.technique_id === 6 ? (
        <MundaneReading result={result} oracle={oracle} />
      ) : (
        <MeridianMap features={result.geojson.features} />
      )}
      <ResultActions oracle={oracle} result={result} name={ROOMS[id][0]} />
      <button className="text-button" onClick={() => setResult(undefined)}>
        Choose another moment ←
      </button>
    </section>
  ) : (
    <div className={`folio-work sky-input sky-${id}`}>
      {id === 7 ? <MeridianMap /> : <InstrumentCover id={id} />}
      <div className="folio-desk">
        <p className="eyebrow">
          {id === 5
            ? "Lilly · Advice-intent scope"
            : id === 6
              ? "Green · Historical cycles"
              : "Geocentric planetary angularity"}
        </p>
        <h2>
          {id === 5
            ? "Begin with the moment of advice"
            : id === 6
              ? "Choose a cycle"
              : "Follow a line across the world"}
        </h2>
        {id === 6 && (
          <div className="folio-picks" role="group" aria-label="Cycle type">
            <button
              aria-pressed={cycle === "ingresses"}
              disabled={busy}
              onClick={() => setCycle("ingresses")}
            >
              Cardinal solar ingresses
            </button>
            <button
              aria-pressed={cycle === "conjunctions"}
              disabled={busy}
              onClick={() => setCycle("conjunctions")}
            >
              Jupiter–Saturn conjunctions
            </button>
          </div>
        )}
        <div className="folio-picks sky-start">
          <button
            className="primary"
            disabled={busy}
            onClick={() => void calculate(true)}
          >
            Explore the teaching example
          </button>
          <button
            disabled={busy}
            onClick={() => setCustom(!custom)}
            aria-expanded={custom}
          >
            {id === 6 ? "Set year and place" : "Use a recorded moment"}
          </button>
        </div>
        {custom && (
          <form
            className="sky-form"
            onSubmit={(e) => {
              e.preventDefault();
              void calculate(false);
            }}
          >
            {id === 5 && (
              <label>
                Advice question
                <textarea
                  rows={2}
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  required
                  maxLength={320}
                  disabled={busy}
                />
              </label>
            )}
            {id === 6 ? (
              <label>
                UTC year
                <input
                  type="number"
                  min="1851"
                  max="2148"
                  value={year}
                  onChange={(e) => setYear(e.target.value)}
                  required
                  disabled={busy}
                />
              </label>
            ) : (
              <label>
                {id === 5
                  ? "When the adviser first disclosed advice"
                  : "Recorded birth date and time"}
                <input
                  type="datetime-local"
                  step="1"
                  min="1851-01-01T00:00"
                  max="2148-12-31T23:59"
                  value={local}
                  onChange={(e) => setLocal(e.target.value)}
                  required
                  disabled={busy}
                />
              </label>
            )}
            <SkySite value={site} onSite={setSite} disabled={busy} />
            {id !== 6 && (
              <details className="folio-depth">
                <summary>Repeated local hour</summary>
                <label>
                  Occurrence
                  <select
                    value={fold}
                    onChange={(e) => setFold(e.target.value)}
                    disabled={busy}
                  >
                    <option value="">Standard validation</option>
                    <option value="0">First occurrence</option>
                    <option value="1">Second occurrence</option>
                  </select>
                </label>
              </details>
            )}
            <button
              className="primary"
              disabled={busy || !site || (id === 5 && !question.trim())}
            >
              Calculate the sky
            </button>
          </form>
        )}
        {busy && (
          <p role="status">
            {id === 6 && cycle === "conjunctions"
              ? "Tracing the year’s slow contacts and stations. This may take several seconds…"
              : "Calculating the sky…"}
          </p>
        )}
        {error && <p role="alert">{error}</p>}
      </div>
    </div>
  );
}
