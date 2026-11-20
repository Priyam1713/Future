import { useEffect, useRef, useState } from "react";
import { api } from "../types";

const questions = [
  [
    "shape.type",
    "Hand outline",
    [
      ["square", "Square"],
      ["spatulate", "Wider toward the fingertips"],
      ["philosophic", "Philosophic"],
      ["conic", "Conic"],
      ["psychic", "Psychic, in Cheiro’s terminology"],
      ["mixed", "Mixed"],
    ],
  ],
  [
    "head_life_gap",
    "Where the head and life lines begin",
    [
      ["joined", "Touching"],
      ["medium", "Separated"],
      ["wide", "Widely separated"],
    ],
  ],
  [
    "lines.head.curvature",
    "Head line shape",
    [
      ["straight", "Straight"],
      ["straight_then_sloping", "Straight first, then gently sloping"],
      ["slight_slope", "Gently sloping"],
      ["very_sloping", "Steeply sloping"],
    ],
  ],
  [
    "lines.head.continuity",
    "Head line continuity",
    [
      ["unbroken", "Unbroken"],
      ["broken", "Interrupted"],
      ["chained", "Chain-like"],
    ],
  ],
  [
    "lines.head.clarity",
    "Head line clarity",
    [
      ["clear", "Clear"],
      ["unclear", "Faint"],
    ],
  ],
  [
    "lines.heart.origin",
    "Heart line endpoint toward the index finger",
    [
      ["jupiter", "Below the index finger"],
      ["between_jupiter_saturn", "Between index and middle fingers"],
      ["saturn", "Below the middle finger"],
    ],
  ],
  [
    "lines.heart.continuity",
    "Heart line continuity",
    [
      ["unbroken", "Unbroken"],
      ["broken", "Interrupted"],
      ["chained", "Chain-like"],
    ],
  ],
  [
    "lines.life.branch_to",
    "Ascending branch from the life line",
    [
      ["jupiter", "Toward the index finger"],
      ["none", "No visible branch"],
    ],
  ],
  ...(
    [
      ["venus", "Thumb base"],
      ["jupiter", "Below the index finger"],
      ["saturn", "Below the middle finger"],
      ["sun", "Below the ring finger"],
      ["mercury", "Below the little finger"],
      ["mars_active", "Inside the life line"],
      ["mars_passive", "Outer edge above the lower palm"],
      ["luna", "Outer edge of the lower palm"],
    ] as const
  ).map(
    ([id, label]) =>
      [
        `mounts.${id}.prominence`,
        `Padding ${label.toLowerCase()}`,
        [
          ["developed", "Clearly raised"],
          ["flat", "Flat"],
          ["excessive", "Very prominent"],
        ],
      ] as const,
  ),
] as const;

type Narrative = {
  title: string;
  chapters: { title: string; body: string; rule_ids: string[] }[];
  connections: { body: string; rule_ids: string[] }[];
  abstained: boolean;
};
type Rule = { id: string; text: string; locator: string; exceptions: string[] };
type Report = {
  narrative: Narrative;
  supplement: Rule[];
  native: {
    source: { url: string; edition: string };
    hands: { readings: Rule[]; observation_conflicts: { reason: string }[] }[];
  };
};
type Mark = { x: number; y: number; line: string };

