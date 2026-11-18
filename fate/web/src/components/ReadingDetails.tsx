import { ArrowUpRight, ChevronDown } from "lucide-react";
import CardArt from "../CardArt";
import type { Oracle } from "../hooks/useOracle";
export function ReadingDetails({ oracle }: { oracle: Oracle }) {
  const { result } = oracle;
  if (!result) return null;
  return (
    <>
      {result.readings.map((r, i) => (
        <section className="interpretation" key={r.card.id}>
          <div className="interpretation-heading">
            <span className="chapter-number">0{i + 1}</span>
            <div>
              <span className="eyebrow">{r.position.label}</span>
              <h2>{r.card.name}</h2>
            </div>
            <span className="orientation-pill">{r.orientation}</span>
          </div>
          <p className="reflection">
            {r.composition.reflection.replaceAll(";", ", ")}
          </p>
          <details>
            <summary>
              The traditional meaning <ChevronDown size={16} />
            </summary>
            <div className="detail-body">
              <p className="source-label">HISTORICAL WORDING · WAITE, 1922</p>
              <blockquote>{r.direct_component.text}</blockquote>
              <a
                href={r.direct_component.page_url}
                target="_blank"
                rel="noreferrer"
              >
                {r.direct_component.locator} <ArrowUpRight size={12} />
              </a>
              {r.upright_reference && (
                <>
                  <p className="source-label">
                    UPRIGHT REFERENCE FOR THIS REVERSAL
                  </p>
                  <p>{r.upright_reference.text}</p>
                </>
              )}
              <p className="source-caution">
                Historical language may contain claims about health, appearance
                or fate. It is recorded as doctrine, never a finding about you.
              </p>
              {r.additional_source_account && (
                <details className="nested-detail">
                  <summary>
                    Separate source account <ChevronDown size={14} />
                  </summary>
                  <p>{r.additional_source_account.text}</p>
                  <small>
                    {r.additional_source_account.locator} · retained separately,
                    not applied to this reading.
                  </small>
                </details>
              )}
              {r.ambiguity.length > 0 && (
                <ul className="source-flags">
                  {r.ambiguity.map((v) => (
                    <li key={v}>{v.replaceAll("_", " ")}</li>
                  ))}
                </ul>
              )}
              <p className="rule-reference">
                {r.direct_component.rule_id} · v{r.direct_component.version}
              </p>
            </div>
          </details>
        </section>
      ))}
    </>
  );
}
