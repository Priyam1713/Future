import { useEffect, useState } from "react";
import {
  RITUAL_ROOMS,
  type RitualNative,
  type RitualSnapshot,
} from "./contracts";
import {
  archive,
  card,
  figure,
  motif,
  passage,
  ritualEvidence,
  ritualTitle,
  titleCase,
} from "./reference";
import { dots } from "./Entries";

const displayText = (text: string) => text.replace(/([,;])(?=\S)/g, "$1 ");

function SourceLink({
  href,
  children,
}: {
  href?: string | null;
  children: React.ReactNode;
}) {
  return href ? (
    <a href={href} target="_blank" rel="noreferrer">
      {children}
    </a>
  ) : (
    <>{children}</>
  );
}
export function SourceDepth({ s }: { s: RitualSnapshot }) {
  return (
    <details className="ritual-depth">
      <summary>Sources & scope</summary>
      {ritualEvidence(s).map((row, i) => (
        <blockquote key={i}>
          <p>{row.wording}</p>
          <cite>
            {row.label} · <SourceLink href={row.url}>{row.locator}</SourceLink>
          </cite>
        </blockquote>
      ))}
      <p>Source edition: {s.profile}</p>
    </details>
  );
}

export function OracleReading({
  s,
  live,
  compact,
  complete,
  cue,
}: {
  s: RitualSnapshot;
  live: boolean;
  compact: boolean;
  complete?: () => void;
  cue?: () => void;
}) {
  const [open, setOpen] = useState<number[]>(
    live ? [] : s.values.map((_, i) => i),
  );
  const [selected, setSelected] = useState(0);
  const active = open.includes(selected) ? card(s.values[selected]) : null;
  const turn = (i: number) => {
    setSelected(i);
    if (open.includes(i)) return;
    const next = [...open, i];
    setOpen(next);
    cue?.();
    if (next.length === s.values.length) complete?.();
  };
  return (
    <div className="oracle-reading">
      <div className={`oracle-line count-${s.values.length}`}>
        {s.values.map((id, i) => {
          const revealed = open.includes(i),
            object = card(id);
          return (
            <button
              className={`oracle-card ${revealed ? "turned" : ""}`}
              key={id}
              type="button"
              disabled={compact}
              aria-pressed={revealed && selected === i}
              aria-label={
                revealed ? `Read ${object.name}` : `Reveal card ${i + 1}`
              }
              data-card={revealed ? id : undefined}
              onClick={() => turn(i)}
            >
              <span className="oracle-card-casing">
                <span className="oracle-card-back" aria-hidden="true">
                  <span>✦</span>
                </span>
                {revealed && (
                  <span className="oracle-card-face">
                    <img
                      src={`/art/ritual-deck/${id}.webp`}
                      alt=""
                      width="384"
                      height="500"
                      draggable="false"
                    />
                    <span>
                      <small>{String(object.number).padStart(2, "0")}</small>
                      {object.name}
                    </span>
                  </span>
                )}
              </span>
            </button>
          );
        })}
      </div>
      {!compact &&
        (active ? (
          <article className="ritual-finding" aria-live="polite">
            <p className="eyebrow">Card {selected + 1} · historical motif</p>
            <h2>{active.name}</h2>
            <p className="ritual-takeaway">
              {displayText(active.meaning.text)}
            </p>
            <details className="ritual-depth">
              <summary>When the source qualifies this meaning</summary>
              <p>{active.meaning.context}</p>
              <SourceLink href={archive.cardSource.url}>
                {active.meaning.locator}
              </SourceLink>
            </details>
          </article>
        ) : (
          <p className="ritual-instruction" role="status">
            Turn a card to read its motif.
          </p>
        ))}
      {!compact && open.length === s.values.length && s.values.length > 1 && (
        <p className="ritual-instruction">
          Read the sequence from left to right and consider what changes from
          one motif to the next.
        </p>
      )}
    </div>
  );
}