export function PalmPhoto({ onRead }: { onRead: () => void }) {
  const [photo, setPhoto] = useState("");
  const [consent, setConsent] = useState(false);
  const [confirmed, setConfirmed] = useState(false);
  const [side, setSide] = useState("");
  const [values, setValues] = useState<Record<string, string>>({});
  const [line, setLine] = useState("head");
  const [marks, setMarks] = useState<Mark[]>([]);
  const [error, setError] = useState("");
  const [report, setReport] = useState<Report>();
  const [busy, setBusy] = useState(false);
  const pending = useRef<AbortController | null>(null);
  const generation = useRef(0);
  const reportHeading = useRef<HTMLHeadingElement>(null);
  useEffect(
    () => () => {
      if (photo) URL.revokeObjectURL(photo);
    },
    [photo],
  );
  useEffect(
    () => () => {
      generation.current++;
      pending.current?.abort();
    },
    [],
  );
  useEffect(() => {
    if (report) reportHeading.current?.focus();
  }, [report]);
  function clear() {
    setPhoto("");
    setMarks([]);
    setValues({});
    setSide("");
    setConfirmed(false);
    setReport(undefined);
  }
  async function intake(file: File | undefined) {
    const check = ++generation.current;
    clear();
    setError("");
    if (!file || !consent) return;
    if (
      !["image/png", "image/jpeg", "image/webp"].includes(file.type) ||
      file.size > 5 * 1024 * 1024
    ) {
      setError("Choose a JPEG, PNG or WebP under 5 MB.");
      return;
    }
    setBusy(true);
    let bitmap: ImageBitmap | undefined;
    try {
      bitmap = await createImageBitmap(file);
      if (
        Math.min(bitmap.width, bitmap.height) < 320 ||
        bitmap.width * bitmap.height > 24000000
      )
        throw Error(
          "Use an image at least 320 pixels on both sides and under 24 megapixels.",
        );
      const canvas = document.createElement("canvas");
      canvas.width = canvas.height = 64;
      const context = canvas.getContext("2d");
      if (!context)
        throw Error("Image checking is unavailable in this browser.");
      context.drawImage(bitmap, 0, 0, 64, 64);
      const pixels = context.getImageData(0, 0, 64, 64).data;
      let mean = 0,
        square = 0;
      for (let i = 0; i < pixels.length; i += 4) {
        const luma =
          (pixels[i] * 0.2126 +
            pixels[i + 1] * 0.7152 +
            pixels[i + 2] * 0.0722) *
          (pixels[i + 3] / 255);
        mean += luma;
        square += luma * luma;
      }
      mean /= 4096;
      if (mean < 28 || mean > 237 || square / 4096 - mean * mean < 100)
        throw Error(
          "The image is too dark, bright or flat to review. Try even light.",
        );
      if (check === generation.current) setPhoto(URL.createObjectURL(file));
    } catch (e) {
      if (check === generation.current)
        setError(
          e instanceof Error ? e.message : "This image could not be decoded.",
        );
    } finally {
      bitmap?.close();
      if (check === generation.current) setBusy(false);
    }
  }
  async function read() {
    if (!photo || !side || !confirmed || pending.current) return;
    const hand: {
      side: string;
      shape: Record<string, string>;
      lines: Record<string, Record<string, string>>;
      mounts: Record<string, Record<string, string>>;
      head_life_gap?: string;
    } = { side, shape: {}, lines: {}, mounts: {} };
    for (const [key, value] of Object.entries(values)) {
      if (value === "unknown" || key === "fingertips" || key === "mount_lean")
        continue;
      const [group, name, field] = key.split(".");
      if (group === "head_life_gap") {
        hand.head_life_gap = value;
        hand.lines.head = { ...hand.lines.head, presence: "present" };
        hand.lines.life = { ...hand.lines.life, presence: "present" };
      } else if (group === "shape") hand.shape[name] = value;
      else if (group === "lines")
        hand.lines[name] = {
          ...hand.lines[name],
          presence: "present",
          [field]: value,
        };
      else hand.mounts[name] = { [field]: value };
    }
    const c = new AbortController();
    pending.current = c;
    setBusy(true);
    setError("");
    setReport(undefined);
    try {
      const r = await api<Report>(
        "/api/palm-reading",
        {
          confirmed: true,
          hand,
          fingertips: values.fingertips ?? "unknown",
          mount_lean: values.mount_lean ?? "unknown",
        },
        c.signal,
      );
      if (!c.signal.aborted) {
        setReport(r);
        onRead();
      }
    } catch (e) {
      if (!c.signal.aborted) setError((e as Error).message);
    } finally {
      pending.current = null;
      if (!c.signal.aborted) setBusy(false);
    }
  }
  const fields = (extra: boolean) => (
    <div className="palm-questions">
      {questions
        .filter(
          ([key]) =>
            (key.startsWith("mounts.") || key.startsWith("shape.")) === extra,
        )
        .map(([key, label, options]) => (
          <label key={key}>
            {label}
            <select
              value={values[key] ?? "unknown"}
              onChange={(e) => {
                setValues({ ...values, [key]: e.target.value });
                setConfirmed(false);
                setReport(undefined);
              }}
            >
              <option value="unknown">Leave open</option>
              {options.map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
        ))}
    </div>
  );
  return (
    <section className="palm-studio" aria-label="Photo-guided palm reading">
      <header>
        <p className="eyebrow">Palmistry</p>
        <h2>Read from your own hand</h2>
        <p>
          Use a clear photo of your open palm. The photo stays in this browser
          tab. Only the descriptions you confirm are sent for the reading.
        </p>
      </header>
      {!photo && (
        <label>
          <input
            type="checkbox"
            checked={consent}
            disabled={busy}
            onChange={(e) => setConsent(e.target.checked)}
          />{" "}
          I have permission to review this photo
        </label>
      )}
      {!photo && (
        <label>
          Palm photograph{" "}
          <input
            type="file"
            accept="image/jpeg,image/png,image/webp"
            disabled={!consent || busy}
            onChange={(e) => void intake(e.target.files?.[0])}
          />
        </label>
      )}
      {photo && (
        <div className="palm-layout">
          <div>
            <div className="palm-photo-frame">
              <img
                src={photo}
                alt="Your selected palm for manual review"
                onClick={(e) => {
                  if (busy || marks.length >= 60) return;
                  const r = e.currentTarget.getBoundingClientRect();
                  setMarks([
                    ...marks,
                    {
                      x: ((e.clientX - r.left) / r.width) * 100,
                      y: ((e.clientY - r.top) / r.height) * 100,
                      line,
                    },
                  ]);
                }}
              />
              <svg
                viewBox="0 0 100 100"
                preserveAspectRatio="none"
                aria-hidden="true"
              >
                {["head", "heart", "life"].map((name) => (
                  <polyline
                    key={name}
                    data-line={name}
                    points={marks
                      .filter((m) => m.line === name)
                      .map((m) => `${m.x},${m.y}`)
                      .join(" ")}
                  />
                ))}
                {marks.map((m, i) => (
                  <circle
                    key={i}
                    cx={m.x}
                    cy={m.y}
                    r="1.1"
                    data-line={m.line}
                  />
                ))}
              </svg>
            </div>
            <label>
              Optional overlay{" "}
              <select value={line} onChange={(e) => setLine(e.target.value)}>
                <option>head</option>
                <option>heart</option>
                <option>life</option>
              </select>
            </label>
            <p>
              Tap visible points in order to trace a crease. Marks stay with the
              photo and do not affect the reading.
            </p>
            <button
              className="text-button"
              disabled={!marks.length || busy}
              onClick={() => setMarks(marks.slice(0, -1))}
            >
              Undo last point
            </button>
            <button className="text-button" disabled={busy} onClick={clear}>
              Remove photo
            </button>
          </div>
          <div>
            <p>
              Lighting and size checked. Choose the hand yourself and leave any
              unclear feature blank.
            </p>
            <fieldset disabled={busy}>
              <legend>What you can see</legend>
              <label>
                Photographed hand{" "}
                <select
                  value={side}
                  onChange={(e) => {
                    setSide(e.target.value);
                    setConfirmed(false);
                    setReport(undefined);
                  }}
                >
                  <option value="">Select a hand</option>
                  <option value="left">Left</option>
                  <option value="right">Right</option>
                </select>
              </label>
              {fields(false)}
              <details>
                <summary>Hand shape, padding and combinations</summary>
                {fields(true)}
                <label>
                  Fingertips on a square hand{" "}
                  <select
                    value={values.fingertips ?? "unknown"}
                    onChange={(e) => {
                      setValues({ ...values, fingertips: e.target.value });
                      setConfirmed(false);
                      setReport(undefined);
                    }}
                  >
                    <option value="unknown">Leave open</option>
                    <option value="conic">Conic or tapered</option>
                  </select>
                </label>
                <label>
                  Padding visibly leaning toward another area{" "}
                  <select
                    value={values.mount_lean ?? "unknown"}
                    onChange={(e) => {
                      setValues({ ...values, mount_lean: e.target.value });
                      setConfirmed(false);
                      setReport(undefined);
                    }}
                  >
                    <option value="unknown">Leave open</option>
                    <option value="saturn_jupiter">Middle toward index</option>
                    <option value="saturn_sun">Middle toward ring</option>
                    <option value="sun_mercury">
                      Ring toward little finger
                    </option>
                  </select>
                </label>
              </details>
              <label>
                <input
                  type="checkbox"
                  checked={confirmed}
                  onChange={(e) => setConfirmed(e.target.checked)}
                />{" "}
                I confirmed these descriptions against the photo
              </label>
              <button
                className="primary"
                disabled={!confirmed || !side}
                onClick={() => void read()}
              >
                Open my palm reading
              </button>
            </fieldset>
          </div>
        </div>
      )}
      {error && <p role="alert">{error}</p>}
      {busy && <p role="status">Working on your request…</p>}
      {report && (
        <article aria-live="polite" className="palm-report">
          <h3 ref={reportHeading} tabIndex={-1}>
            {report.narrative.title}
          </h3>
          {report.narrative.abstained && (
            <p>
              Cheiro’s rules in this edition need a clearer or more complete
              feature. Leave uncertain details open.
            </p>
          )}
          {report.narrative.chapters.map((chapter) => (
            <section key={chapter.title}>
              <h4>{chapter.title}</h4>
              <p>{chapter.body}</p>
            </section>
          ))}
          {report.narrative.connections.map((c) => (
            <p key={c.body}>{c.body}</p>
          ))}
          {report.native.hands[0].observation_conflicts.map((c) => (
            <p key={c.reason}>
              {c.reason}. That part of the reading was withheld.
            </p>
          ))}
          <p>Cheiro’s historical symbolism is a lens for reflection.</p>
          <details>
            <summary>Source and matched observations</summary>
            <a href={report.native.source.url} target="_blank" rel="noreferrer">
              {report.native.source.edition}
            </a>
            {[...report.native.hands[0].readings, ...report.supplement].map(
              (r) => (
                <section key={r.id}>
                  <p>{r.text}</p>
                  <small>{r.locator}</small>
                  {r.exceptions.map((x) => (
                    <p key={x}>{x}</p>
                  ))}
                </section>
              ),
            )}
          </details>
        </article>
      )}
    </section>
  );
}
