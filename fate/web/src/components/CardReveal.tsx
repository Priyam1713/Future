import { ArrowRight } from "lucide-react";
import CardArt from "../CardArt";
import { PhysicalCard } from "./PhysicalCard";
import { plainThemes } from "../experiences/tarotPresentation";
import type { Oracle } from "../hooks/useOracle";
export function CardReveal({ oracle }: { oracle: Oracle }) {
  const { result, revealed, reveal, allRevealed, readAll, reduced, paused } =
    oracle;
  if (!result) return null;
  return (
    <>
      {result.question && <p className="question-echo">“{result.question}”</p>}
      <div
        className={`reveal-spread card-table count-${result.readings.length}`}
      >
        {result.readings.map((r, i) => (
          <div className="reveal-slot" key={r.card.id}>
            <p className="position-label">
              {r.position.label}
            </p>
            <PhysicalCard still={reduced || paused}>
              <button
                className={`flip-card tactile ${revealed.includes(i) ? "flipped" : ""}`}
                aria-label={
                  revealed.includes(i)
                    ? `${r.card.name}, ${r.orientation}`
                    : `Reveal card ${i + 1}`
                }
                aria-pressed={revealed.includes(i)}
                onClick={() => reveal(i)}
              >
                <span className="flip-inner">
                  <span
                    className="card-face card-back"
                    aria-hidden={revealed.includes(i)}
                  >
                    <CardArt back />
                  </span>
                  <span
                    className="card-face card-front"
                    aria-hidden={!revealed.includes(i)}
                  >
                    <span
                      className={
                        r.orientation === "reversed" ? "reversed-art" : ""
                      }
                    >
                      <CardArt card={r.card} />
                    </span>
                  </span>
                </span>
              </button>
            </PhysicalCard>
            <div
              className={`card-caption ${revealed.includes(i) ? "visible" : ""}`}
              aria-hidden={!revealed.includes(i)}
            >
              <h2>{revealed.includes(i) ? r.card.name : "Unrevealed"}</h2>
              <p>{revealed.includes(i) ? r.orientation : "Tap to turn"}</p>
            </div>
          </div>
        ))}
      </div>
      <div className="ritual-status" role="status" aria-live="polite">
        {allRevealed
          ? "Your cards are open."
          : `${revealed.length} of ${result.readings.length} cards open`}
      </div>
      {revealed.length > 0 && (
        <div
          className="reveal-insight artifact-arrival"
          key={revealed.at(-1)}
          aria-live="polite"
        >
          <span className="eyebrow">
            {result.readings[revealed.at(-1)!].position.label}
          </span>
          <p>{plainThemes(result.readings[revealed.at(-1)!])}</p>
        </div>
      )}
      <div className="ritual-actions">
        <button
          className={allRevealed ? "primary" : "secondary"}
          onClick={readAll}
        >
          {allRevealed ? "Open my reading" : "Skip reveal & read now"}{" "}
          <ArrowRight size={17} />
        </button>
      </div>
    </>
  );
}
