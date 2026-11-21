import { ArrowUpRight, ChevronDown } from "lucide-react";
import type { ReadingSection } from "../codex/narrative";
import { cardReference, tarotPage, tarotRule, type TarotSnapshot } from "../experiences/tarotEdition";

export function ReadingDetails({ pick, section, heading }: {
  pick: TarotSnapshot["cards"][number];
  section: ReadingSection;
  heading: string;
}) {
  const card = cardReference(pick.id);
  const meaning = card.meanings[pick.orientation];
  const [position, direct] = section.passages;
  const rule = tarotRule(direct.rules[0])!;
  return (
    <section className="interpretation connected-position" aria-labelledby={heading}>
      <div className="interpretation-heading">
        <div>
          <span className="eyebrow">{section.title} · {pick.orientation}</span>
          <h2 id={heading} aria-live="polite">{card.name}</h2>
        </div>
      </div>
      <p className="position-reading">{position.text}</p>
      <details key={meaning.rule_id}>
        <summary>The traditional meaning <ChevronDown size={16} /></summary>
        <div className="detail-body">
          <p className="source-label">WAITE, 1922 · {pick.orientation}</p>
          <blockquote>{direct.text}</blockquote>
          <a href={rule.url} target="_blank" rel="noreferrer">
            {rule.locator} <ArrowUpRight size={12} />
          </a>
          <p className="rule-reference">{meaning.rule_id} · v{meaning.version}</p>
          {rule.exceptions.length > 0 && (
            <ul className="source-flags">
              {rule.exceptions.map((exception) => <li key={exception}>{exception}</li>)}
            </ul>
          )}
          {pick.orientation === "reversed" && (
            <details open className="nested-detail">
              <summary>Upright reference</summary>
              <blockquote>{card.meanings.upright.text}</blockquote>
              <a href={card.meanings.upright.page_url} target="_blank" rel="noreferrer">
                {card.meanings.upright.locator}
              </a>
            </details>
          )}
          {card.additional_meanings && (
            <details className="nested-detail">
              <summary>Separate source account</summary>
              <p>{card.additional_meanings.text}</p>
              <a href={tarotPage(card.additional_meanings.page)} target="_blank" rel="noreferrer">
                {card.additional_meanings.locator}
              </a>
            </details>
          )}
          <p className="source-caution">Historical wording can include claims about health, appearance or fate. Read it as the author’s account.</p>
        </div>
      </details>
    </section>
  );
}
