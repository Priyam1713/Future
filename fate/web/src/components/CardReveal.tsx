import { ArrowRight } from "lucide-react";
import CardArt from "../CardArt";
import { PhysicalCard } from "./PhysicalCard";
import type { Oracle } from "../hooks/useOracle";
export function CardReveal({ oracle }: { oracle: Oracle }) {
  const { result, revealed, reveal, allRevealed, readAll, reduced, paused } =
    oracle;
  if (!result) return null;
  return (
    <>
      {result.question && <p className="question-echo">“{result.question}”</p>}
      <div className={`reveal-spread count-${result.readings.length}`}>
        {result.readings.map((r, i) => (
          <div className="reveal-slot" key={r.card.id}>
            <p className="position-label">
              {String(i + 1).padStart(2, "0")} <span />
              {r.position.label}
            </p>
            <PhysicalCard still={reduced || paused}>
              <button
                className={`flip-card ${revealed.includes(i) ? "flipped" : ""}`}
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
          ? "Your cards are here. Take a breath."
          : `${revealed.length} of ${result.readings.length} revealed · tap a card to turn it`}
      </div>
      {revealed.length > 0 && (
        <div className="reveal-insight" key={revealed.at(-1)}>
          <span className="eyebrow">
            {result.readings[revealed.at(-1)!].position.label}
          </span>
          <p>
            {result.readings[revealed.at(-1)!].direct_component.symbolic_focus
              .split(";")
              .join(" · ")}
          </p>
          <small>Source-derived motifs · a symbolic lens</small>
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
      <p className="scope-note">
        One digital draw, already complete. Turning the cards never changes the
        result.
      </p>
    </>
  );
}
