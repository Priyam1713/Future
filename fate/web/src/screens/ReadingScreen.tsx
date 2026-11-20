import { ArrowLeft, ArrowRight, ChevronDown, Download } from "lucide-react";
import CardArt from "../CardArt";
import type { Oracle } from "../hooks/useOracle";
import { ReadingDetails } from "../components/ReadingDetails";
import { GeminiCommentary } from "../components/GeminiCommentary";
import { plainThemes } from "../experiences/tarotPresentation";
import { SaveChapter } from "../codex/SaveChapter";
import { ReadingConclusion } from "../components/ReadingConclusion";
export default function ReadingScreen({ oracle }: { oracle: Oracle }) {
  const { heading, navigate, result, download, fresh } = oracle;
  if (!result) return null;
  return (
    <div className="reading page-enter narrow tarot-folio finished-material">
      <div className="journey-top">
        <button className="text-button" onClick={() => navigate("ritual")}>
          <ArrowLeft size={15} /> Your cards
        </button>
        <span className="eyebrow">
          02 <span className="journey-line" /> THE READING
        </span>
      </div>
      <div className="page-heading">
        <h1 ref={heading} tabIndex={-1}>
          The story in <em>your cards.</em>
        </h1>
      </div>
      {result.question && <p className="question-echo">“{result.question}”</p>}
      <section
        className="reading-summary artifact-arrival"
        aria-labelledby="themes-title"
      >
        <h2 id="themes-title">Threads to follow</h2>
        <div className="tarot-payoff">
          {result.readings.map((r) => (
            <div key={r.card.id}>
              <div
                className={`tarot-thumb ${r.orientation === "reversed" ? "reversed-art" : ""}`}
                aria-hidden="true"
              >
                <CardArt card={r.card} />
              </div>
              <div>
                <span>
                  {r.position.label} · {r.orientation}
                </span>
                <h3>{r.card.name}</h3>
                <p>{plainThemes(r)}</p>
              </div>
            </div>
          ))}
        </div>
        <details className="native-motifs">
          <summary>Original source motifs</summary>
          {result.readings.map((r) => (
            <div className="theme-row" key={r.card.id}>
              <span>{r.position.label}</span>
              <strong>
                {r.direct_component.symbolic_focus.split(";").join(" · ")}
              </strong>
            </div>
          ))}
        </details>
        <p className="summary-footnote">
          Source themes, edited for clarity. These are reflection prompts, not
          findings about your life. Alternative source accounts remain separate.
        </p>
      </section>
      <ReadingConclusion
        kind="tarot"
        themes={result.readings.map(plainThemes)}
      />
      <div className="section-label depth-label">
        <span>LOOK A LITTLE DEEPER</span>
        <ChevronDown size={15} />
      </div>
      <ReadingDetails oracle={oracle} />
      <GeminiCommentary oracle={oracle} />
      <details className="provenance">
        <summary>
          Sources, conventions & limits <ChevronDown size={16} />
        </summary>
        <div className="detail-body">
          <p>{result.source.edition}</p>
          <p>
            <strong>Text profile:</strong> {result.profile}
          </p>
          <p>
            <strong>Art:</strong> The Archive Edition: Pamela Colman Smith’s
            complete 1910 Pam-A illustrations, with a new original FATE
            observatory back. Artwork is independent of the Waite 1922 text
            profile.
          </p>
          <p>{result.overall.summary}</p>
          <p>
            <strong>Draw protocol:</strong> {result.replay.protocol}.
            Cryptographically generated local seed; the native engine uses its
            frozen deterministic draw protocol.
          </p>
          <p className="seed">Replay seed: {result.replay.seed}</p>
          <ul>
            {result.limitations.map((l) => (
              <li key={l}>{l}</li>
            ))}
          </ul>
          <p>{result.predictive_validity}</p>
          <p>
            <strong>Engine text-profile rights note:</strong>{" "}
            {result.source.rights_note}
          </p>
        </div>
      </details>
      <SaveChapter oracle={oracle} result={result} kind="tarot" />
      <div className="reading-actions">
        <button className="secondary" onClick={download}>
          <Download size={16} /> Export native reading
        </button>
        <button className="primary" onClick={fresh}>
          Begin another chapter <ArrowRight size={16} />
        </button>
      </div>
      <p className="scope-note">
        Nothing is saved automatically. Native export includes your original
        question and replay data; saving a Codex chapter keeps only the symbols
        and source version.
      </p>
      <div className="next-room">
        <p className="eyebrow">YOUR NEXT DOOR · NUMEROLOGY</p>
        <h2>
          A different kind
          <br />
          of <em>pattern.</em>
        </h2>
        <p>
          Leave the cards for a moment. Explore the symbolic themes in a name
          and a date.
        </p>
        <button
          className="primary"
          onClick={() => oracle.navigate("numerology")}
        >
          Explore Numerology <span aria-hidden="true">↗</span>
        </button>
        <button className="text-button" onClick={() => navigate("explore")}>
          Return to the Gallery
        </button>
      </div>
    </div>
  );
}
