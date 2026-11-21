import { useState } from "react";
import type { BaziSnapshot, VedicSnapshot } from "./contracts";
import { bazi, citation, pillarNames, vedic } from "./reference";
import { GLYPHS, SIGN_GLYPHS } from "../astrology/contracts";
import { GrahaReading, JyotishOpening, JyotishTimeline, LunarReading, type JyotishReading } from "./JyotishReading";
import type { Evidence } from "../codex/reference";

export function Sources({
  rows,
  title = "Source notes",
}: {
  rows: Evidence[];
  title?: string;
}) {
  return (
    <details className="chamber-depth">
      <summary>{title}</summary>
      {rows.map((row, i) => (
        <blockquote key={i}>
          <p>{row.wording}</p>
          <cite>
            {row.label} ·{" "}
            {row.url ? (
              <a href={row.url} target="_blank" rel="noreferrer">
                {row.locator}
              </a>
            ) : (
              row.locator
            )}
          </cite>
        </blockquote>
      ))}
    </details>
  );
}
const gems = [
  "#e7ab46",
  "#c1e0ed",
  "#a4c06c",
  "#f1c1ad",
  "#e87a57",
  "#e8d285",
  "#88a3e3",
  "#9a7cc8",
  "#80c5b7",
];
const polar = (angle: number, radius: number) => {
  const rad = ((angle - 90) * Math.PI) / 180;
  return { x: 240 + Math.cos(rad) * radius, y: 240 + Math.sin(rad) * radius };
};

