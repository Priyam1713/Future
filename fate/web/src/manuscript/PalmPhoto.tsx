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
const supplements = [
  ["fingertips", "Fingertips on a square hand", [["conic", "Tapered"]]],
  ["mount_lean", "Does the padding lean toward a neighboring finger?", [
    ["saturn_jupiter", "Middle toward index"], ["saturn_sun", "Middle toward ring"],
    ["sun_mercury", "Ring toward little finger"],
  ]],
] as const;

const guides = [
  ["M141 122 Q103 108 67 127", "Look for the upper crease below the fingers, starting at the little-finger edge."],
  ["M78 156 Q114 145 140 170", "Look for the middle crease that crosses the palm from the thumb side."],
  ["M79 151 Q107 178 82 216", "Look for the crease that curves around the base of the thumb."],
] as const;

const paddingLocations: Record<string, [number, number]> = {
  venus: [68, 181], jupiter: [82, 127], saturn: [104, 117],
  sun: [123, 115], mercury: [144, 120], mars_active: [76, 145],
  mars_passive: [140, 153], luna: [132, 191],
};

function PalmGuide({ feature, side }: { feature: string; side: string }) {
  const active = feature.includes("heart") ? [0] : feature.includes("head_life") ? [1, 2] :
    feature.includes("head") ? [1] : feature.includes("life") ? [2] : [];
  const padding = paddingLocations[feature.split(".")[1]];
  const caption = padding ? "Compare the padding in the highlighted area with the rest of your palm."
    : feature === "shape.type" ? "Look at the outline from the wrist to the base of the fingers."
    : feature === "fingertips" ? "Look at the tips of the fingers on your square palm."
    : feature === "mount_lean" ? "Look just below the fingers and compare adjacent areas."
    : active.length === 2 ? "Compare where the middle crease and the crease around the thumb begin."
    : active.length ? guides[active[0]][1] : "Use the fingers, thumb base and wrist to orient your palm.";
  return <figure className="palm-guide">
    <svg viewBox="0 0 200 248" role="img" aria-label="Illustrated palm anatomy guide">
      <g transform={side === "left" ? "translate(200 0) scale(-1 1)" : undefined}>
        <path className="guide-outline" data-active={feature === "shape.type"} d="M77 235 Q78 213 63 198 L34 160 Q26 146 37 143 Q45 142 61 158 L51 83 Q50 70 58 70 Q67 69 70 82 L83 122 L78 49 Q77 32 87 31 Q98 31 100 46 L107 106 L111 29 Q113 16 122 18 Q133 20 132 34 L129 108 L144 54 Q148 43 157 47 Q165 50 161 63 L152 132 Q156 158 147 182 Q133 212 135 235 Z" />
        {padding && <circle className="guide-highlight" cx={padding[0]} cy={padding[1]} r="10" />}
        {feature === "fingertips" && [[61,76], [88,38], [121,26], [152,53]].map(([x,y]) =>
          <circle className="guide-highlight" key={x} cx={x} cy={y} r="7" />)}
        {feature === "mount_lean" && <path className="guide-highlight" d="M79 134 Q110 116 147 126" />}
        {guides.map(([path], index) => <path key={path} d={path} data-active={active.includes(index)} />)}
      </g>
    </svg>
    <figcaption>{caption}</figcaption>
  </figure>;
}

