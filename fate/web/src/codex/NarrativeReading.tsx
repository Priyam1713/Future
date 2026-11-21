import { useId, useState, type ReactNode } from "react";
import { oracleLabel, ROOMS } from "../chambers/contracts";
import { coverageLabel, narrativeRule, narrativeScope, type Narrative } from "./narrative";

export function NarrativeReading({ narrative, title, context, illustration }: {
  narrative: Narrative;
  title: string;
  context: string;
  illustration: ReactNode;
}) {
  const [active, setActive] = useState(0);
  const heading = useId();
  const sectionLabel = useId();
  const { sections, edition, technique } = narrative;
  const section = sections[active];
  const rules = [...new Set(section.passages.flatMap((passage) => passage.rules))];
  const room = technique === 1 ? "western" : technique === 4 ? "numerology" : ROOMS[technique].slug;
  return (
    <div className={`narrative-folio chamber-folio chamber-${room}`} data-motion="still">
      <header className="folio-heading">
        <p className="eyebrow">{technique === 1 ? "WESTERN ASTROLOGY" : oracleLabel(technique)}</p>
        <h2 tabIndex={-1}>{title}</h2>
        <p>{context}</p>
      </header>
      <nav className="narrative-navigation" aria-label="Saved reading sections">
        <label><span id={sectionLabel}>Reading section</span>
          <select aria-labelledby={sectionLabel} value={active}
            onChange={(event) => setActive(Number(event.target.value))}>
            {sections.map(({ id, title }, i) => <option key={id} value={i}>{title}</option>)}
          </select>
        </label>
        {sections.length > 1 && <div>
          <button className="text-button" disabled={!active} onClick={() => setActive(active - 1)}>Previous section</button>
          <button className="text-button" disabled={active === sections.length - 1} onClick={() => setActive(active + 1)}>Next section</button>
        </div>}
      </nav>
      <div className="folio-mobile-art">
        <details className="chamber-depth narrative-illustration">
          <summary>{technique === 4 ? "Number illustration" : "Chart illustration"}</summary>
          {illustration}
        </details>
      </div>
      <section className="narrative-section" aria-labelledby={heading}>
        <h3 id={heading} aria-live="polite">{section.title}</h3>
        {section.passages.map((passage, i) => (
          <article key={i} className="narrative-passage">
            <h4>{passage.title}</h4>
            <p>{passage.text}</p>
            <small>{coverageLabel[passage.coverage]}</small>
          </article>
        ))}
        <details className="chamber-depth" key={section.id}>
          <summary>Sources and scope</summary>
          {rules.map((id) => {
            const ref = narrativeRule(edition, id)!;
            return <blockquote key={id}>
              {ref.text && <p>{ref.text}</p>}
              <cite>{ref.url ? <a href={ref.url} target="_blank" rel="noreferrer">{ref.locator}</a> : ref.locator}</cite>
              <p>{ref.edition} · {id}</p>
              {ref.exceptions.map((exception) => <p key={exception}>{exception}</p>)}
            </blockquote>;
          })}
          <p>{narrativeScope[technique]}</p>
        </details>
      </section>
      <p className="folio-scope">Interpretation edition · {edition}</p>
    </div>
  );
}
