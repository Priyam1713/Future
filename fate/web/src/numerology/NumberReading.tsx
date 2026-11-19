import type { Numerology } from "./useNumerology";
import type { Oracle } from "../hooks/useOracle";
import type { NumberTrace } from "../experiences/contracts";
import { SaveChapter } from "../codex/SaveChapter";
import { ReadingConclusion } from "../components/ReadingConclusion";
function trace(t: NumberTrace): string {
  return t.result === null
    ? "No qualifying letters"
    : `${t.components ? `${t.components.map((c) => c.steps?.join(" → ")).join(" + ")} → ` : ""}${t.steps?.join(" → ") ?? t.result}`;
}
export function NumberReading({
  state,
  oracle,
}: {
  state: Numerology;
  oracle: Oracle;
}) {
  const {
    result,
    consent,
    setConsent,
    ai,
    aiBusy,
    aiError,
    explain,
    download,
    fresh,
  } = state;
  if (!result) return null;
  const themes = result.readings.filter((r) => r.coverage === "direct");
  const numbers = [
    { title: "Your birth-date pattern", value: result.life_path },
    { title: "Your inner motivation", value: result.soul_urge },
    { title: "Your outward presentation", value: result.personality },
  ];
  return (
    <div className="number-payoff">
      <section className="number-themes" aria-label="Your symbolic themes">
        {themes.map((theme, i) => (
          <article key={theme.scope}>
            <p className="eyebrow">
              {i === 0
                ? "HOW YOU EXPRESS YOURSELF"
                : `THE RHYTHM OF ${result.target.slice(0, 4)}`}
            </p>
            <div className="number-theme-line">
              <strong>{theme.number}</strong>
              <h2>{theme.text.replace(/\.$/, "")}</h2>
            </div>
            <p>
              {i === 0
                ? "A symbolic lens on the qualities associated with your chosen name."
                : "A calendar-year theme to reflect on, rather than a prediction of events."}
            </p>
            <details>
              <summary>
                Where this theme comes from <span aria-hidden="true">＋</span>
              </summary>
              <div className="detail-body">
                <p>
                  {theme.scope === "expression"
                    ? "Expression"
                    : "Personal Year"}{" "}
                  · Direct source summary
                </p>
                <p>{theme.text}</p>
                <a href={theme.url} target="_blank" rel="noreferrer">
                  World Numerology · {theme.locator}
                </a>
                <p className="rule-reference">{theme.source_id}</p>
              </div>
            </details>
          </article>
        ))}
      </section>
      <ReadingConclusion
        kind="numerology"
        themes={themes.map((t) => t.text.replace(/\.$/, ""))}
      />
      <p className="number-reflection">
        Which of these themes feels useful to carry into your next small
        decision?
      </p>
      <p className="scope-note">
        A reflection prompt from FATE. The themes above are source summaries,
        not findings about your personality or future.
      </p>
      <details className="provenance number-calculations">
        <summary>
          The rest of your constellation <span aria-hidden="true">＋</span>
        </summary>
        <div className="detail-body">
          <p>
            Calculated context. This engine does not supply direct
            number-specific interpretations for these numbers.
          </p>
          {numbers.map((n) => (
            <p key={n.title}>
              <strong>
                {n.title}: {n.value.result ?? "Unavailable"}
              </strong>
              <br />
              {trace(n.value)}
            </p>
          ))}
          <p>
            Birthday: {result.birthday.original_day} · reduced companion{" "}
            {result.birthday.companion.result}
          </p>
          <p>
            Personal month {result.cycles.month.result} · personal day{" "}
            {result.cycles.day.result}. Monthly and daily interpretations are
            outside this profile.
          </p>
        </div>
      </details>
      <details className="provenance">
        <summary>
          Calculation, sources & limits <span aria-hidden="true">＋</span>
        </summary>
        <div className="detail-body">
          <p>
            {result.profile} · {result.name.basis} name basis.
          </p>
          <p>Expression: {trace(result.expression)}</p>
          <p>Personal year: {trace(result.cycles.year)}</p>
          <p>
            Core name/date numbers preserve 11, 22 and 33 during component
            reduction; personal cycles reduce to a single digit. Each Y is
            caller-classified. Hyphen/apostrophe joining is an implementation
            convention.
          </p>
          <p>{result.interpretation_limits}</p>
          {result.limitations.map((l) => (
            <p key={l}>{l}</p>
          ))}
          {result.sources.map((s) => (
            <p key={s.id}>
              <a href={s.url} target="_blank" rel="noreferrer">
                {s.id}
              </a>
              <br />
              {s.locator}
            </p>
          ))}
        </div>
      </details>
      <section className="number-ai">
        <p className="eyebrow">OPTIONAL · ANOTHER VOICE</p>
        <h2>A little more perspective.</h2>
        <p>
          Gemini can expand the two supplied themes. It adds experimental AI
          commentary, separate from your native reading. Only those themes and
          their source references go to Google; your name and dates are omitted
          from the provider prompt.
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
      </section>
      <SaveChapter oracle={oracle} result={result} kind="numerology" />
      <div className="reading-actions">
        <button className="secondary" onClick={download}>
          Export native reading
        </button>
        <button className="secondary" onClick={fresh}>
          Explore another name
        </button>
      </div>
      <div className="next-room">
        <p className="eyebrow">YOUR NEXT DOOR · TAROT</p>
        <h2>
          From numbers
          <br />
          to <em>symbols.</em>
        </h2>
        <p>Carry a theme into the cards and consider it from another angle.</p>
        <button className="primary" onClick={oracle.begin}>
          {oracle.explored.includes(16) ? "Return to Tarot" : "Discover Tarot"}{" "}
          <span aria-hidden="true">↗</span>
        </button>
        <button
          className="text-button"
          onClick={() => oracle.navigate("explore")}
        >
          Return to the Gallery
        </button>
      </div>
    </div>
  );
}
