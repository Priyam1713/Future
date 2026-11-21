import { useId, useState } from "react";
import type { Numerology } from "./useNumerology";
import type { Oracle } from "../hooks/useOracle";
import type { NumberTrace } from "../experiences/contracts";
import { SaveChapter } from "../codex/SaveChapter";
import { coverageLabel, narrativeRule, type Narrative } from "../codex/narrative";

function trace(t: NumberTrace): string {
  if (t.result === null) return "No qualifying letters";
  const parts = t.components?.map((part) => part.steps?.join(" → ")).join(" + ");
  return [parts, t.steps?.join(" → ") ?? t.result].filter(Boolean).join(" → ");
}

export function NumberReading({ state, oracle, narrative }: {
  state: Numerology;
  oracle: Oracle;
  narrative?: Narrative;
}) {
  const {
    result, consent, setConsent, ai, aiBusy, aiError, explain, download, fresh,
    busy, error, calculate,
  } = state;
  const [index, select] = useState(0);
  const [target, setTarget] = useState(result?.target ?? "");
  const sectionHeading = useId();
  if (!result) return null;
  const section = narrative?.sections[index];
  const cycles = section?.id === "cycles";
  const values = [
    result.life_path.result,
    result.expression.result,
    result.soul_urge.result,
    result.personality.result,
    result.birthday.original_day,
    result.cycles.year.result,
  ];
  const ruleIds = [...new Set(section?.passages.flatMap(({ rules }) => rules) ?? [])];
  const traces: [string, NumberTrace][] = [
    ["Life Path", result.life_path], ["Expression", result.expression],
    ["Soul Urge", result.soul_urge], ["Personality", result.personality],
    ["Birthday companion", result.birthday.companion], ["Personal Year", result.cycles.year],
    ["Personal Month", result.cycles.month], ["Personal Day", result.cycles.day],
  ];
  return (
    <div className="number-payoff personal-code">
      {narrative && section ? <>
        <nav className="number-chapters" aria-label="Personal Code chapters">
          {narrative.sections.map((item, i) => (
            <button key={item.id} type="button" aria-pressed={index === i} onClick={() => select(i)}>
              {i < values.length && <strong>{values[i] ?? "—"}</strong>}
              <span>{item.title}</span>
            </button>
          ))}
        </nav>
        <section className="number-themes personal-code-section" aria-labelledby={sectionHeading}>
          <header className="personal-code-heading">
            {index < values.length && <strong aria-hidden="true">{values[index] ?? "—"}</strong>}
            <div>
              <h2 id={sectionHeading} aria-live="polite">{section.title}</h2>
              {index > 0 && index < 4 && <p>{result.name.basis === "birth" ? "Birth name" : "Current-name overlay"}</p>}
            </div>
          </header>
          {cycles && <div className="personal-cycle-context">
            <p aria-live="polite">Reading date <time dateTime={result.target}>{result.target}</time></p>
            <p>Personal Year runs from {result.cycles.year_interval[0]} up to {result.cycles.year_interval[1]}.</p>
            <form onSubmit={(event) => {
              event.preventDefault();
              if (target !== result.target) void calculate(target);
            }}>
              <label>Explore a different date
                <input type="date" required min="0001-01-01" max="9998-12-31"
                  value={target} onChange={(event) => setTarget(event.target.value)} />
              </label>
              <button type="submit" className="secondary" disabled={busy || target === result.target}>
                {busy ? "Updating cycles…" : "Update cycles"}
              </button>
              {error && <p role="alert" className="error">{error}</p>}
            </form>
          </div>}
          <div className={cycles ? "number-cycle-passages" : "number-prose"}>
            {section.passages.map((passage) => (
              <article key={passage.title} className="personal-code-passage">
                <h3>{passage.title}</h3>
                <p>{passage.text}</p>
                <small>{coverageLabel[passage.coverage]}</small>
              </article>
            ))}
          </div>
          <details key={section.id} className="provenance">
            <summary>Sources and scope</summary>
            <div className="detail-body">
              {ruleIds.map((id) => {
                const rule = narrativeRule(narrative.edition, id)!;
                return <div key={id}>
                  <a href={rule.url} target="_blank" rel="noreferrer">{rule.locator}</a>
                  <p className="rule-reference">{rule.edition} · {id}</p>
                  {rule.exceptions.map((exception) => <p key={exception}>{exception}</p>)}
                </div>;
              })}
            </div>
          </details>
        </section>
      </> : <p role="status">The interpretation edition is unavailable. You can still export the calculation.</p>}
      <details className="provenance number-calculations">
        <summary>Calculation traces and conventions</summary>
        <div className="detail-body">
          <p>{result.profile} · {result.name.basis} name basis.</p>
          <dl>
            {traces.map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{trace(value)}</dd></div>)}
          </dl>
          <p>Core reductions preserve 11, 22 and 33. Calendar cycles reduce to a single digit. The name calculation uses the Y roles you chose and joins letters across internal hyphens and apostrophes.</p>
          <p>These symbolic readings leave personality diagnoses and event forecasts outside the edition.</p>
        </div>
      </details>
      <SaveChapter oracle={oracle} result={result} kind="numerology" narrative={narrative} />
      {result.name.basis === "birth" && <section className="number-ai">
        <h2>Optional Gemini commentary</h2>
        <p>
          Gemini can expand the Expression and Personal Year themes. It receives
          those themes and their sources. Your name and dates stay out of the
          provider prompt.
        </p>
        {oracle.gemini ? (
          <>
            <label className="consent">
              <input
                type="checkbox"
                checked={consent}
                onChange={(e) => setConsent(e.target.checked)}
              />{" "}
              I consent to sending these symbolic themes to Google Gemini.
            </label>
            <button
              className="secondary"
              disabled={!consent || aiBusy}
              onClick={() => void explain()}
            >
              {aiBusy
                ? "Considering your themes…"
                : "Request Gemini commentary"}
            </button>
          </>
        ) : (
          <p className="scope-note">
            Gemini is not configured on this server. Your complete native
            reading is available above.
          </p>
        )}
        {aiError && (
          <p role="alert" className="error">
            {aiError}
          </p>
        )}
        {ai && (
          <div className="ai-commentary">
            <p className="eyebrow">
              EXPERIMENTAL AI COMMENTARY · NOT NATIVE ENGINE OUTPUT
            </p>
            {ai.themes.map((t) => (
              <p key={t.scope}>{t.reflection}</p>
            ))}
            <p className="scope-note">
              {ai.provenance.provider} · {ai.provenance.model}. Reference checks
              do not guarantee semantic accuracy.
            </p>
          </div>
        )}
      </section>}
      <div className="reading-actions">
        <button className="secondary" onClick={download}>Export native reading</button>
        <button className="secondary" onClick={fresh} disabled={busy}>Explore another name</button>
        <button className="text-button" onClick={() => oracle.navigate("explore")}>Return to the Gallery</button>
      </div>
      <p className="scope-note">The native download includes the entered name, dates and letter trace.</p>
    </div>
  );
}
