import { useId, useState, type CSSProperties } from "react";
import type {
  InstrumentData,
  Mark,
  Node as TreeNode,
  Track,
} from "./contracts";

const paints = ["#ffe0a3", "#87dfcb", "#b6aadd", "#eaa7a7"];

function Bars({
  rows,
  proportional = false,
}: {
  rows: Mark[];
  proportional?: boolean;
}) {
  const limit = proportional
    ? 1
    : Math.max(1e-9, ...rows.map((r) => Math.abs(r.value)));
  return (
    <dl className="lab-bars">
      {rows.map(({ label, value }, i) => (
        <div key={label}>
          <dt>{label}</dt>
          <dd>
            <span className="bar-track">
              <i
                style={
                  {
                    "--length": (Math.abs(value) / limit) * 100 + "%",
                    "--ink": paints[i % paints.length],
                  } as CSSProperties
                }
              />
            </span>
            <b>
              {proportional
                ? (value * 100).toFixed(value > 0.995 && value < 1 ? 2 : 1) +
                  "%"
                : Number(value.toFixed(4))}
            </b>
          </dd>
        </div>
      ))}
    </dl>
  );
}

function Viewport({
  tracks,
  label,
  markers = false,
  sequence,
  frame,
}: {
  tracks: Track[];
  label: string;
  markers?: boolean;
  sequence?: boolean;
  frame?: number;
}) {
  const scale = (min: number, max: number, t: number, size: number) =>
    t +
    (max === min ? 0.5 : (size - min) / (max - min)) * (t === 32 ? 476 : 210);
  const source = tracks.flatMap((row) => row.points);
  const dx = source.map(([x]) => x),
    dy = source.map(([, y]) => y);
  const loX = Math.min(...dx),
    hiX = Math.max(...dx),
    loY = Math.min(...dy),
    hiY = Math.max(...dy);
  const location = ([x, y]: [number, number]) => [
    scale(loX, hiX, 32, x),
    238 - scale(loY, hiY, 14, y),
  ];
  return (
    <svg
      viewBox="0 0 540 264"
      role="img"
      aria-label={label}
      className={sequence ? "lab-orbit-plot" : "lab-plot"}
    >
      <g className="plot-grid">
        {[22, 64, 106, 148, 190, 232].map((y) => (
          <path key={y} d={`M28 ${y}H514`} />
        ))}
        {[32, 111, 190, 269, 348, 427, 506].map((x) => (
          <path key={x} d={`M${x} 22V232`} />
        ))}
      </g>
      <text x="31" y="253" className="plot-label">
        {sequence ? "X / Z PHASE PLANE" : "OBSERVATION AXIS"}
      </text>
      {tracks.map((row, i) => {
        const used =
          sequence && frame !== undefined
            ? row.points.slice(0, frame + 1)
            : row.points;
        const coordinates = used.map(location);
        const color = paints[i % paints.length];
        return (
          <g key={row.label} stroke={color} fill={color}>
            {coordinates.length > 1 && (
              <polyline
                points={coordinates.map((p) => p.join(",")).join(" ")}
                fill="none"
                strokeWidth={sequence ? 1.4 : 2.4}
                strokeDasharray={i === 1 && !sequence ? "7 5" : undefined}
              />
            )}
            {(markers ? coordinates : coordinates.slice(-1)).map(
              ([x, y], k) => (
                <circle key={k} cx={x} cy={y} r={4} />
              ),
            )}
          </g>
        );
      })}
    </svg>
  );
}

export function Scrubber({
  value,
  max,
  label,
  onChange,
  caption,
}: {
  value: number;
  max: number;
  label: string;
  onChange: (n: number) => void;
  caption?: string;
}) {
  return (
    <label className="lab-scrubber">
      <span>
        {label} <strong>{caption ?? value}</strong>
      </span>
      <input
        type="range"
        min={0}
        max={max}
        step={1}
        value={value}
        disabled={max === 0}
        onChange={(e) => onChange(e.target.valueAsNumber)}
        aria-valuetext={caption ?? String(value)}
      />
    </label>
  );
}

