import { useId, useState } from "react";
import CardArt from "../CardArt";
import { coverageLabel, narrativeRule, type Narrative } from "../codex/narrative";
import { cardReference, type TarotSnapshot } from "../experiences/tarotEdition";
import { ReadingDetails } from "./ReadingDetails";

export function ConnectedSpread({ snapshot, narrative }: { snapshot: TarotSnapshot; narrative: Narrative }) {
  const [selected, select] = useState(0);
  const selectedHeading = useId();
  const overviewHeading = useId();
  const [overview, ...sections] = narrative.sections;
  const connections = sections.find((section) => section.id === "relationships");
  const closing = sections.find((section) => section.id === "closing");
  return (
    <div className={`connected-spread count-${snapshot.cards.length}`}>
      <div className="connected-cards">
        <div className="connected-table" role="group" aria-label="Explore cards in spread order">
        {snapshot.cards.map((pick, index) => {
          const card = cardReference(pick.id);
          return <button key={pick.id} type="button" aria-pressed={selected === index}
            aria-label={`${sections[index].title}, ${card.name}, ${pick.orientation}`}
            data-card={pick.id} data-orientation={pick.orientation} onClick={() => select(index)}>
            <span className="connected-position-label">{sections[index].title}</span>
            <span className={`connected-card-art ${pick.orientation === "reversed" ? "reversed-art" : ""}`} aria-hidden="true">
              <CardArt card={card} />
            </span>
            <strong>{card.name}</strong>
            <small>{pick.orientation}</small>
          </button>;
        })}
        </div>
        <ReadingDetails pick={snapshot.cards[selected]} section={sections[selected]} heading={selectedHeading} />
      </div>
      <div className="connected-copy">
        <section className="spread-overview" aria-labelledby={overviewHeading}>
          <h2 id={overviewHeading}>{overview.title}</h2>
          <p className="spread-passage">{overview.passages[0].text}</p>
        </section>
        {connections && <section className="spread-connections">
          <h3>{connections.title}</h3>
          {connections.passages.map((passage) => <div key={[passage.title, ...passage.rules].join(" ")} className="spread-connection">
            <h4>{passage.title}</h4>
            <p className="spread-passage">{passage.text}</p>
            {passage.coverage === "direct" && <small>{coverageLabel.direct}</small>}
          </div>)}
        </section>}
        {closing && <section className="spread-closing">
          <h3>{closing.title}</h3>
          <p className="spread-passage">{closing.passages[0].text}</p>
        </section>}
        <details className="spread-provenance">
          <summary>How the spread is read</summary>
          <p>The connected passages use FATE’s editorial positions. Historical recurrence entries have a separate source label.</p>
          {connections?.passages.flatMap((p) => p.coverage === "direct" ? p.rules : []).map((id) => {
            const source = narrativeRule(narrative.edition, id)!;
            return <p key={id}><a href={source.url} target="_blank" rel="noreferrer">{source.locator}</a> · {id}</p>;
          })}
          <p>Interpretation edition · {narrative.edition}</p>
        </details>
      </div>
    </div>
  );
}
