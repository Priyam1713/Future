import { ArrowLeft, ArrowRight, ChevronDown, Download } from "lucide-react";
import type { Oracle } from "../hooks/useOracle";
import { ConnectedSpread } from "../components/ConnectedSpread";
import { GeminiCommentary } from "../components/GeminiCommentary";
import { SaveChapter } from "../codex/SaveChapter";
import { tarotSnapshot } from "../codex/records";
import { matchesLiveStory, tarotStory } from "../experiences/tarotStory";

export default function ReadingScreen({ oracle }: { oracle: Oracle }) {
  const { heading, navigate, result, download, fresh } = oracle;
  if (!result) return null;
  const snapshot = tarotSnapshot(result);
  const narrative = matchesLiveStory(result, snapshot) ? tarotStory(snapshot) : undefined;
  return (
    <div className="reading page-enter narrow tarot-folio finished-material connected-reading">
      <div className="journey-top">
        <button className="text-button" onClick={() => navigate("ritual")}>
          <ArrowLeft size={15} /> Your cards
        </button>
        <span className="eyebrow">Tarot</span>
      </div>
      <div className="page-heading">
        <h1 ref={heading} tabIndex={-1}>The story in <em>your cards.</em></h1>
      </div>
      {result.question && <p className="question-echo">“{result.question}”</p>}
      {narrative ? <ConnectedSpread snapshot={snapshot} narrative={narrative} />
        : <p role="status">The connected edition is unavailable. You can still download the native reading.</p>}
      <SaveChapter oracle={oracle} result={result} kind="tarot" narrative={narrative} />
      <details className="provenance">
        <summary>Sources, conventions & limits <ChevronDown size={16} /></summary>
        <div className="detail-body">
          <p>{result.source.edition}</p>
          <p>Art from Pamela Colman Smith’s 1910 Pam-A illustrations with FATE’s original card back.</p>
          <p>Draw protocol {result.replay.protocol}.</p>
          <p className="seed">Replay seed: {result.replay.seed}</p>
          <ul>{result.limitations.map((limit) => <li key={limit}>{limit}</li>)}</ul>
          <p>{result.predictive_validity}</p>
          <p>{result.source.rights_note}</p>
        </div>
      </details>
      <GeminiCommentary oracle={oracle} />
      <div className="reading-actions">
        <button className="secondary" onClick={download}><Download size={16} /> Export native reading</button>
        <button className="primary" onClick={fresh}>Begin another chapter <ArrowRight size={16} /></button>
      </div>
      <p className="scope-note">The native export includes your original question and replay data.</p>
      <div className="reading-actions">
        <button className="text-button" onClick={() => navigate("numerology")}>Explore Numerology</button>
        <button className="text-button" onClick={() => navigate("explore")}>Return to the Gallery</button>
      </div>
    </div>
  );
}