export function VedicDial({
  s,
  compact = false,
  live = false,
  reading,
}: {
  s: VedicSnapshot;
  compact?: boolean;
  live?: boolean;
  reading?: JyotishReading;
}) {
  const [d9, setD9] = useState(false),
    [selected, setSelected] = useState(1),
    [period, setPeriod] = useState(s.active);
  const [mansionShown, setMansionShown] = useState(!live);
  const graha = vedic.grahas[selected],
    position = s.planets[selected],
    asc = d9 ? s.d9Asc : s.asc;
  const [mansion, pada, sensitive] = s.mansion;
  const active = s.sub[period];
  return (
    <div className="vedic-experience">
      {reading && <JyotishOpening reading={reading} />}
      <div className="vedic-dial">
        <div className="vedic-inlay" aria-hidden="true" />
        <svg
          viewBox="0 0 480 480"
          role="img"
          aria-label={
            d9
              ? "Symbolic D9 Navamsa geometry"
              : "Native D1 sidereal graha geometry"
          }
        >
          {[212, 194, 171, 148, 90, 71].map((r) => (
            <circle
              key={r}
              cx="240"
              cy="240"
              r={r}
              fill="none"
              stroke="currentColor"
              opacity={r > 150 ? 0.32 : 0.22}
            />
          ))}
          {Array.from({ length: 108 }, (_, i) => {
            const a = polar((i * 360) / 108, i % 4 === 0 ? 197 : 204),
              b = polar((i * 360) / 108, 211);
            return (
              <line
                key={i}
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                stroke="currentColor"
                opacity={i % 4 === 0 ? 0.65 : 0.26}
              />
            );
          })}
          {vedic.signs.map((sign, i) => {
            const p = polar(i * 30 + 15, 181);
            return (
              <text key={sign} x={p.x} y={p.y} dy=".34em" textAnchor="middle">
                {SIGN_GLYPHS[i] + "\uFE0E"}
              </text>
            );
          })}
          {(() => {
            const p = polar(asc[0], 171);
            return (
              <circle
                cx={p.x}
                cy={p.y}
                r="5"
                fill="#faf0cc"
                data-lagna={asc[0]}
              />
            );
          })()}
          {s.planets.map((row, i) => {
            const lon = row[d9 ? 3 : 0],
              p = polar(lon, 150);
            const inner = polar(lon, i === selected ? 79 : 101 + i * 3);
            return (
              <g
                key={vedic.grahas[i]}
                data-graha={vedic.grahas[i]}
                data-longitude={lon}
                data-selected={i === selected}
                onClick={() => setSelected(i)}
              >
                <line
                  x1={p.x}
                  y1={p.y}
                  x2={inner.x}
                  y2={inner.y}
                  stroke={gems[i]}
                  opacity={i === selected ? 1 : 0.35}
                />
                <circle
                  cx={p.x}
                  cy={p.y}
                  r={i === selected ? 8 : 5}
                  fill={gems[i]}
                  stroke="#ead7ac"
                  opacity={i === selected ? 1 : 0.82}
                />
              </g>
            );
          })}
          <text x="240" y="232" textAnchor="middle" className="dial-center">
            {d9 ? "D9" : "D1"}
          </text>
          <text x="240" y="260" textAnchor="middle" className="dial-caption">
            {vedic.signs[asc[1]] + " Lagna"}
          </text>
        </svg>
      </div>
      {!compact && (
        <>
          <div
            className="chamber-switch"
            role="group"
            aria-label="Vedic chart view"
          >
            <button aria-pressed={!d9} onClick={() => setD9(false)}>
              D1 · Rashi
            </button>
            <button aria-pressed={d9} onClick={() => setD9(true)}>
              D9 · Navamsa
            </button>
          </div>
          <p className="chamber-measure" aria-live="polite">
            {graha} · {vedic.signs[position[d9 ? 4 : 1]]} · House{" "}
            {position[d9 ? 5 : 2]} · {position[d9 ? 3 : 0].toFixed(3)}°{" "}
            {d9 ? "symbolic longitude" : "sidereal longitude"}
          </p>
          <div
            className="graha-keys"
            role="group"
            aria-label="Explore the nine grahas"
          >
            {vedic.grahas.map((name, i) => (
              <button
                key={name}
                aria-pressed={i === selected}
                onClick={() => setSelected(i)}
                style={{ "--gem": gems[i] } as React.CSSProperties}
              >
                <span aria-hidden="true">
                  {name === "Rahu" ? "☊" : name === "Ketu" ? "☋" : GLYPHS[i]}
                </span>
                {name}
              </button>
            ))}
          </div>
          {reading && <GrahaReading reading={reading} graha={graha} s={s} />}
          <section className="moon-mansion">
            <p className="eyebrow">Your lunar mansion</p>
            {mansionShown ? (
              <div className="mansion-reveal" aria-live="polite">
                <h3>{vedic.mansions[mansion]}</h3>
                <div className="mansion-petals" aria-hidden="true">
                  {[1, 2, 3, 4].map((i) => (
                    <i key={i} className={i === pada ? "lit" : ""} />
                  ))}
                </div>
                {reading ? <LunarReading reading={reading} /> : <p>
                  Pada {pada} of 4 · {vedic.lords[mansion]} is the birth-star
                  lord.
                </p>}
                {sensitive && <p>This placement is close to a mansion or quarter boundary.</p>}
              </div>
            ) : (
              <button
                className="secondary"
                onClick={() => setMansionShown(true)}
              >
                Reveal my birth star
              </button>
            )}
          </section>
          {reading ? <JyotishTimeline reading={reading} active={s.active} /> : <section className="dasha-rail">
            <p className="eyebrow">
              Vimshottari ·{" "}
              {s.year === "pvr-2000-savana"
                ? "360-day savana year"
                : "365.2425-day year"}
            </p>
            <h3>{s.main[0][0]} main period</h3>
            <p>
              Active subperiod at the selected instant: {s.sub[s.active][0]}.
              Explore the nine subdivisions.
            </p>
            <div
              className="chamber-switch"
              role="group"
              aria-label="Explore subperiods"
            >
              {s.sub.map(([lord], i) => (
                <button
                  key={lord}
                  aria-pressed={i === period}
                  onClick={() => setPeriod(i)}
                >
                  {lord}
                </button>
              ))}
            </div>
            <p className="chamber-measure" aria-live="polite">
              {active[0]} · {active[1]} → {active[2]} (UTC boundary days)
            </p>
            <details className="chamber-depth">
              <summary>Main period boundaries and upcoming periods</summary>
              <ol>
                {s.main.map(([lord, start, end]) => (
                  <li key={start}>
                    {lord} · {start} → {end}
                  </li>
                ))}
              </ol>
              <p>
                The native calculation uses exact UTC start-inclusive and
                end-exclusive times. These are the corresponding UTC days.
              </p>
            </details>
          </section>}
        </>
      )}
    </div>
  );
}