export function PalmPhoto({ onRead }: { onRead: () => void }) {
  const [photo, setPhoto] = useState("");
  const [consent, setConsent] = useState(false);
  const [confirmed, setConfirmed] = useState(false);
  const [side, setSide] = useState("");
  const [values, setValues] = useState<Record<string, string>>({});
  const [manual, setManual] = useState(false);
  const [step, setStep] = useState(0);
  const [review, setReview] = useState(false);
  const [camera, setCamera] = useState(false);
  const video = useRef<HTMLVideoElement>(null);
  const stream = useRef<MediaStream | null>(null);
  const sectionHeading = useRef<HTMLHeadingElement>(null);
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
      stream.current?.getTracks().forEach((track) => track.stop());
    },
    [],
  );
  useEffect(() => {
    if (report) reportHeading.current?.focus();
  }, [report]);
  function clear() {
    setPhoto("");
    generation.current++;
    pending.current?.abort();
    pending.current = null;
    stream.current?.getTracks().forEach((track) => track.stop());
    stream.current = null;
    setCamera(false);
    setBusy(false);
    setManual(false);
    setReview(false);
    setStep(0);
    setError("");
    setValues({});
    setSide("");
    setConfirmed(false);
    setReport(undefined);
  }
  async function intake(file: File | undefined) {
    clear();
    const check = generation.current;
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
    if ((!photo && !manual) || !side || !confirmed || pending.current) return;
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
      if (pending.current === c) pending.current = null;
      if (!c.signal.aborted) setBusy(false);
    }
  }
  const examining = Boolean(photo || manual);
  const ordered = [questions[2], questions[5], questions[7], questions[1], questions[3],
    questions[4], questions[6], questions[0], ...questions.slice(8), ...supplements];
  const selected = ordered[step - 1];
  const focusQuestion = () => requestAnimationFrame(() => sectionHeading.current?.focus());
  const move = (next: number) => { setStep(next); focusQuestion(); };
  const openReview = () => { setReview(true); focusQuestion(); };
  useEffect(() => {
    if (examining && !report) sectionHeading.current?.focus();
  }, [examining, report]);

  async function startCamera() {
    const check = ++generation.current;
    setError("");
    setBusy(true);
    try {
      const opened = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: { ideal: "environment" } }, audio: false,
      });
      if (check !== generation.current) {
        opened.getTracks().forEach((track) => track.stop());
        return;
      }
      stream.current = opened;
      setCamera(true);
    } catch {
      if (check === generation.current) setError("Camera unavailable. Choose an existing photo or examine your hand directly.");
    } finally {
      if (check === generation.current) setBusy(false);
    }
  }
  useEffect(() => {
    if (camera && video.current) video.current.srcObject = stream.current;
  }, [camera]);
  function capture() {
    const frame = video.current;
    if (!frame?.videoWidth || !frame.videoHeight) return;
    const canvas = document.createElement("canvas");
    canvas.width = frame.videoWidth;
    canvas.height = frame.videoHeight;
    canvas.getContext("2d")?.drawImage(frame, 0, 0);
    const check = generation.current;
    canvas.toBlob((blob) => {
      if (blob && check === generation.current) void intake(new File([blob], "palm.jpg", { type: blob.type }));
    }, "image/jpeg", 0.9);
  }
  return (
    <section className="palm-studio" aria-label="Palm reading">
      <ol className="palm-progress" aria-label="Reading progress">
        {["Capture", "Examine", "Reading"].map((name, index) =>
          <li key={name} aria-current={(report ? 2 : examining ? 1 : 0) === index ? "step" : undefined}>{name}</li>)}
      </ol>
      {!examining && <>
        <h2>Begin with an open palm</h2>
        <p>Frame one hand in even light, from wrist to fingertips.</p>
        <label className="palm-consent"><input type="checkbox" checked={consent} disabled={busy || camera}
          onChange={(e) => setConsent(e.target.checked)} /> I have permission to review this photo</label>
        <div className="palm-actions">
          {!camera && <button className="primary" disabled={!consent || busy} onClick={() => void startCamera()}>Use camera</button>}
          <label className="palm-upload">Choose a photo<input aria-label="Palm photograph" type="file"
            accept="image/jpeg,image/png,image/webp" disabled={!consent || busy || camera}
            onChange={(e) => { const file = e.target.files?.[0]; e.target.value = ""; if (file) void intake(file); }} /></label>
          {!camera && <button className="text-button" disabled={busy} onClick={() => setManual(true)}>Examine without a photo</button>}
        </div>
        <p className="palm-note">Photos stay in this tab. Only the observations you confirm are sent for the reading.</p>
        {camera && <div className="palm-camera">
          <video ref={video} autoPlay muted playsInline aria-label="Live camera preview" />
          <div className="palm-actions"><button className="primary" onClick={capture}>Take photo</button>
            <button className="text-button" onClick={clear}>Close camera</button></div>
        </div>}
      </>}
      {examining && !report && <div className="palm-layout">
        <div className="palm-view">
          {photo && <img className="palm-image" src={photo} alt="Your selected palm for manual review" />}
          <PalmGuide feature={review ? "" : selected?.[0] ?? ""} side={side} />
        </div>
        <div className="palm-examine">
          <p className="eyebrow">{review ? "Before the reading" : step > 3 ? "Further observations" : "Examine your hand"}</p>
          <h2 ref={sectionHeading} tabIndex={-1}>{review ? "Review your observations" : selected?.[1] ?? "Which hand are you looking at?"}</h2>
          {review ? <>
            <dl className="palm-review">
              <div><dt>Hand</dt><dd>{side}</dd></div>
              {ordered.flatMap(([key, label, options]) => !values[key] ? [] :
                [<div key={key}><dt>{label}</dt><dd>{options.find(([value]) => value === values[key])?.[1]}</dd></div>])}
            </dl>
            {Object.keys(values).length === 0 && <p>No features selected. You can revise your observations or see what the reading can establish.</p>}
            <label className="palm-consent"><input type="checkbox" checked={confirmed}
              onChange={(e) => setConfirmed(e.target.checked)} /> I confirm these observations</label>
            <div className="palm-actions">
              <button className="primary" disabled={!confirmed || busy} onClick={() => void read()}>Open my palm reading</button>
              <button className="text-button" disabled={busy} onClick={() => { setReview(false); setConfirmed(false); focusQuestion(); }}>Edit observations</button>
            </div>
          </> : <>
            <div className="palm-options" role="group" aria-label={selected?.[1] ?? "Hand"}>
              {(selected?.[2] ?? [["left", "Left hand"], ["right", "Right hand"]]).map(([value, label]) =>
                <button className="text-button" key={value} aria-pressed={(selected ? values[selected[0]] : side) === value}
                  onClick={() => selected ? setValues({ ...values, [selected[0]]: value }) : setSide(value)}>{label}</button>)}
            </div>
            <div className="palm-actions palm-step-actions">
              {step > 0 && <button className="text-button" onClick={() => move(step - 1)}>Back</button>}
              {selected && <button className="text-button" onClick={() => {
                const next = { ...values };
                delete next[selected[0]];
                setValues(next);
                if (step >= ordered.length) openReview(); else move(step + 1);
              }}>Skip this feature</button>}
              <button className="primary" disabled={selected ? !values[selected[0]] : !side} onClick={() => {
                if (step >= ordered.length) openReview(); else move(step + 1);
              }}>Continue</button>
            </div>
            {step > 0 && <div className="palm-actions">
              <button className="text-button" onClick={openReview}>Review observations</button>
              {step < 4 && <button className="text-button" onClick={() => move(4)}>Explore more features</button>}
            </div>}
          </>}
        </div>
      </div>}
      {error && <p role="alert">{error}</p>}
      {busy && <p role="status">{examining ? "Preparing your reading…" : "Preparing your photo…"}</p>}
      {report && (
        <article aria-live="polite" className="palm-report">
          <h3 ref={reportHeading} tabIndex={-1}>
            {report.narrative.title}
          </h3>
          {report.narrative.abstained && (
            <p>
              The details you could confirm are too limited for a reading. You can leave unclear features open.
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
      {report && <>
        <p className="palm-note">A symbolic reading from a historical practice.</p>
        <button className="text-button" onClick={() => {
          setConfirmed(false);
          setReview(false);
          setReport(undefined);
        }}>Return to observations</button>
      </>}
      {examining && <button className="text-button palm-remove" onClick={clear}>{photo ? "Remove photo and start over" : "Start over"}</button>}
    </section>
  );
}
