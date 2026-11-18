import { ArrowLeft } from "lucide-react";
import CardArt from "../CardArt";
import type { Oracle } from "../hooks/useOracle";
import { Intention } from "../components/Intention";
import { CardReveal } from "../components/CardReveal";
export default function RitualScreen({ oracle }: { oracle: Oracle }) {
  const { heading, navigate, result } = oracle;
  return (
    <div className="ritual page-enter narrow">
      <div className="journey-top">
        <button className="text-button" onClick={() => navigate("explore")}>
          <ArrowLeft size={15} /> Explore
        </button>
        <span className="eyebrow">
          01 <span className="journey-line" />{" "}
          {result ? "REVEAL" : "THE RITUAL"}
        </span>
      </div>
      <div className="page-heading">
        <p className="eyebrow">THE TAROT · WAITE TRADITION</p>
        <h1 ref={heading} tabIndex={-1}>
          {result ? (
            "A moment of revelation."
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
            ? "Turn each card. Notice what speaks to you."
            : "Bring a question, or simply bring yourself."}
        </p>
      </div>
      {!result ? <Intention oracle={oracle} /> : <CardReveal oracle={oracle} />}
    </div>
  );
}