function PendulumReading({
  s,
  native,
}: {
  s: RitualSnapshot;
  native?: RitualNative;
}) {
  const [mode, response] = s.values;
  return (
    <article className="pendulum-answer ritual-finding">
      <div className="pendulum-medal" aria-hidden="true">
        <span>
          {response === "unresolved" ? "◇" : response === "yes" ? "✦" : "◈"}
        </span>
      </div>
      <div>
        <p className="eyebrow">
          {mode === "seeded"
            ? "Seeded digital symbol"
            : "From your reported movement"}
        </p>
        <h2>{titleCase(response)}</h2>
        <p className="ritual-takeaway">
          {displayText(
            native?.reflection?.text ??
              (response === "unresolved"
                ? "Keep the question open."
                : "A symbolic response for reflection."),
          )}
        </p>
        {native?.outcome?.reasons.length ? (
          <details className="ritual-depth">
            <summary>Why the category remained unresolved</summary>
            <ul>
              {native.outcome.reasons.map((reason) => (
                <li key={reason}>
                  {titleCase(reason.replace("observation_", "Observation: "))}
                </li>
              ))}
            </ul>
          </details>
        ) : null}
      </div>
    </article>
  );
}

type NotebookRow = {
  user_record?: { description?: string; experience_type?: string };
};
function journalNotes(native?: RitualNative) {
  const data = native?.journal;
  if (Array.isArray(data))
    return (data as NotebookRow[])
      .map((row) => row.user_record?.description ?? "")
      .filter(Boolean);
  if (data && typeof data === "object" && "record" in data) {
    const record = data.record;
    if (
      record &&
      typeof record === "object" &&
      "narrative" in record &&
      typeof record.narrative === "string"
    )
      return [record.narrative];
  }
  return [];
}
function JournalReading({
  id,
  native,
}: {
  id: 21 | 22;
  native?: RitualNative;
}) {
  const notes = journalNotes(native);
  const rows = Array.isArray(native?.journal)
    ? (native.journal as NotebookRow[])
    : [];
  return (
    <article className="ritual-finding journal-reading">
      <p className="eyebrow">
        {id === 21 ? "Crystal gazing" : "Mirror reflection"} ·{" "}
        {native ? "your journal" : "bookmarked guide"}
      </p>
      <h2>
        {native
          ? rows.length
            ? "Your observations"
            : "An open, unmarked page"
          : "Return to the guide"}
      </h2>
      {native &&
        rows.map((row, i) => (
          <div className="private-quote" key={i}>
            <small>
              {titleCase(
                row.user_record?.experience_type ?? "Unclassified observation",
              )}
            </small>
            {row.user_record?.description && (
              <p>{row.user_record.description}</p>
            )}
          </div>
        ))}
      {native && !rows.length && (
        <p>You closed this visit without recording an observation.</p>
      )}
      {!native && <p>This bookmark keeps the reference guide only.</p>}
      <details className="ritual-depth">
        <summary>Read the guide from this room</summary>
        <ol>
          {archive.guides[id].steps.map((step) => (
            <li key={step.id}>
              <strong>{titleCase(step.id)}</strong> · {step.text}
            </li>
          ))}
        </ol>
      </details>
      {notes.length > 0 && (
        <p className="scope-note">
          These words were entered by you during this visit.
        </p>
      )}
    </article>
  );
}

