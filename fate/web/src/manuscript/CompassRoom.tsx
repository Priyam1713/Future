import { useEffect, useRef, useState, type PointerEvent } from "react";
import { api } from "../types";
import type { Oracle } from "../hooks/useOracle";
import { ResultLeaf } from "../components/ResultLeaf";
import {
  EDITION,
  mountains,
  type Envelope,
  type NativeResult,
} from "./contracts";
import { ResultActions } from "./Result";

const northFrames = {
  source_diagram: "Published diagram",
  true: "True north",
  magnetic: "Magnetic north",
  unknown: "Unknown",
};
const roles = {
  source_heading: "Published heading",
  building_facing: "Building facing",
  building_sitting: "Building sitting",
  door: "Door bearing",
  observer: "Observer bearing",
  unknown: "Unknown",
};
type CompassReport = NativeResult & {
  readings: {
    bearing_degrees_display: string;
    uncertainty_tenths: number;
    possible_mountain_ids: string[];
    frame_issues: string[];
    context_status: string;
  }[];
};
function tenths(value: string, max: number) {
  if (!/^\d{1,3}(?:\.\d)?$/.test(value)) return undefined;
  const [degree, decimal = "0"] = value.split(".");
  const n = Number(degree) * 10 + Number(decimal);
  return n <= max ? n : undefined;
}
const display = (value: number) => (value / 10).toFixed(1);
function point(angle: number, radius: number) {
  const rad = ((angle / 10) * Math.PI) / 180;
  return [150 + radius * Math.sin(rad), 150 - radius * Math.cos(rad)];
}