function Circuit({ data }: { data: InstrumentData }) {
  return (
    <div className="circuit-board">
      <svg
        viewBox="0 0 450 180"
        role="img"
        aria-label="Native circuit gate diagram"
      >
        {[58, 121].map((y, i) => (
          <g key={y}>
            <line x1="45" x2="420" y1={y} y2={y} />
            <text x="24" y={y + 5}>
              q{i}
            </text>
            <circle cx="411" cy={y} r="12" />
          </g>
        ))}
        {data.gates?.map(({ op, target, control }, i) => {
          const x = 125 + i * 88,
            y = 58 + target * 63;
          return (
            <g key={i} className="gate">
              {control === undefined ? (
                <>
                  <rect x={x - 19} y={y - 18} width="38" height="36" rx="3" />
                  <text x={x} y={y + 5}>
                    {op.toUpperCase()}
                  </text>
                </>
              ) : (
                <>
                  <line x1={x} x2={x} y1={58 + control * 63} y2={y} />
                  <circle cx={x} cy={58 + control * 63} r="7" className="pin" />
                  <circle cx={x} cy={y} r="15" />
                  <text x={x} y={y + 5}>
                    +
                  </text>
                </>
              )}
            </g>
          );
        })}
      </svg>
      <Bars rows={data.bars ?? []} proportional />
    </div>
  );
}

function Dial({ value, label }: { value: number; label: string }) {
  const id = useId();
  return (
    <div className="lab-dial">
      <svg viewBox="0 0 160 160" role="img" aria-label={label}>
        <defs>
          <radialGradient id={id}>
            <stop stopColor="#2e5149" />
            <stop offset="1" stopColor="#101e28" />
          </radialGradient>
        </defs>
        <circle cx="80" cy="80" r="73" fill={`url(#${id})`} stroke="#ae9163" />
        <circle
          cx="80"
          cy="80"
          r="62"
          fill="none"
          stroke="#c0a77e"
          strokeDasharray="1 4"
        />
        <circle
          cx="80"
          cy="80"
          r="52"
          fill="none"
          stroke="#416b63"
          strokeWidth="7"
        />
        <circle
          cx="80"
          cy="80"
          r="52"
          fill="none"
          stroke="#eed6a2"
          strokeWidth="7"
          pathLength="100"
          strokeLinecap="round"
          strokeDasharray={`${value * 100} 100`}
          transform="rotate(-90 80 80)"
        />
        <text x="80" y="86" textAnchor="middle" fill="#f3e0b0" fontSize="23">
          {(value * 100).toFixed(value > 0.995 && value < 1 ? 2 : 1)}%
        </text>
      </svg>
      <span>{label}</span>
    </div>
  );
}

function SignalNetwork({
  names,
  links,
  active,
  dag,
}: {
  names: string[];
  links: [string, string][];
  active?: number[];
  dag?: boolean;
}) {
  const id = useId();
  const positions = names.map((label, i) => ({
    label,
    x: 85 + i * (272 / Math.max(1, names.length - 1)),
    y: dag ? (i === 0 ? 48 : 147) : i === 1 ? 82 : 137,
  }));
  return (
    <svg
      viewBox="0 0 445 213"
      role="img"
      aria-label={
        dag ? "Declared causal graph" : "Native population activation"
      }
      className="lab-network"
    >
      <defs>
        <marker
          id={id}
          markerWidth="10"
          markerHeight="10"
          refX="7"
          refY="3"
          orient="auto"
          viewBox="0 0 8 6"
        >
          <path d="M0 0L8 3 0 6Z" fill="#c6ad7e" />
        </marker>
      </defs>
      {links.map(([source, target], i) => {
        const a = positions.find((p) => p.label === source),
          b = positions.find((p) => p.label === target);
        if (!a || !b) return null;
        const d = Math.hypot(b.x - a.x, b.y - a.y),
          gap = dag ? 30 : 27;
        const x = ((b.x - a.x) * gap) / d,
          y = ((b.y - a.y) * gap) / d;
        return (
          <line
            key={i}
            x1={a.x + x}
            y1={a.y + y}
            x2={b.x - x}
            y2={b.y - y}
            markerEnd={dag ? `url(#${id})` : undefined}
          />
        );
      })}
      {positions.map((p, i) => (
        <g key={p.label} data-active={active?.[i] === 1}>
          <circle cx={p.x} cy={p.y} r="34" className="outer" />
          <circle cx={p.x} cy={p.y} r="24" />
          <text x={p.x} y={p.y + 5} textAnchor="middle">
            {p.label}
          </text>
        </g>
      ))}
    </svg>
  );
}