const statuses: Record<string, string> = {
  conditional_reference: "Matches chosen context",
  missing_context: "Context left open",
  polysemous_reference: "Several historical readings",
  conflicting_references: "Several conditions match",
  conditions_not_met: "Conditions differ",
};
function DreamReading({
  s,
  native,
}: {
  s: RitualSnapshot;
  native?: RitualNative;
}) {
  const notes = journalNotes(native);
  return (
    <div className="dream-reading">
      <p className="eyebrow">Artemidorus · historical references</p>
      <h2>
        {s.values.length ? "The motifs you chose" : "A page without a lookup"}
      </h2>
      {s.values.map((id) => {
        const lookup =
          native?.motif_references?.find((row) => row.motif_id === id) ??
          motif(id);
        const cases = native ? lookup.selected_cases : lookup.reference.cases;
        return (
          <article className="dream-reference" key={id} data-motif={id}>
            <div>
              <h3>{titleCase(id)}</h3>
              <p className="eyebrow">
                {native ? statuses[lookup.status] : "Reference bookmark"}
              </p>
            </div>
            <p>
              {native && cases.length === 1
                ? displayText(cases[0].historical_account)
                : cases.length > 1
                  ? "Artemidorus gives " +
                    cases.length +
                    " historical accounts for this motif."
                  : displayText(lookup.reference.definition)}
            </p>
            {cases.length > 0 && (
              <details className="ritual-depth">
                <summary>
                  {cases.length === 1
                    ? "Historical account"
                    : "Historical accounts"}
                </summary>
                <ul>
                  {cases.map((item) => (
                    <li key={item.id}>{item.historical_account}</li>
                  ))}
                </ul>
                <SourceLink href={archive.dream.source.url}>
                  {lookup.reference.provenance.locator}
                </SourceLink>
              </details>
            )}
            {native && lookup.missing_context.length > 0 && (
              <p className="ritual-measure">
                Unspecified: {lookup.missing_context.map(titleCase).join(", ")}.
              </p>
            )}
          </article>
        );
      })}
      {!s.values.length && (
        <p>You can leave your words on their own, without assigning a motif.</p>
      )}
      {notes.length > 0 && (
        <details className="ritual-depth">
          <summary>My dream notes for this visit</summary>
          <p className="private-quote">{notes[0]}</p>
        </details>
      )}
    </div>
  );
}

function Shield({
  s,
  native,
  compact,
  still,
  complete,
}: {
  s: RitualSnapshot;
  native?: RitualNative;
  compact: boolean;
  still: boolean;
  complete?: () => void;
}) {
  const [selected, setSelected] = useState(14);
  const current = figure(s.values[selected]),
    trace = native?.positions?.[selected];
  useEffect(() => {
    if (!native) return;
    if (still) {
      complete?.();
      return;
    }
    const timeout = setTimeout(() => complete?.(), 1360);
    return () => clearTimeout(timeout);
  }, [native, still, complete]);
  const tiers = [[7, 6, 5, 4, 3, 2, 1, 0], [11, 10, 9, 8], [13, 12], [14]];
  const role = (i: number) =>
    i < 4
      ? "Mother"
      : i < 8
        ? "Daughter"
        : i < 12
          ? "Niece"
          : i < 14
            ? "Witness"
            : "Judge";
  const groups = compact ? [[14]] : tiers;
  return (
    <div className="shield-view">
      <div
        className={`shield-table ${native && !still ? "shield-forming" : ""}`}
      >
        {groups.map((tier, i) => (
          <div className="shield-tier" key={i}>
            {tier.map((index) => (
              <button
                key={index}
                type="button"
                className="shield-figure"
                data-position={index + 1}
                data-pattern={s.values[index]}
                aria-label={`${role(index)} ${index + 1}: ${figure(s.values[index]).name}`}
                aria-pressed={selected === index}
                disabled={compact}
                onClick={() => setSelected(index)}
                style={{ "--delay": index * 68 + "ms" } as React.CSSProperties}
              >
                <small>{index + 1}</small>
                {Array.from(s.values[index], (n, j) => (
                  <span key={j}>{dots(Number(n))}</span>
                ))}
              </button>
            ))}
          </div>
        ))}
      </div>
      {!compact && (
        <article className="ritual-finding">
          <p className="eyebrow">
            {role(selected)} · position {selected + 1}
          </p>
          <h2>{current.name}</h2>
          <p className="ritual-takeaway">
            {selected < 4
              ? "One of your four hand-set figures."
              : selected < 8
                ? "This figure reads a single row across the four Mothers."
                : "This figure combines two parents, row by row, by odd and even parity."}
          </p>
          {selected === 14 && (
            <p>The Judge is the final result of the shield construction.</p>
          )}
          {trace && (
            <details className="ritual-depth">
              <summary>Trace the rows and parents</summary>
              <p>
                {titleCase(trace.operation)}{" "}
                {trace.parents.length
                  ? "· parents " + trace.parents.join(", ")
                  : ""}
              </p>
              <ol>
                {trace.line_trace.map((r, i) => (
                  <li key={i}>
                    {r.inputs
                      ? `${r.inputs.join(" + ")} = ${r.sum} → ${r.result}`
                      : `Mother ${r.parent}, row ${r.parent_row} → ${r.dot_count}`}
                  </li>
                ))}
              </ol>
              <SourceLink href={archive.geo.source.url}>
                {current.locator}
              </SourceLink>
            </details>
          )}
        </article>
      )}
    </div>
  );
}

