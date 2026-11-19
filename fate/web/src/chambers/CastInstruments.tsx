import { useState } from "react";
import type { CoinSnapshot, RuneSnapshot } from "./contracts";
import {
  chamberEvidence,
  coinTexts,
  isMoving,
  runes,
  stone,
} from "./reference";
import { Sources } from "./ChartInstruments";

export function Hexagram({
  values,
  visible = 6,
  changed = false,
}: {
  values: number[];
  visible?: number;
  changed?: boolean;
}) {
  return (
    <div
      className="hexagram"
      role="group"
      aria-label={
        changed
          ? "Relating hexagram, bottom to top"
          : "Initial hexagram, bottom to top"
      }
    >
      {values.map((value, i) => {
        const moving = isMoving(value),
          yang = !!(value % 2) !== (moving && changed);
        return (
          <div
            className="hex-line"
            data-line={i + 1}
            data-value={i < visible ? value : undefined}
            data-state={i >= visible ? "hidden" : yang ? "yang" : "yin"}
            data-moving={i < visible && moving}
            key={i}
            role="img"
            aria-label={
              i >= visible
                ? `Line ${i + 1}, uncast`
                : `Line ${i + 1}, ${yang ? "yang" : "yin"}${moving ? ", changing" : ""}`
            }
          >
            <span />
            <span />
            <i aria-hidden="true">{moving ? "◇" : ""}</i>
          </div>
        );
      })}
    </div>
  );
}

export function Coins({
  s,
  cast,
  compact = false,
  cue,
  complete,
}: {
  s: CoinSnapshot;
  cast?: number[][];
  compact?: boolean;
  cue?: () => void;
  complete?: () => void;
}) {
  const [visible, setVisible] = useState(cast ? 0 : 6),
    [relating, setRelating] = useState(false);
  const { initial, resulting } = coinTexts(s);
  const shown = relating ? resulting : initial;
  const last = cast?.[visible - 1],
    finished = visible === 6;
  const reveal = () => {
    if (finished) return;
    cue?.();
    setVisible(visible + 1);
    if (visible === 5) complete?.();
  };
  return (
    <div className="coin-experience">
      <div className="ink-board">
        <Hexagram values={s.values} visible={visible} changed={relating} />
        {!compact && (
          <div className="ink-caption" aria-live="polite">
            {finished ? (
              <>
                <p className="eyebrow">King Wen {shown.number}</p>
                <h3>{shown.name}</h3>
              </>
            ) : (
              <>
                <p className="eyebrow">A figure drawn from the bottom</p>
                <h3>{visible} of six lines</h3>
              </>
            )}
          </div>
        )}
      </div>
      {!compact && cast && (
        <div className="coin-ritual-area">
          <div
            className="three-coins"
            role="img"
            aria-label={
              last
                ? last.map((bit) => (bit ? "Heads" : "Tails")).join(", ")
                : "Three coins ready"
            }
            key={visible}
          >
            {[0, 1, 2].map((i) => (
              <span
                className={last ? "coin tossed" : "coin"}
                key={i}
                style={{ "--coin-delay": i * 55 + "ms" } as React.CSSProperties}
              >
                <span>{last ? (last[i] ? "H" : "T") : "◇"}</span>
              </span>
            ))}
          </div>
          {!finished && (
            <button className="primary" onClick={reveal}>
              Cast line {visible + 1}
            </button>
          )}
        </div>
      )}
      {!compact && finished && (
        <>
          <div
            className="chamber-switch"
            role="group"
            aria-label="Explore the hexagrams"
          >
            <button aria-pressed={!relating} onClick={() => setRelating(false)}>
              Initial figure
            </button>
            <button
              aria-pressed={relating}
              onClick={() => setRelating(true)}
              disabled={initial.number === resulting.number}
            >
              Relating figure
            </button>
          </div>
          <p className="eyebrow judgment-credit">
            Legge’s 1882 judgment · historical source wording
          </p>
          <blockquote className="chamber-quote" aria-live="polite">
            {shown.judgment.text}
          </blockquote>
          <p>
            {initial.number === resulting.number
              ? "No lines move. The judgment is the single reflection context for this cast."
              : "The relating figure offers a second symbolic context. Each marked line contributes, with no universal priority."}
          </p>
          <Sources
            title="Judgments, changing lines & Legge’s edition"
            rows={chamberEvidence(s)}
          />
        </>
      )}
    </div>
  );
}

export function Stones({
  s,
  drawing = false,
  compact = false,
  cue,
  complete,
}: {
  s: RuneSnapshot;
  drawing?: boolean;
  compact?: boolean;
  cue?: () => void;
  complete?: () => void;
}) {
  const [open, setOpen] = useState<number[]>(
    drawing ? [] : s.runes.map((_, i) => i),
  );
  const [selected, setSelected] = useState(0);
  const positions =
    s.runes.length === 1 ? ["Focus"] : ["Situation", "Challenge", "Reflection"];
  const active = stone(s.runes[selected]);
  const show = (i: number) => {
    setSelected(i);
    if (open.includes(i)) return;
    cue?.();
    setOpen([...open, i]);
    if (open.length + 1 === s.runes.length) complete?.();
  };
  return (
    <div className="rune-experience">
      <div className="rune-bed">
        <div className="rune-mist" aria-hidden="true" />
        {s.runes.map((id, i) => {
          const r = stone(id),
            revealed = open.includes(i);
          return (
            <button
              key={id}
              type="button"
              className={"rune-stone" + (revealed ? " revealed" : "")}
              disabled={compact}
              aria-label={
                revealed
                  ? `Explore ${r.name}, ${positions[i]}`
                  : `Reveal stone ${i + 1}, ${positions[i]}`
              }
              aria-pressed={revealed && selected === i}
              data-rune={revealed ? id : undefined}
              onClick={() => show(i)}
            >
              <span className="rune-incision" aria-hidden="true">
                {revealed ? r.glyph : "·"}
              </span>
              <span>{positions[i]}</span>
            </button>
          );
        })}
      </div>
      {!compact && open.includes(selected) && (
        <article className="rune-reading" aria-live="polite">
          <p className="eyebrow">
            {positions[selected]} · {active.transliteration}
          </p>
          <h3>{active.name}</h3>
          <p className="runic-theme">{active.composition.theme}</p>
          <p>{active.composition.reflection}</p>
          <p className="scope-note">
            Modern editorial reflection · upright Elder Futhark layout.
          </p>
          <details className="chamber-depth">
            <summary>Historical and linguistic evidence</summary>
            <p>
              Transliteration: {active.transliteration}.{" "}
              {active.name_attested_as_elder_label
                ? "Attested label."
                : "The displayed name is not directly attested as an Elder Futhark label."}
            </p>
            <p>
              Qualified name association:{" "}
              {active.association.lexical_association ?? "unresolved"}.
            </p>
            {[
              active.historical_reference,
              active.association,
              ...active.later_poem_accounts,
            ].map((row, i) => {
              const source = runes.sources.find(
                (source) => source.id === row.source_id,
              );
              return (
                <p key={i}>
                  {row.coverage} ·{" "}
                  {source ? (
                    <a href={source.url} target="_blank" rel="noreferrer">
                      {source.author} · {row.locator}
                    </a>
                  ) : (
                    row.locator
                  )}
                </p>
              );
            })}
            <p>
              Later rune poems are comparative witnesses, with their own
              traditions and dates.
            </p>
          </details>
        </article>
      )}
    </div>
  );
}