export function JadePillars({
  s,
  compact = false,
}: {
  s: BaziSnapshot;
  compact?: boolean;
}) {
  const [selected, setSelected] = useState(2);
  const pairs = s.pairs.map((index) => bazi.pairs[index]),
    day = pairs[2].stem;
  const picked = pairs[selected],
    relation = bazi.relations[day.index][picked.stem.index];
  const image = bazi.masters[day.index];
  return (
    <div className="bazi-experience">
      <div
        className="jade-rack"
        role="group"
        aria-label="Calculated Four Pillars"
      >
        {pairs.map((pair, i) => (
          <button
            type="button"
            disabled={compact}
            key={pillarNames[i]}
            onClick={() => setSelected(i)}
            aria-label={pillarNames[i] + " pillar, " + pair.name}
            aria-pressed={i === selected}
            data-pillar={pillarNames[i]}
            data-pair={pair.sexagenary_index}
          >
            <span className="pillar-label">{pillarNames[i]}</span>
            <span className="pillar-stem" lang="zh">
              {pair.stem.character}
            </span>
            <span className="pillar-branch" lang="zh">
              {pair.branch.character}
            </span>
            <span>
              {pair.stem.element} / {pair.branch.element}
            </span>
          </button>
        ))}
      </div>
      {!compact && (
        <section className="jade-reading" aria-live="polite">
          <p className="eyebrow">
            {pillarNames[selected]} pillar · {picked.name}
          </p>
          <h3>
            {selected === 2 ? day.name + ", the Day Master" : relation.name}
          </h3>
          <p>
            {selected === 2
              ? day.polarity +
                " " +
                day.element +
                " is the reference for stem relationships. " +
                image.text
              : relation.reason}
          </p>
          <p>
            {picked.branch.name} · {picked.branch.animal} ·{" "}
            {picked.branch.polarity} {picked.branch.element}
          </p>
          <p className="chamber-measure">
            {s.profile === "standard-zi23"
              ? "Standard clock · 23:00 day boundary"
              : s.profile === "civil-split-zi"
                ? "Civil clock · split late Zi hour"
                : "Civil clock · 23:00 day boundary"}
          </p>
          <Sources
            title="Pillar sources & hidden stems"
            rows={[
              citation("Day Master imagery", image, bazi.sources),
              citation(
                "Documented pillar topic",
                bazi.topics[selected],
                bazi.sources,
              ),
              ...(selected !== 2
                ? [
                    citation(
                      "Defined stem relationship",
                      { ...relation, text: relation.reason },
                      bazi.sources,
                    ),
                  ]
                : []),
              citation(
                "Fixed hidden-stem membership",
                {
                  ...bazi.hidden,
                  text: bazi.hidden.stems_by_branch[picked.branch.index]
                    .map(
                      (i) => bazi.stems[i].name + " · " + bazi.stems[i].element,
                    )
                    .join(" / "),
                },
                bazi.sources,
              ),
            ]}
          />
          <p className="scope-note">
            Element relationships are symbolic definitions. This reading makes
            no strength, luck-cycle, or outcome assessment.
          </p>
        </section>
      )}
    </div>
  );
}