function Branches({ nodes }: { nodes: TreeNode[] }) {
  const root = nodes.find((n) => n.parent === null);
  const [chosen, setChosen] = useState(root?.id ?? "");
  if (!root) return null;
  const layers = nodes.reduce<Record<number, TreeNode[]>>((acc, node) => {
    (acc[node.depth] ??= []).push(node);
    return acc;
  }, {});
  const coord = Object.entries(layers).flatMap(([level, items]) =>
    items.map((n, i) => ({
      ...n,
      x: 52 + Number(level) * 154,
      y: ((i + 1) * 244) / (items.length + 1),
    })),
  );
  const detail = nodes.find((n) => n.id === chosen) ?? root;
  return (
    <div className="lab-tree">
      <svg
        viewBox="0 0 440 244"
        role="img"
        aria-label="Native scenario branch weights"
      >
        {coord
          .filter((n) => n.parent)
          .map((n) => {
            const p = coord.find((p) => p.id === n.parent)!;
            return (
              <path
                key={n.id}
                d={`M${p.x + 19} ${p.y}C${p.x + 80} ${p.y},${n.x - 70} ${n.y},${n.x - 20} ${n.y}`}
              />
            );
          })}
        {coord.map((n) => (
          <g key={n.id} data-active={n.id === detail.id}>
            <rect x={n.x - 20} y={n.y - 15} width="40" height="30" rx="4" />
            <text x={n.x} y={n.y + 4}>
              {n.id}
            </text>
            <text x={n.x} y={n.y + 32} className="branch-mass">
              {n.mass}
            </text>
          </g>
        ))}
      </svg>
      <div className="lab-picks" aria-label="Explore a branch">
        {nodes.map((n) => (
          <button
            type="button"
            key={n.id}
            aria-pressed={detail.id === n.id}
            onClick={() => setChosen(n.id)}
          >
            {n.id}
          </button>
        ))}
      </div>
      <p className="instrument-note">
        {detail.id} · mass {detail.mass}
        {detail.utility !== null ? " · utility " + detail.utility : ""}
      </p>
    </div>
  );
}

export function Ribbon({
  labels,
  notes = [],
}: {
  labels: string[];
  notes?: string[];
}) {
  return (
    <ol className="lab-ribbon">
      {labels.map((line, i) => (
        <li key={i}>
          <b>{line}</b>
          {notes[i] && <small>{notes[i]}</small>}
        </li>
      ))}
    </ol>
  );
}

