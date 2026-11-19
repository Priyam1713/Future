import { useEffect, useId, useMemo, useRef, useState } from "react";
import {
  BODY_NAMES,
  GLYPHS,
  SIGNS,
  SIGN_GLYPHS,
  degree,
  type Geometry,
} from "./contracts";
import { initialQuality } from "../orb/policy";
import { point } from "./geometry";
function between(a: number, b: number) {
  return (a + ((b - a + 360) % 360) / 2) % 360;
}
const ASPECT_NAMES: Record<number, string> = {
  0: "Conjunction",
  60: "Sextile",
  90: "Square",
  120: "Trine",
  180: "Opposition",
};
export { ASPECT_NAMES };
export function BirthChart({
  chart,
  reduced = false,
  paused = false,
  onSelect,
  selected = "Sun",
  compact = false,
}: {
  chart: Geometry;
  reduced?: boolean;
  paused?: boolean;
  onSelect?: (body: string) => void;
  selected?: string;
  compact?: boolean;
}) {
  const host = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false),
    [hidden, setHidden] = useState(document.hidden),
    [rotation, setRotation] = useState(0),
    [quality] = useState(initialQuality);
  const id = useId().replaceAll(":", "");
  const moving = !reduced && !paused && visible && !hidden;
  useEffect(() => {
    const o = new IntersectionObserver(([e]) => setVisible(e.isIntersecting));
    if (host.current) o.observe(host.current);
    const fn = () => setHidden(document.hidden);
    document.addEventListener("visibilitychange", fn);
    return () => {
      o.disconnect();
      document.removeEventListener("visibilitychange", fn);
    };
  }, []);
  const origin = chart.angles.ascendant;
  // Exact longitudes stay on the ecliptic. Crowded glyphs move to radial lanes,
  // with leaders to their true coordinate; selection never changes the chart.
  const locations = BODY_NAMES.map((name, i) => {
    const p = chart.planets[name];
    let neighbours = 0;
    for (let j = 0; j < i; j++) {
      const d = Math.abs(
        ((p.longitude - chart.planets[BODY_NAMES[j]].longitude + 540) % 360) -
          180,
      );
      if (d < 13) neighbours++;
    }
    return { name, p, i, r: 201 - (neighbours % 3) * 25 };
  });
  const drawing = useMemo(
    () => (
      <svg
        viewBox="0 0 600 600"
        role="img"
        aria-label="Calculated tropical birth chart: planetary longitudes, house cusps and major aspects"
        data-chart-origin={origin}
      >
        <defs>
          <radialGradient id={`${id}-glass`}>
            <stop stopColor="#123f43" stopOpacity=".8" />
            <stop offset=".75" stopColor="#071f26" />
            <stop offset="1" stopColor="#020e15" />
          </radialGradient>
          <linearGradient id={`${id}-brass`} x2="1" y2="1">
            <stop stopColor="#634d25" />
            <stop offset=".3" stopColor="#f1dca1" />
            <stop offset=".55" stopColor="#7f6836" />
            <stop offset="1" stopColor="#dec48b" />
          </linearGradient>
        </defs>
        <circle
          cx="300"
          cy="300"
          r="296"
          fill="#203630"
          stroke="#7f6f45"
          strokeWidth="2"
        />
        <circle cx="300" cy="300" r="292" fill={`url(#${id}-brass)`} />
        <circle
          cx="300"
          cy="300"
          r="287"
          fill="none"
          stroke="#172e2e"
          strokeWidth="2"
        />
        <circle
          cx="300"
          cy="300"
          r="283"
          fill={`url(#${id}-glass)`}
          stroke="#ebdba5"
          strokeWidth="1"
        />
        <g
          className="chart-etchings"
          fill="none"
          stroke="#dfcc95"
          opacity=".45"
        >
          <circle cx="300" cy="300" r="294" strokeDasharray="1 6" />
          <circle cx="300" cy="300" r="276" />
          <circle cx="300" cy="300" r="266" strokeDasharray=".6 5" />
        </g>
        <g stroke="#cdb780" strokeWidth="1">
          {Array.from({ length: 360 }, (_, i) => {
            const a = point(
                i,
                i % 10 === 0 ? 263 : i % 5 === 0 ? 269 : 273,
                origin,
              ),
              b = point(i, 278, origin);
            return (
              <line
                key={i}
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                opacity={i % 5 === 0 ? 0.65 : 0.25}
              />
            );
          })}
        </g>
        <circle
          cx="300"
          cy="300"
          r="227"
          fill="none"
          stroke="#c7b479"
          opacity=".55"
        />
        {SIGNS.map((s, i) => {
          const a = point(i * 30, 227, origin),
            b = point(i * 30, 265, origin),
            t = point(i * 30 + 15, 246, origin);
          return (
            <g key={s}>
              <line
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                stroke="#ddc893"
                opacity=".5"
              />
              <text
                x={t.x}
                y={t.y + 5}
                textAnchor="middle"
                fill="#e1d2a8"
                fontSize="19"
                style={{ fontFamily: 'Georgia, "Segoe UI Symbol", serif' }}
              >
                <title>{s}</title>
                {SIGN_GLYPHS[i] + "\uFE0E"}
              </text>
            </g>
          );
        })}
        {chart.house_cusps.map((c, i) => {
          const a = point(c, 115, origin),
            b = point(c, 226, origin),
            t = point(between(c, chart.house_cusps[(i + 1) % 12]), 132, origin);
          return (
            <g key={i} data-house={i + 1} data-longitude={c}>
              <line
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                stroke="#a9c7b4"
                opacity=".22"
              />
              <text
                x={t.x}
                y={t.y + 4}
                fill="#9caf9c"
                textAnchor="middle"
                fontSize="10"
              >
                {i + 1}
              </text>
            </g>
          );
        })}
        <g className="chart-aspects">
          {chart.aspects.map((a, i) => {
            const p = point(chart.planets[a.bodies[0]].longitude, 112, origin),
              q = point(chart.planets[a.bodies[1]].longitude, 112, origin),
              active = a.bodies.includes(selected);
            return (
              <line
                key={i}
                data-bodies={a.bodies.join("-")}
                data-angle={a.angle}
                x1={p.x}
                y1={p.y}
                x2={q.x}
                y2={q.y}
                stroke={
                  a.angle === 90 || a.angle === 180 ? "#dbad96" : "#85cbbf"
                }
                strokeWidth={active ? 1.6 : 0.65}
                opacity={active ? 0.85 : 0.16}
              >
                <title>
                  {a.bodies.join(" / ")} · {ASPECT_NAMES[a.angle]} · orb{" "}
                  {a.orb.toFixed(2)}°
                </title>
              </line>
            );
          })}
        </g>
        <circle
          cx="300"
          cy="300"
          r="112"
          fill="none"
          stroke="#9dbaac"
          opacity=".2"
        />
        {locations.map(({ name, p, i, r }) => {
          const a = point(p.longitude, 224, origin),
            b = point(p.longitude, r, origin);
          return (
            <g
              key={name}
              data-planet={name}
              data-longitude={p.longitude}
              className={selected === name ? "planet-selected" : ""}
            >
              <line
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                stroke="#d2c18d"
                opacity=".5"
              />
              <circle cx={a.x} cy={a.y} r="2.3" fill="#e9d49e" />
              <g
                onClick={() => onSelect?.(name)}
                style={{ cursor: onSelect ? "pointer" : "default" }}
              >
                <circle
                  cx={b.x}
                  cy={b.y}
                  r="15"
                  fill={selected === name ? "#385c57" : "#10262e"}
                  stroke={selected === name ? "#e6d2a2" : "#6a887e"}
                  strokeWidth={selected === name ? 1.5 : 0.6}
                />
                <text
                  x={b.x}
                  y={b.y + 6}
                  textAnchor="middle"
                  fontSize="20"
                  fill="#f1e4c0"
                >
                  {GLYPHS[i]}
                </text>
                <title>
                  {name} · {degree(p.longitude)} · House {p.house}
                  {p.retrograde ? " · retrograde" : ""}
                </title>
              </g>
            </g>
          );
        })}
        {[
          { label: "ASC", lon: origin },
          { label: "MC", lon: chart.angles.midheaven },
        ].map((a) => {
          const p = point(a.lon, 287, origin);
          return (
            <g key={a.label}>
              <circle
                cx={p.x}
                cy={p.y}
                r="15"
                fill="#183a3a"
                stroke="#e4cc8f"
              />
              <text
                x={p.x}
                y={p.y + 3}
                textAnchor="middle"
                fontSize="8"
                fill="#f6dfa9"
              >
                {a.label}
              </text>
              <title>
                {a.label} · {degree(a.lon)}
              </title>
            </g>
          );
        })}
        <circle cx="300" cy="300" r="5" fill="#ddc78c" />
        <path d="M300 282v36m-18-18h36" stroke="#d5c18d" opacity=".4" />
      </svg>
    ),
    [chart, origin, id, onSelect, selected],
  );
  return (
    <div
      ref={host}
      className={`birth-chart ${compact ? "chart-compact" : ""} ${moving ? "chart-moving" : "chart-still"} ${quality === "low" ? "chart-economy" : ""}`}
      data-renderer="native-svg-chart"
      data-render-state={moving ? "running" : "paused"}
      onPointerMove={(e) => {
        if (!moving || quality === "low" || compact) return;
        const b = e.currentTarget.getBoundingClientRect();
        e.currentTarget.style.setProperty(
          "--chart-x",
          `${((e.clientX - b.left) / b.width) * 4 - 2}deg`,
        );
        e.currentTarget.style.setProperty(
          "--chart-y",
          `${2 - ((e.clientY - b.top) / b.height) * 4}deg`,
        );
      }}
      onPointerLeave={(e) => {
        e.currentTarget.style.setProperty("--chart-x", "0deg");
        e.currentTarget.style.setProperty("--chart-y", "0deg");
      }}
    >
      <div className="chart-halo" aria-hidden="true" />
      <div
        className="chart-instrument"
        style={{
          transform: `perspective(1000px) rotateX(var(--chart-y,0deg)) rotateY(var(--chart-x,0deg)) rotate(${rotation}deg)`,
        }}
      >
        {drawing}
        <div className="chart-engraving" aria-hidden="true" />
      </div>
      <div className="chart-light" aria-hidden="true" />
      {!compact && (
        <>
          <div className="chart-touch" aria-label="Choose a planet">
            {BODY_NAMES.map((n, i) => (
              <button
                key={n}
                aria-pressed={selected === n}
                aria-label={`Explore ${n}`}
                onClick={() => onSelect?.(n)}
              >
                <span aria-hidden="true">{GLYPHS[i]}</span>
                <small>{n}</small>
              </button>
            ))}
          </div>
          <label className="chart-turn">
            Turn the instrument{" "}
            <input
              type="range"
              min="-180"
              max="180"
              step="1"
              value={rotation}
              onChange={(e) => setRotation(Number(e.target.value))}
            />
            <button className="text-button" onClick={() => setRotation(0)}>
              Align Ascendant
            </button>
          </label>
        </>
      )}
    </div>
  );
}
