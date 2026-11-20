import { ArrowUpRight, LoaderCircle, X } from "lucide-react";
import type { Oracle } from "../hooks/useOracle";
export function GeminiCommentary({ oracle }: { oracle: Oracle }) {
  const {
    result,
    ai,
    setAi,
    setConsent,
    gemini,
    consent,
    aiBusy,
    explain,
    aiError,
  } = oracle;
  if (!result) return null;
  return (
    <section className="ai-section">
      <div className="ai-heading">
        <span className="eyebrow">Optional commentary</span>
      </div>
      <h2>A gentler way into the symbols.</h2>
      <p>Explore the card themes in everyday language.</p>
      {ai ? (
        <div className="commentary" aria-live="polite">
          {ai.cards.map((c, i) => (
            <div key={c.card_id}>
              <h3>{result.readings[i].card.name}</h3>
              <p>{c.reflection}</p>
            </div>
          ))}
          <details className="source-caution">
            <summary>Commentary details</summary>
            <p>
              AI commentary may be mistaken. {ai.provenance.provider} ·{" "}
              {ai.provenance.model}
            </p>
            {ai.cards.map((c) => (
              <p key={c.card_id}>{c.rule_id}</p>
            ))}
          </details>
          <button
            className="text-button"
            onClick={() => {
              setAi(null);
              setConsent(false);
            }}
          >
            Dismiss commentary <X size={14} />
          </button>
        </div>
      ) : gemini ? (
        <>
          <label className="check-label">
            <input
              type="checkbox"
              checked={consent}
              onChange={(e) => setConsent(e.target.checked)}
              disabled={aiBusy}
            />
            <span>
              I agree to send my question, cards and source meanings to Google
              Gemini for this explanation.
            </span>
          </label>
          <button
            className="secondary"
            disabled={!consent || aiBusy}
            onClick={() => void explain()}
          >
            {aiBusy ? (
              <>
                <LoaderCircle size={16} className="spin" /> Listening to the
                symbols…
              </>
            ) : (
              <>
                Explain my reading <ArrowUpRight size={16} />
              </>
            )}
          </button>
          {aiError && (
            <p className="error" role="alert">
              {aiError}
            </p>
          )}
        </>
      ) : (
        <p className="availability">Optional commentary is unavailable.</p>
      )}
    </section>
  );
}
