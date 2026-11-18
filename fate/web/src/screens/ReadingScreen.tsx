import { ArrowLeft, ArrowRight, ChevronDown, Download } from "lucide-react";
import CardArt from "../CardArt";
import type { Oracle } from "../hooks/useOracle";
import { ReadingDetails } from "../components/ReadingDetails";
import { GeminiCommentary } from "../components/GeminiCommentary";
export default function ReadingScreen({ oracle }: { oracle: Oracle }) {
  const { heading, navigate, result, download, fresh } = oracle;
  if (!result) return null;
  return (
    <div className="reading page-enter narrow">
      <div className="journey-top">
        <button className="text-button" onClick={() => navigate("ritual")}>
          <ArrowLeft size={15} /> Your cards
        </button>
        <span className="eyebrow">
          02 <span className="journey-line" /> THE READING
        </span>
      </div>
      <div className="page-heading">
        <p className="eyebrow">A NEW PERSPECTIVE</p>
        <h1 ref={heading} tabIndex={-1}>
          The story in <em>your cards.</em>
        </h1>
        <p>Symbols to sit with. Possibilities to consider.</p>
      </div>
      {result.question && <p className="question-echo">“{result.question}”</p>}
      <div
        className={`reading-art count-${result.readings.length}`}
        aria-hidden="true"
      >
        {result.readings.map((r) => (
          <div
            key={r.card.id}
            className={r.orientation === "reversed" ? "reversed-art" : ""}
          >
            <CardArt card={r.card} />
          </div>
        ))}
      </div>
      <section className="reading-summary" aria-labelledby="themes-title">
        <p className="eyebrow">YOUR READING AT A GLANCE</p>
        <h2 id="themes-title">Threads to follow</h2>
        {result.readings.map((r) => (
          <div className="theme-row" key={r.card.id}>
            <span>{r.position.label}</span>
            <strong>
              {r.direct_component.symbolic_focus.split(";").join(" · ")}
            </strong>
          </div>
        ))}
        <p className="summary-footnote">
          Source-derived motifs, arranged as a reflection. These positions are
          an editorial frame, not evidence of events.
        </p>
      </section>
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
      <div className="reading-actions">
        <button className="secondary" onClick={download}>
          <Download size={16} /> Export native reading
        </button>
        <button className="primary" onClick={fresh}>
          Begin another chapter <ArrowRight size={16} />
        </button>
      </div>
      <p className="scope-note">
        This visit only. Export to keep your reading; nothing is saved
        automatically.
      </p>
    </div>
  );
}
