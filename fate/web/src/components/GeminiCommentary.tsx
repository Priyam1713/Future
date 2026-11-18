import { ArrowUpRight, LoaderCircle, Sparkles, X } from "lucide-react";
import CardArt from "../CardArt";
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
        <Sparkles size={20} />
        <span className="eyebrow">AN OPTIONAL SECOND VOICE</span>
        <span className="experimental">EXPERIMENTAL</span>
      </div>
      <h2>A gentler way into the symbols.</h2>
      <p>
        Ask Gemini to put these source-linked themes into everyday language.
        Your cards and their meanings stay the source of truth.
      </p>
      {ai ? (
        <div className="commentary" aria-live="polite">
          {ai.cards.map((c, i) => (
            <div key={c.card_id}>
              <h3>{result.readings[i].card.name}</h3>
              <p>{c.reflection}</p>
              <small>Grounding: {c.rule_id}</small>
            </div>
          ))}
          <p className="source-caution">
            AI commentary may be mistaken. Refer to the traditional meanings
            above. {ai.provenance.provider} · {ai.provenance.model}
          </p>
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
        <p className="availability">
          Gemini isn’t configured on this instance. Your complete reading is
          available above.
        </p>
      )}
    </section>
  );
}