function BookReading({
  s,
  native,
  compact,
}: {
  s: RitualSnapshot;
  native?: RitualNative;
  compact: boolean;
}) {
  const rows =
    native?.selections ??
    s.values.slice(1).map((id) => passage(id, Number(s.values[0])));
  return (
    <div className="selected-book">
      {rows.map((row, i) => (
        <article className="book-leaf" key={i} data-sentence={row.sentence_id}>
          <p className="eyebrow">
            Your chosen passage · World English Bible Classic
          </p>
          <h2>{row.citation}</h2>
          <blockquote>{row.text}</blockquote>
          {!compact && (
            <details className="ritual-depth">
              <summary>Nearby sentences & edition</summary>
              {row.context_before.map((p) => (
                <p key={p.sentence_id}>
                  <small>{p.citation}</small> {p.text}
                </p>
              ))}
              {row.context_after.map((p) => (
                <p key={p.sentence_id}>
                  <small>{p.citation}</small> {p.text}
                </p>
              ))}
              <p>
                <SourceLink href={row.source_url}>
                  Open {row.citation} in the pinned edition
                </SourceLink>
              </p>
            </details>
          )}
        </article>
      ))}
    </div>
  );
}
export function RitualReading({
  s,
  native,
  compact = false,
  still = true,
  complete,
  cue,
}: {
  s: RitualSnapshot;
  native?: RitualNative;
  compact?: boolean;
  still?: boolean;
  complete?: () => void;
  cue?: () => void;
}) {
  switch (s.oracle) {
    case 17:
      return (
        <OracleReading
          s={s}
          live={!!native}
          compact={compact}
          complete={complete}
          cue={cue}
        />
      );
    case 20:
      return <PendulumReading s={s} native={native} />;
    case 21:
    case 22:
      return compact ? (
        <div className="guide-medallion">◇</div>
      ) : (
        <JournalReading id={s.oracle} native={native} />
      );
    case 23:
      return compact ? (
        <div className="guide-medallion">☾</div>
      ) : (
        <DreamReading s={s} native={native} />
      );
    case 33:
      return (
        <Shield
          s={s}
          native={native}
          compact={compact}
          still={still}
          complete={complete}
        />
      );
    case 36:
      return <BookReading s={s} native={native} compact={compact} />;
  }
}

export function RitualChapter({
  s,
  index,
}: {
  s: RitualSnapshot;
  index: number;
}) {
  return (
    <div
      className={`ritual-folio ritual-${RITUAL_ROOMS[s.oracle].slug}`}
      data-ritual-still="true"
    >
      <header className="folio-heading">
        <p className="eyebrow">
          Chapter {index + 1} · {RITUAL_ROOMS[s.oracle].name}
        </p>
        <h2 tabIndex={-1}>{ritualTitle(s)}</h2>
      </header>
      <RitualReading s={s} />
      <SourceDepth s={s} />
    </div>
  );
}