export function CompassRoom({ oracle }: { oracle: Oracle }) {
  const [heading, setHeading] = useState("97.5");
  const [radius, setRadius] = useState("0.0");
  const [north, setNorth] = useState("");
  const [role, setRole] = useState("");
  const [busy, setBusy] = useState(false);
  const [data, setData] = useState<Envelope<CompassReport>>();
  const [error, setError] = useState("");
  const c = useRef<AbortController | null>(null);
  useEffect(() => () => c.current?.abort(), []);
  const angle = tenths(heading, 3599);
  const uncertainty = tenths(radius, 1800);
  const read = data?.result.readings[0];
  function turn(e: PointerEvent<SVGSVGElement>) {
    if (
      busy ||
      (e.type === "pointermove" &&
        !e.currentTarget.hasPointerCapture(e.pointerId))
    )
      return;
    const box = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - (box.left + box.width / 2);
    const y = e.clientY - (box.top + box.height / 2);
    if (Math.hypot(x, y) < box.width * 0.12) return;
    if (e.type === "pointerdown")
      e.currentTarget.setPointerCapture(e.pointerId);
    setHeading(
      display((Math.round((Math.atan2(x, -y) * 1800) / Math.PI) + 3600) % 3600),
    );
    setData(undefined);
  }
  async function submit() {
    if (
      c.current ||
      angle === undefined ||
      uncertainty === undefined ||
      !north ||
      !role
    )
      return;
    const request = new AbortController();
    c.current = request;
    setBusy(true);
    setError("");
    try {
      const output = await api<Envelope<CompassReport>>(
        "/api/sky-manuscript",
        { oracle: 40, bearing: angle, uncertainty, north, role },
        request.signal,
      );
      if (request.signal.aborted) return;
      setData(output);
      oracle.markExplored(40);
      oracle.sound.cue("reveal");
    } catch (ex) {
      if (!request.signal.aborted) setError((ex as Error).message);
    } finally {
      if (!request.signal.aborted) {
        c.current = null;
        setBusy(false);
      }
    }
  }
  return (
    <div className="folio-work compass-work">
      <div className="compass-instrument">
        <svg
          viewBox="0 0 300 300"
          role="img"
          aria-label="Turn the compass or use the bearing input. Engraved IDs follow the source intervals."
          onPointerDown={turn}
          onPointerMove={turn}
        >
          <circle cx="150" cy="150" r="146" className="compass-case" />
          <circle cx="150" cy="150" r="130" className="compass-brass" />
          <circle cx="150" cy="150" r="101" className="compass-brass" />
          <circle cx="150" cy="150" r="71" className="compass-well" />
          {mountains.map((mountain) => {
            const lower = mountain.lower_tenths - 0.5;
            const middle =
              (mountain.lower_tenths +
                mountain.upper_tenths +
                (mountain.wraps_north ? 3600 : 0)) /
              2;
            const [x, y] = point(middle, 115);
            const [x1, y1] = point(lower, 102);
            const [x2, y2] = point(lower, 130);
            return (
              <g
                key={mountain.id}
                data-mountain={mountain.id}
                data-active={
                  read?.possible_mountain_ids.includes(mountain.id) || undefined
                }
              >
                <line x1={x1} y1={y1} x2={x2} y2={y2} />
                <text x={x} y={y} dominantBaseline="middle">
                  {mountain.id}
                </text>
              </g>
            );
          })}
          {["N", "E", "S", "W"].map((dir, i) => {
            const [x, y] = point(i * 900, 86);
            return (
              <text
                key={dir}
                x={x}
                y={y}
                dominantBaseline="middle"
                className="compass-cardinal"
              >
                {dir}
              </text>
            );
          })}
          {angle !== undefined && Boolean(uncertainty) && (
            <circle
              cx="150"
              cy="150"
              r="138"
              pathLength="3600"
              className="compass-uncertainty"
              strokeDasharray={`${2 * (uncertainty ?? 0)} 3600`}
              transform={`rotate(${(angle - (uncertainty ?? 0)) / 10 - 90} 150 150)`}
            />
          )}
          {angle !== undefined && (
            <g
              transform={`rotate(${angle / 10} 150 150)`}
              className="compass-needle"
            >
              <path d="M150 85 L160 149 L150 215 L140 149Z" />
              <path d="M150 85 L160 149 L150 149Z" />
            </g>
          )}
          <circle cx="150" cy="150" r="7" className="compass-pin" />
        </svg>
        <strong>{angle === undefined ? "—" : display(angle) + "°"}</strong>
        <label className="sr-only" htmlFor="compass-scrub">
          Turn bearing
        </label>
        <input
          id="compass-scrub"
          type="range"
          min="0"
          max="3599"
          step="1"
          disabled={busy}
          value={angle ?? 0}
          aria-valuetext={
            angle === undefined ? "Unset" : display(angle) + " degrees"
          }
          onChange={(e) => {
            setHeading(display(e.target.valueAsNumber));
            setData(undefined);
          }}
        />
      </div>
      <div className="folio-desk">
        {read && data ? (
          <section aria-label="Compass result">
            <ResultLeaf
              status="Native classification"
              title={
                read.possible_mountain_ids.length === 1
                  ? (data.mountainViews?.[0].title ?? "")
                  : "This range crosses a boundary"
              }
            >
              <p className="folio-lead">
                {read.bearing_degrees_display}° ±{" "}
                {display(read.uncertainty_tenths)}° ·{" "}
                {read.possible_mountain_ids.join(" / ")}
              </p>
              <p>
                {northFrames[north as keyof typeof northFrames]} ·{" "}
                {roles[role as keyof typeof roles]}
              </p>
            </ResultLeaf>
            <details className="folio-depth">
              <summary>Mountain intervals and sources</summary>
              <ul>
                {data.mountainViews?.map((view) => {
                  const source = view.sources[0];
                  return (
                    <li key={view.title}>
                      <strong>{view.title}</strong> · {view.lead}{" "}
                      {source?.url && (
                        <a href={source.url} target="_blank" rel="noreferrer">
                          {source.locator}
                        </a>
                      )}
                    </li>
                  );
                })}
              </ul>
              <p>
                The native engine checks inclusive printed intervals at 0.1°
                resolution.
              </p>
              {read.frame_issues.map((issue) => (
                <p key={issue}>{issue}</p>
              ))}
            </details>
            <ResultActions
              key={read.bearing_degrees_display}
              oracle={oracle}
              result={data.result}
              name="compass"
              snapshot={{
                oracle: 40,
                profile: EDITION,
                entries: read.possible_mountain_ids,
              }}
            />
            <button className="text-button" onClick={() => setData(undefined)}>
              Change the declaration ←
            </button>
          </section>
        ) : (
          <form
            onSubmit={(e) => {
              e.preventDefault();
              void submit();
            }}
          >
            <p className="eyebrow">Declaring a bearing</p>
            <h2>Set the needle.</h2>
            <div className="folio-pair">
              <label>
                Bearing (°)
                <input
                  inputMode="decimal"
                  value={heading}
                  onChange={(e) => setHeading(e.target.value)}
                  disabled={busy}
                />
              </label>
              <label>
                Uncertainty ± (°)
                <input
                  inputMode="decimal"
                  value={radius}
                  onChange={(e) => setRadius(e.target.value)}
                  disabled={busy}
                />
              </label>
            </div>
            <label>
              North reference
              <select
                required
                value={north}
                onChange={(e) => setNorth(e.target.value)}
                disabled={busy}
              >
                <option value="">Choose a reference</option>
                {Object.entries(northFrames).map(([id, label]) => (
                  <option key={id} value={id}>
                    {label}
                  </option>
                ))}
              </select>
            </label>
            <label>
              What the bearing describes
              <select
                required
                value={role}
                onChange={(e) => setRole(e.target.value)}
                disabled={busy}
              >
                <option value="">Choose a role</option>
                {Object.entries(roles).map(([id, label]) => (
                  <option key={id} value={id}>
                    {label}
                  </option>
                ))}
              </select>
            </label>
            <button
              className="primary"
              disabled={
                busy ||
                angle === undefined ||
                uncertainty === undefined ||
                !north ||
                !role
              }
            >
              Classify the bearing
            </button>
            {(angle === undefined || uncertainty === undefined) && (
              <p role="status">
                Use one decimal place. Bearing 0–359.9°, uncertainty 0–180°.
              </p>
            )}
            {error && <p role="alert">{error}</p>}
          </form>
        )}
      </div>
    </div>
  );
}