export function Instrument({
  kind,
  data,
  seed,
  setSeed,
}: {
  kind: string;
  data?: InstrumentData;
  seed: number[] | null;
  setSeed: (grid: number[] | null) => void;
}) {
  const [step, setStep] = useState(kind === "orbit" ? 999 : 0);
  if (!data)
    return (
      <div className={`lab-spinner lab-${kind}-waiting`} aria-hidden="true">
        <i />
        <i />
        <i />
      </div>
    );
  const frames = data.frames ?? [];
  const count = Math.max(frames.length, data.counts?.length ?? 0);
  const tick = Math.min(step, Math.max(0, count - 1));
  if (kind === "cells") {
    const grid = seed ?? frames[tick] ?? Array(49).fill(0);
    return (
      <div className="cell-instrument">
        <div
          className="cell-loom"
          role="group"
          aria-label="Edit the 7 by 7 seed"
        >
          {grid.map((bit, i) => (
            <button
              key={i}
              type="button"
              data-lit={bit === 1}
              aria-pressed={bit === 1}
              aria-label={`Cell ${Math.floor(i / 7) + 1},${(i % 7) + 1}`}
              disabled={!seed && tick !== 0}
              onClick={() => {
                const draft = [...(seed ?? frames[0] ?? grid)];
                draft[i] = 1 - draft[i];
                setSeed(draft);
              }}
            />
          ))}
        </div>
        {seed ? (
          <p className="instrument-note">
            Seed edited · run the loom to compute new generations.
          </p>
        ) : (
          <Scrubber
            label="Generation"
            value={tick}
            max={frames.length - 1}
            onChange={setStep}
          />
        )}
      </div>
    );
  }
  if (kind === "circuit") return <Circuit data={data} />;
  if (kind === "tree") return <Branches nodes={data.nodes ?? []} />;
  if (kind === "network" || kind === "graph")
    return (
      <>
        <SignalNetwork
          names={data.labels ?? []}
          links={data.links ?? []}
          active={frames[tick]}
          dag={kind === "graph"}
        />
        {kind === "network" && (
          <Scrubber
            label="Native round"
            value={tick}
            max={frames.length - 1}
            onChange={setStep}
            caption={String(tick + 1)}
          />
        )}
        {data.bars && <Bars rows={data.bars} proportional />}
      </>
    );
  if (kind === "posterior" || kind === "market")
    return (
      <div className="dial-pair">
        {data.bars?.map((m) => (
          <Dial key={m.label} value={m.value} label={m.label} />
        ))}
      </div>
    );
  if (kind === "pool")
    return (
      <div className="pool-instrument">
        <svg
          viewBox="0 0 420 120"
          role="img"
          aria-label="Two declared forecasts converge on the pool"
        >
          <path
            d="M94 20Q147 20 202 85 M326 20Q273 20 218 85"
            stroke="#bd9e69"
            fill="none"
          />
          {[94, 326, 210].map((x, i) => (
            <circle
              key={x}
              cx={x}
              cy={i === 2 ? 90 : 20}
              r={i === 2 ? 18 : 11}
              fill={paints[i]}
            />
          ))}
        </svg>
        <Bars rows={data.bars ?? []} proportional />
      </div>
    );
  if (kind === "scatter")
    return (
      <>
        <Viewport
          tracks={(data.points ?? []).map((row) => ({
            label: row.label,
            points: [row.xy],
          }))}
          label="Held-out feature and training centroids"
          markers
        />
        <p className="instrument-note">
          Gold A · teal B · violet held-out vector
        </p>
        <Bars rows={data.bars ?? []} />
      </>
    );
  if (data.series)
    return (
      <>
        <Viewport
          tracks={data.series}
          label={
            kind === "orbit"
              ? "Lorenz X/Z trajectories"
              : "Native observations and model traces"
          }
          markers={kind !== "orbit"}
          sequence={kind === "orbit"}
          frame={kind === "orbit" ? Math.max(1, tick) : undefined}
        />
        <p className="instrument-note">
          {data.series.map(({ label }) => label).join(" · ")}
        </p>
        {kind === "orbit" && (
          <Scrubber
            value={tick}
            max={count - 1}
            onChange={setStep}
            label="Native sample"
            caption={`t=${data.labels?.[tick]} · distance ${data.counts?.[tick]?.toFixed(3)}`}
          />
        )}
      </>
    );
  if (data.bars) return <Bars rows={data.bars} />;
  return (
    <div className={`archive-artefact archive-artefact-${kind}`}>
      {data.text && <blockquote>{data.text}</blockquote>}
      {kind === "index" && (
        <div className="folio-rings" aria-hidden="true">
          <i />
          <i />
          <i />
        </div>
      )}
      {data.labels && (
        <Ribbon
          labels={data.labels}
          notes={kind === "cue" || kind === "ledger" ? data.notes : []}
        />
      )}
    </div>
  );
}
