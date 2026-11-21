import { useEffect, useId, useMemo, useRef, useState } from "react";
import {
  BODY_NAMES,
  GLYPHS,
  SIGNS,
  SIGN_GLYPHS,
  aspectKey,
  degree,
  type Geometry,
} from "./contracts";
import { initialQuality } from "../orb/policy";
import { point } from "./geometry";
import { ChartTurn } from "./ChartTurn";
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
  exploreDetails = false,
  label = "Calculated tropical birth chart: planetary longitudes, house cusps and major aspects",
}: {
  chart: Geometry;
  reduced?: boolean;
  paused?: boolean;
  onSelect?: (body: string) => void;
  selected?: string;
  compact?: boolean;
  exploreDetails?: boolean;
  label?: string;
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
  const selectedAspect = exploreDetails && selected.startsWith("aspect:")
    ? chart.aspects.find((aspect) => aspectKey(aspect) === selected) : undefined;
  // Resolve label collisions in display space, retaining a leader to the exact
  // native coordinate. Selected glyphs own the front lane; no modulo overlap.
  const locations = useMemo(() => {
    const used: { x: number; y: number }[] = [];
    const ordered = BODY_NAMES.map((name, i) => ({
      name,
      p: chart.planets[name],
      i,
    }))
      .filter(({ p }) => p)
      .sort(
        (a, b) => Number(b.name === selected) - Number(a.name === selected),
      );
    return ordered
      .map((item) => {
        const lon = item.p.longitude;
        let best = { r: 200, angle: lon, x: 0, y: 0 },
          clearance = -1;
        search: for (const r of [200, 173, 146])
          for (const shift of [0, -7, 7, -14, 14, -21, 21]) {
            const p = point(lon + shift, r, origin),
              gap = used.length
                ? Math.min(...used.map((q) => Math.hypot(q.x - p.x, q.y - p.y)))
                : 999;
            if (gap > clearance) {
              clearance = gap;
              best = { r, angle: lon + shift, ...p };
            }
            if (gap >= 34) {
              best = { r, angle: lon + shift, ...p };
              clearance = gap;
              break search;
            }
          }
        used.push(best);
        return { ...item, ...best };
      })
      .sort((a, b) => a.i - b.i);
  }, [chart, origin, selected]);
  const drawing = useMemo(
    () => (
      <svg
        viewBox="0 0 600 600"
        role="img"
        aria-label={label}
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
                fill={selected === `house:${i + 1}` ? "#ffe0a7" : "#9caf9c"}
                textAnchor="middle"
                fontSize={selected === `house:${i + 1}` ? "16" : "11"}
                onClick={exploreDetails ? () => onSelect?.(`house:${i + 1}`) : undefined}
                style={exploreDetails ? { cursor: "pointer" } : undefined}
              >
                {i + 1}
              </text>
            </g>
          );
        })}
        <g className="chart-aspects">
          {chart.aspects.map((a, i) => {
            if (a.bodies.some((name) => !chart.planets[name])) return null;
            const p = point(chart.planets[a.bodies[0]].longitude, 112, origin),
              q = point(chart.planets[a.bodies[1]].longitude, 112, origin),
              active = a.bodies.includes(selected) || (exploreDetails && aspectKey(a) === selected);
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
                onClick={exploreDetails ? () => onSelect?.(aspectKey(a)) : undefined}
                style={exploreDetails ? { cursor: "pointer" } : undefined}
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
        {locations.map(({ name, p, i, r, angle }) => {
          const a = point(p.longitude, 224, origin),
            b = point(angle, r, origin);
          const highlighted = selected === name || selectedAspect?.bodies.includes(name) || selected === `house:${p.house}`;
          return (
            <g
              key={name}
              data-planet={name}
              data-longitude={p.longitude}
              className={highlighted ? "planet-selected" : ""}
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
                  fill={highlighted ? "#385c57" : "#10262e"}
                  stroke={highlighted ? "#e6d2a2" : "#6a887e"}
                  strokeWidth={highlighted ? 1.5 : 0.6}
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
    [chart, origin, id, onSelect, selected, label, locations, exploreDetails, selectedAspect],
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
          <p className="chart-current">
            {selected in chart.planets ? (
              <>
                <strong>{selected}</strong> ·{" "}
                {degree(chart.planets[selected].longitude)} · House{" "}
                {chart.planets[selected].house}
              </>
            ) : selected.startsWith("house:") ? (
              <>House {selected.slice(6)}</>
            ) : selected.startsWith("aspect:") ? (
              <>Major aspect selected</>
            ) : (
              <>Ascendant · {degree(chart.angles.ascendant)}</>
            )}
          </p>
          <div className="chart-touch" aria-label="Choose a planet">
            {BODY_NAMES.map(
              (n, i) =>
                chart.planets[n] && (
                  <button
                    key={n}
                    aria-pressed={selected === n}
                    aria-label={`Explore ${n}`}
                    onClick={() => onSelect?.(n)}
                  >
                    <span aria-hidden="true">{GLYPHS[i]}</span>
                    <small>{n}</small>
                  </button>
                ),
            )}
          </div>
          <ChartTurn rotation={rotation} setRotation={setRotation} />
        </>
      )}
    </div>
  );
}
