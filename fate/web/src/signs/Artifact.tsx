import { useId, type CSSProperties } from "react";
import { choicesTitle, options, type SignId } from "./contracts";

type Props = {
  id: SignId;
  values: string[];
  step?: number;
  choose?: (value: string) => void;
  compact?: boolean;
};
const cupZones = [
  ["rim", "Rim", 66],
  ["side", "Side", 48],
  ["bottom", "Bottom", 27],
] as const;
const glyphs: Record<string, string> = {
  anchor: "⚓︎",
  bird: "⌁",
  letter: "A",
  acorn: "●",
  cross: "✚",
  camel: "∽",
  fish: "≋",
  moon_patch: "☽",
};
const and = (v: string) => (v.includes("+") ? v.split("+").join(" / ") : v);
function readLabel(id: SignId, index: number, values: string[]) {
  return (
    options(id, index, values).find(([key]) => key === values[index])?.[1] ?? ""
  );
}

export function Artifact({ id, values, step, choose, compact }: Props) {
  const material = useId();
  const paint = (layer: string) => `url(#${material}-${layer})`;
  const active = (number: number) => step === number && choose;
  const buttons = (n: number, name: string) =>
    active(n) && (
      <div className={name} role="group" aria-label="Select on the instrument">
        {options(id, n, values).map(([key, label]) => (
          <button key={key} onClick={() => choose!(key)}>
            {label}
          </button>
        ))}
      </div>
    );
  if (id === 28) {
    return (
      <div className="sign-cup">
        <svg viewBox="0 0 210 210" role="img" aria-label="Cup region diagram">
          <defs>
            <radialGradient id={`${material}-glaze`} cx="34%" cy="24%" r="75%">
              <stop stopColor="#fff0d0" />
              <stop offset=".65" stopColor="#bca97f" />
              <stop offset=".9" stopColor="#e6d3a6" />
              <stop offset="1" stopColor="#88805d" />
            </radialGradient>
            <radialGradient id={`${material}-tea`} cx="36%" cy="28%" r="72%">
              <stop stopColor="#9d6951" />
              <stop offset=".68" stopColor="#503126" />
              <stop offset="1" stopColor="#2f211c" />
            </radialGradient>
            <linearGradient id={`${material}-selection`} x2="80%" y2="100%">
              <stop stopColor="#eed293" />
              <stop offset="1" stopColor="#926747" />
            </linearGradient>
          </defs>
          <path
            d="M181 85c43-22 38 68 0 48"
            fill="none"
            stroke={paint("glaze")}
            strokeWidth="7"
          />
          <circle
            cx="101"
            cy="106"
            r="90"
            fill={paint("glaze")}
            stroke="#846e4c"
            strokeWidth="3"
          />
          <circle
            cx="101"
            cy="106"
            r="82"
            fill="none"
            stroke="#796447"
            strokeWidth="2"
          />
          <circle
            cx="101"
            cy="106"
            r="77"
            fill="none"
            stroke="#8b754b"
            strokeDasharray="1 2.7"
          />
          {cupZones.map(([key, , radius], i) => (
            <circle
              key={key}
              cx="101"
              cy="106"
              r={radius}
              fill={paint(values[0] === key ? "selection" : "tea")}
              opacity={i === 0 ? 1 : 0.92}
              stroke={values[0] === key ? "#f6dfab" : "#c6a474"}
              strokeWidth={values[0] === key ? "2.4" : "1"}
            />
          ))}
          <text
            x="101"
            y="121"
            textAnchor="middle"
            fill="#fff1ca"
            fontSize="34"
            paintOrder="stroke"
            stroke="#2c201a"
            strokeWidth="1.4"
          >
            {glyphs[values[1]] ?? "·"}
          </text>
        </svg>
        {!!active(0) && (
          <div className="vessel-choices">
            {cupZones.map(([key, label]) => (
              <button key={key} onClick={() => choose!(key)}>
                {label}
              </button>
            ))}
            <button onClick={() => choose!("unknown")}>Region unknown</button>
          </div>
        )}
      </div>
    );
  }
  if (id === 29) {
    return (
      <div
        className={
          "sign-saucer " + (values[0] === "saucer" ? "saucer-active" : "")
        }
      >
        <span className="coffee-handle" aria-hidden="true" />
        <div className="coffee-well" aria-hidden="true">
          <span>{glyphs[values[1]] ?? "∴"}</span>
        </div>
        {!!active(0) && (
          <div className="vessel-choices">
            <button onClick={() => choose!("cup")}>Cup</button>
            <button onClick={() => choose!("saucer")}>Saucer</button>
          </div>
        )}
      </div>
    );
  }
  if (id === 30) {
    return (
      <div
        className="sign-candle"
        data-height={values[0] ?? "unknown"}
        data-persistent={values[1] === "persistent"}
      >
        <div className="candle-ruler" aria-hidden="true" />
        <div className="candle-flame" aria-hidden="true" />
        <div className="candle-wax" aria-hidden="true" />
        {!!active(0) && (
          <div className="vessel-choices">
            {options(id, 0, values).map(([k, l]) => (
              <button key={k} onClick={() => choose!(k)}>
                {l}
              </button>
            ))}
          </div>
        )}
      </div>
    );
  }
  if (id === 31) {
    return (
      <div className="sign-water" data-category={values[0]}>
        <div className="water-lens" aria-hidden="true">
          <i />
          <i />
          <i />
          <span>
            {values[0] === "reflection"
              ? "◇"
              : values[0] === "physical_ripples"
                ? "≈"
                : "·"}
          </span>
        </div>
        {buttons(0, "vessel-choices water-choices")}
      </div>
    );
  }
  if (id === 32) {
    const angles: Record<string, number> = {
      east: 90,
      west: -90,
      east_west: 90,
      north_south: 0,
      unknown: 0,
    };
    const angle = angles[values[1]] ?? 0;
    return (
      <div className="sign-wind">
        <svg
          viewBox="0 0 200 200"
          role="img"
          aria-label="Diagram illustrates the manually selected direction"
        >
          <defs>
            <radialGradient id={`${material}-patina`} cx="38%" cy="25%" r="76%">
              <stop stopColor="#456067" />
              <stop offset=".76" stopColor="#182d39" />
              <stop offset="1" stopColor="#08121b" />
            </radialGradient>
            <linearGradient id={`${material}-bronze`} x2="60%" y2="90%">
              <stop stopColor="#f6deb0" />
              <stop offset=".48" stopColor="#997955" />
              <stop offset="1" stopColor="#d5b582" />
            </linearGradient>
          </defs>
          <circle
            cx="100"
            cy="100"
            r="92"
            fill={paint("patina")}
            stroke={paint("bronze")}
            strokeWidth="3"
          />
          <circle
            cx="100"
            cy="100"
            r="85"
            fill="none"
            stroke="#b0956c"
            strokeDasharray="1 3.45"
          />
          <circle
            cx="100"
            cy="100"
            r="53"
            fill="none"
            stroke="#b0956c"
            opacity=".42"
          />
          <path
            d="M54 54 146 146 M146 54 54 146"
            fill="none"
            stroke="#b0956c"
            opacity=".35"
          />
          <circle
            cx="100"
            cy="100"
            r="72"
            fill="none"
            stroke="#765e45"
            strokeDasharray="2 4"
          />
          {["N", "E", "S", "W"].map((l, i) => (
            <text
              key={l}
              x={[100, 177, 100, 23][i]}
              y={[31, 105, 177, 105][i]}
              textAnchor="middle"
              fill="#f3e2b7"
              fontSize="14"
            >
              {l}
            </text>
          ))}
          {values[1] && values[1] !== "unknown" && (
            <g
              className="wind-pointer"
              style={{ "--bearing": angle + "deg" } as CSSProperties}
            >
              <path
                d="M100 48 L110 103 L100 155 L90 103 Z"
                fill={paint("bronze")}
                stroke="#f1d4a0"
              />
            </g>
          )}
          <circle cx="100" cy="100" r="10" fill="#ecce9c" stroke="#4d3c2d" />
        </svg>
        {values[1] && (
          <span className="artifact-tag">{readLabel(id, 1, values)}</span>
        )}
        {buttons(1, "vessel-choices wind-choices")}
      </div>
    );
  }
  if (id === 34) {
    const cells = options(id, 1, values);
    return (
      <div
        className="sign-stone-board"
        role="group"
        aria-label="Relative stone positions"
      >
        {cells.map(([key]) => {
          const [x, y] = key.split(":");
          const selected = key === values[1],
            center = key === "0:0";
          return active(1) ? (
            <button
              key={key}
              aria-pressed={selected}
              onClick={() => choose!(key)}
              aria-label={`Place stone at x ${x}, y ${y}`}
              data-stone={center ? "center" : ""}
            >
              {center ? "✥" : "·"}
            </button>
          ) : (
            <span
              key={key}
              aria-hidden="true"
              data-stone={selected ? "selected" : center ? "center" : ""}
            >
              {selected ? (center ? "◈" : "◆") : center ? "✥" : "·"}
            </span>
          );
        })}
        {!active(1) && (
          <span className="sr-only">
            {values[1]
              ? "Selected center " + values[1]
              : "Lodestone at the origin"}
          </span>
        )}
      </div>
    );
  }
  if (id === 35)
    return (
      <div className="archive-display">
        <div className="sign-inscription">
          <span aria-hidden="true">◇</span>
          <strong>{values[0] ? and(values[0]) : "Shang"}</strong>
          <small>Documentary index</small>
        </div>
        {buttons(0, "archive-tray")}
      </div>
    );
  if (id === 37) {
    if (active(0))
      return (
        <div className="sign-lots" role="group" aria-label="Greek marks">
          {options(id, 0, values).map(([key, label]) => (
            <button
              key={key}
              onClick={() => choose!(key)}
              aria-label={label.slice(label.indexOf("·") + 2)}
            >
              {label.split(" · ")[0]}
            </button>
          ))}
        </div>
      );
    const letter = readLabel(id, 0, values).split(" · ")[0];
    return (
      <div className="letter-tile">
        <span>{letter || "◇"}</span>
        <small>{values[0] ? "Declared lot" : "Greek alphabet"}</small>
      </div>
    );
  }
  if (id === 38) {
    return (
      <div
        className="sign-bird"
        data-side={values[2]}
        data-behavior={values[1]}
      >
        <svg viewBox="0 0 230 150" aria-hidden="true">
          <path
            d="M0 115 Q47 98 89 112 T168 109 T230 111"
            fill="none"
            stroke="#d2ac72"
          />
          <path
            d="M92 73 Q111 51 117 69 Q134 55 147 69 Q132 72 116 83 Q109 73 92 73"
            fill="#e4c38d"
            className="bird-mark"
          />
          <path
            d="M115 32 V121"
            fill="none"
            stroke="#e6c593"
            strokeDasharray="2 5"
          />
        </svg>
        {!!active(2) && (
          <div className="vessel-choices">
            {options(id, 2, values).map(([key, label]) => (
              <button key={key} onClick={() => choose!(key)}>
                {label}
              </button>
            ))}
          </div>
        )}
        {!compact && values[2] && (
          <span className="artifact-tag">
            {readLabel(id, 2, values)} · observer relative
          </span>
        )}
      </div>
    );
  }
  return (
    <div className="sign-casebook">
      <div>
        <span aria-hidden="true">§</span>
        <strong>
          {values[0] ? choicesTitle({ oracle: id, values }) : "Roman casebook"}
        </strong>
        <small>Annotated source folio</small>
      </div>
      {buttons(0, "vessel-choices roman-tabs")}
    </div>
  );
}

export function hasArtifactControls(id: SignId, step: number) {
  return (
    (id === 28 && step === 0) ||
    (id === 29 && step === 0) ||
    (id === 30 && step === 0) ||
    (id === 31 && step === 0) ||
    (id === 32 && step === 1) ||
    (id === 34 && step === 1) ||
    (id === 35 && step === 0) ||
    (id === 37 && step === 0) ||
    (id === 38 && step === 2) ||
    (id === 39 && step === 0)
  );
}
