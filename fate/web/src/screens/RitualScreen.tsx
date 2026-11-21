import { ArrowLeft } from "lucide-react";
import type { Oracle } from "../hooks/useOracle";
import { Intention } from "../components/Intention";
import { CardReveal } from "../components/CardReveal";
export default function RitualScreen({ oracle }: { oracle: Oracle }) {
  const { heading, navigate, result } = oracle;
  return (
    <div
      className={`ritual page-enter narrow finished-material ${result ? "tarot-turning" : ""}`}
    >
      <div className="journey-top">
        <button className="text-button" onClick={() => navigate("explore")}>
          <ArrowLeft size={15} /> Explore
        </button>
        <span className="eyebrow">{result ? "Cards drawn" : "Tarot"}</span>
      </div>
      <div className="page-heading">
        <p className="eyebrow">THE TAROT · WAITE TRADITION</p>
        <h1 ref={heading} tabIndex={-1}>
          {result ? (
            <>
              Turn <em>your cards.</em>
            </>
          ) : (
            <>
              Make room for
              <br />
              <em>a little clarity.</em>
            </>
          )}
        </h1>
        <p>
          {result
            ? "Turn the cards to see their positions and orientations."
            : "Choose a single focus or a connected three-card reading."}
        </p>
      </div>
      {!result ? <Intention oracle={oracle} /> : <CardReveal oracle={oracle} />}
    </div>
  );
}
