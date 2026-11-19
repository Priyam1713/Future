import { useEffect, useId, useRef, useState } from "react";
import { BODY_NAMES, GLYPHS, SIGN_GLYPHS } from "../astrology/contracts";
import { point } from "../astrology/geometry";
import { initialQuality } from "../orb/policy";
import {
  TARGETS,
  dateLabel,
  timeLabel,
  type TurningResult,
  type TransitEvent,
} from "./contracts";
export function TimeInstrument({
  result,
  index,
  onDay,
  selectedEvent,
  onEvent,
  reduced = false,
  paused = false,
  compact = false,
}: {
  result: TurningResult;
  index: number;
  onDay: (day: number) => void;
  selectedEvent: TransitEvent | null;
  onEvent?: (event: TransitEvent | null) => void;
  reduced?: boolean;
  paused?: boolean;
  compact?: boolean;
}) {
  const ref = useRef<HTMLDivElement>(null),
    id = useId().replaceAll(":", "");
  const [visible, setVisible] = useState(false),
    [hidden, setHidden] = useState(document.hidden),
    [quality] = useState(initialQuality);
  useEffect(() => {
    const o = new IntersectionObserver(([e]) => setVisible(e.isIntersecting));
    if (ref.current) o.observe(ref.current);
    const fn = () => setHidden(document.hidden);
    document.addEventListener("visibilitychange", fn);
    return () => {
      o.disconnect();
      document.removeEventListener("visibilitychange", fn);
    };
  }, []);
  const frame = result.sky_samples[index],
    n = result.report.natal_summary,
    origin = n.angles.ascendant;
  const days = result.sky_samples.length;
  const target = selectedEvent
    ? (n.planets[selectedEvent.natal_target]?.longitude ??
      n.angles[selectedEvent.natal_target as "ascendant" | "midheaven"])
    : null;
  const positions = selectedEvent
    ? [[selectedEvent.transiting, selectedEvent.longitude] as const]
    : BODY_NAMES.map((name) => [name, frame.planets[name].longitude] as const);
  return (
    <div
      ref={ref}
      className={`time-instrument ${visible && !hidden && !reduced && !paused ? "time-moving" : "time-still"} ${quality === "low" ? "time-economy" : ""} ${compact ? "time-compact" : ""}`}
      data-renderer="native-time-instrument"
      data-render-state={
        visible && !hidden && !reduced && !paused ? "running" : "paused"
      }
    >
      <div
        className="time-machine"
        style={
          {
            "--time-turn": `${(index / Math.max(1, days)) * 360}deg`,
          } as React.CSSProperties
        }
      >
        <div className="time-orbit" aria-hidden="true" />
        <div className="time-gear" aria-hidden="true" />
        <svg
          viewBox="0 0 600 600"
          role="img"
          aria-label={
            selectedEvent
              ? "Exact native transit contact geometry"
              : "Native sampled planetary positions on the selected UTC date"
          }
        >
          <defs>
            <radialGradient id={`${id}-glass`}>
              <stop stopColor="#1c4c47" />
              <stop offset=".65" stopColor="#0c272d" />
              <stop offset="1" stopColor="#06171f" />
            </radialGradient>
            <linearGradient id={`${id}-metal`} x2="1" y2="1">
              <stop stopColor="#715733" />
              <stop offset=".3" stopColor="#e4cc8c" />
              <stop offset=".6" stopColor="#594827" />
              <stop offset="1" stopColor="#d7ba77" />
            </linearGradient>
          </defs>
          <circle cx="300" cy="300" r="281" fill={`url(#${id}-metal)`} />
          <circle
            cx="300"
            cy="300"
            r="272"
            fill={`url(#${id}-glass)`}
            stroke="#dbca9844"
          />
          {Array.from({ length: 120 }, (_, i) => {
            const a = point(i * 3, i % 10 === 0 ? 251 : 258, origin),
              b = point(i * 3, 268, origin);
            return (
              <line
                key={i}
                x1={a.x}
                y1={a.y}
                x2={b.x}
                y2={b.y}
                stroke="#d9c18c"
                opacity={i % 10 === 0 ? 0.6 : 0.2}
              />
            );
          })}
          {SIGN_GLYPHS.map((g, i) => {
            const p = point(i * 30 + 15, 238, origin);
            return (
              <text
                key={i}
                x={p.x}
                y={p.y + 5}
                fill="#d9c68d"
                fontSize="17"
                textAnchor="middle"
                fontFamily="Georgia, Segoe UI Symbol, serif"
              >
                {g + "\uFE0E"}
              </text>
            );
          })}
          <circle cx="300" cy="300" r="216" fill="none" stroke="#bcb38555" />
          <circle
            cx="300"
            cy="300"
            r="141"
            fill="none"
            stroke="#86a79d33"
            strokeDasharray="2 7"
          />
          {positions.map(([name, lon], i) => {
            const exact = point(lon, 215, origin),
              p = point(lon, 200 - (i % 2) * 24, origin);
            return (
              <g key={name} data-sky-body={name} data-native-longitude={lon}>
                <line
                  x1={exact.x}
                  y1={exact.y}
                  x2={p.x}
                  y2={p.y}
                  stroke="#bcd4bd"
                  opacity=".45"
                />
                <circle cx={exact.x} cy={exact.y} r="2.5" fill="#f1d99b" />
                <circle
                  cx={p.x}
                  cy={p.y}
                  r="15"
                  fill="#183c3c"
                  stroke="#bfa96c66"
                />
                <text
                  x={p.x}
                  y={p.y + 5}
                  fill="#e5d8b3"
                  fontSize="19"
                  textAnchor="middle"
                >
                  {
                    GLYPHS[
                      BODY_NAMES.indexOf(name as (typeof BODY_NAMES)[number])
                    ]
                  }
                </text>
              </g>
            );
          })}
          {selectedEvent &&
            target !== null &&
            (() => {
              const a = point(selectedEvent.longitude, 141, origin),
                b = point(target, 141, origin),
                label = point(target, 165, origin);
              return (
                <g
                  data-exact-longitude={selectedEvent.longitude}
                  data-target-longitude={target}
                >
                  <line
                    x1={a.x}
                    y1={a.y}
                    x2={b.x}
                    y2={b.y}
                    stroke="#e8ce93"
                    strokeWidth="2"
                  />
                  <circle cx={a.x} cy={a.y} r="6" fill="#a0c8b7" />
                  <circle cx={b.x} cy={b.y} r="6" fill="#dfc38a" />
                  <text
                    x={label.x}
                    y={label.y + 5}
                    fontSize="17"
                    textAnchor="middle"
                    fill="#e2c58d"
                  >
                    {GLYPHS[
                      BODY_NAMES.indexOf(
                        selectedEvent.natal_target as (typeof BODY_NAMES)[number],
                      )
                    ] ??
                      (selectedEvent.natal_target === "ascendant"
                        ? "ASC"
                        : "MC")}
                  </text>
                </g>
              );
            })()}
          <circle cx="300" cy="300" r="102" fill="#071b22" stroke="#b6a77d66" />
          <path d="M300 208v184m-92-92h184" stroke="#d8c18b" opacity=".08" />
        </svg>
        <div className="time-date">
          <small>{selectedEvent ? "EXACT CONTACT" : "NATIVE DAILY SKY"}</small>
          <strong>{dateLabel(selectedEvent?.exact_utc ?? frame.utc)}</strong>
          <span>{timeLabel(selectedEvent?.exact_utc ?? frame.utc)} UTC</span>
          <i aria-hidden="true">✧</i>
        </div>
        <div className="time-caustic" aria-hidden="true" />
      </div>
      {!compact && (
        <div className="time-scrub">
          <div>
            <span>
              DAY {index + 1} / {days}
            </span>
            <span>TURN THE SKY</span>
          </div>
          <label className="sr-only" htmlFor={`${id}-scrub`}>
            Explore the daily sky
          </label>
          <input
            id={`${id}-scrub`}
            type="range"
            min="0"
            max={Math.max(0, days - 1)}
            value={index}
            disabled={days === 1}
            onChange={(e) => {
              onEvent?.(null);
              onDay(Number(e.target.value));
            }}
          />
          <div>
            <button
              className="text-button"
              disabled={index === 0}
              onClick={() => {
                onEvent?.(null);
                onDay(index - 1);
              }}
            >
              ← Previous day
            </button>
            <button
              className="text-button"
              disabled={index === days - 1}
              onClick={() => {
                onEvent?.(null);
                onDay(index + 1);
              }}
            >
              Next day →
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
