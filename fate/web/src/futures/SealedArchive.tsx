import { useEffect, useRef, useState } from "react";
import { api } from "../types";
import type { Oracle } from "../hooks/useOracle";
import { download, Payoff, StudyPage } from "./StudyPage";

type ViewerPacket = {
  visibility: "blind_viewer";
  cue: string;
  commitment: string;
  instructions: string;
};
type JudgePacket = {
  visibility: "blind_judge";
  cue: string;
  instructions: string;
  transcript: { text: string }[];
  candidates: { alias: string; bytes_base64: string }[];
};
type RemoteReport = {
  actual_target_id: string;
  commitment_verified: boolean;
  commitment: string;
  judge_results: { actual_target_rank: number }[];
};
type DreamReport = {
  state: string;
  pair_counts: { total: number; eligible: number };
  pairs: { chronology: string; ratings: Record<string, string> }[];
};
type VaultData = {
  code?: string;
  phase: string;
  packet?: ViewerPacket | JudgePacket;
  commitment?: string;
  cue?: string;
  invite?: string;
  image?: string;
  result?: RemoteReport | DreamReport;
  due?: string;
  feature?: string;
  planHash?: string;
  window?: { start: string; end: string };
  originalLock?: string;
  lockedAt?: string;
  ratingAvailable?: boolean;
};

function useVault() {
  const [data, setData] = useState<VaultData>();
  const [code, setCode] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const c = useRef<AbortController | null>(null);
  useEffect(() => () => c.current?.abort(), []);
  async function send(
    action: string,
    values: Record<string, unknown> = {},
    token = code,
  ) {
    if (c.current) return;
    const next = new AbortController();
    c.current = next;
    setBusy(true);
    setError("");
    try {
      const response = await api<VaultData>(
        "/api/archive-session",
        { action, ...(token ? { code: token } : {}), ...values },
        next.signal,
      );
      if (!next.signal.aborted) {
        if (action === "discard") {
          setData(undefined);
          setCode("");
        } else {
          setData(response);
          if (response.code || token) setCode(response.code || token);
        }
        return response;
      }
    } catch (e) {
      if (!next.signal.aborted) setError((e as Error).message);
    } finally {
      if (!next.signal.aborted) {
        setBusy(false);
        c.current = null;
      }
    }
  }
  return { data, code, busy, error, send };
}

function Seal({ open = false, label }: { open?: boolean; label: string }) {
  return (
    <div className="sealed-display" data-unsealed={open}>
      <svg viewBox="0 0 340 340" role="img" aria-label={label}>
        <circle cx="170" cy="170" r="138" />
        <circle cx="170" cy="170" r="123" className="seal-hash" />
        <circle cx="170" cy="170" r="104" />
        <path d="M170 38L302 170 170 302 38 170Z" />
        <g className="seal-face">
          <path d="M100 170Q170 110 240 170Q170 230 100 170Z" />
          <circle cx="170" cy="170" r="24" />
          <circle cx="170" cy="170" r="10" />
        </g>
      </svg>
    </div>
  );
}
function HoldCode({ label, value }: { label: string; value: string }) {
  return (
    <label className="vault-code">
      {label}
      <input readOnly value={value} onFocus={(e) => e.target.select()} />
    </label>
  );
}
function Resume({
  label,
  send,
  busy,
}: {
  label: string;
  send: (code: string) => void;
  busy: boolean;
}) {
  const [text, setText] = useState("");
  return (
    <details className="lab-depth">
      <summary>{label}</summary>
      <label>
        Session code
        <input
          autoComplete="off"
          value={text}
          maxLength={55}
          onChange={(e) => setText(e.target.value)}
        />
      </label>
      <button
        className="secondary"
        disabled={busy || text.trim().length !== 43}
        onClick={() => send(text.trim())}
      >
        Open session
      </button>
    </details>
  );
}

export function RemoteRoom({ oracle }: { oracle: Oracle }) {
  const { data, code, busy, error, send } = useVault();
  const [consent, setConsent] = useState(false);
  const [text, setText] = useState("");
  const [rank, setRank] = useState<string[]>([]);
  const [judgeRole, setJudgeRole] = useState(false);
  const packet = data?.packet;
  const judge = packet?.visibility === "blind_judge" ? packet : undefined;
  const outcome =
    data?.phase === "revealed" ? (data.result as RemoteReport) : undefined;
  function chooseRank(alias: string) {
    setRank((prev) =>
      prev.includes(alias) ? prev.filter((c) => c !== alias) : [...prev, alias],
    );
  }
  async function rankAndReveal() {
    if (!judge) return;
    const response = await send("judge_rank", {
      ranks: judge.candidates.map(({ alias }) => rank.indexOf(alias) + 1),
    });
    if (response?.phase === "revealed") {
      oracle.markExplored(43);
      oracle.sound.cue("reveal");
    }
  }
  return (
    <div
      className={`future-work future-work-sealed ${judge ? "vault-judging" : ""}`}
    >
      <div className="future-apparatus" aria-label="Sealed target instrument">
        {outcome && data?.image ? (
          <img
            className="target-open"
            src={`data:image/png;base64,${data.image}`}
            alt="The committed geometric target, revealed after both locks"
          />
        ) : judge ? (
          <div
            className="judge-candidates"
            role="group"
            aria-label="Blind candidate ordering"
          >
            {judge.candidates.map(({ alias, bytes_base64 }) => (
              <button
                key={alias}
                type="button"
                aria-pressed={rank.includes(alias)}
                onClick={() => chooseRank(alias)}
                disabled={busy}
                aria-label={`Candidate ${alias}${rank.includes(alias) ? ", rank " + (rank.indexOf(alias) + 1) : ""}`}
              >
                <img
                  src={`data:image/png;base64,${bytes_base64}`}
                  alt="Original geometric candidate plate"
                />
                <span>
                  {alias.toUpperCase()} ·{" "}
                  {rank.includes(alias)
                    ? "Rank " + (rank.indexOf(alias) + 1)
                    : "Unranked"}
                </span>
              </button>
            ))}
          </div>
        ) : (
          <Seal label="Sealed blind target" />
        )}
      </div>
      <div className="future-reading">
        {!data && (
          <>
            <p className="eyebrow">Sealed target</p>
            <h2>Start as the viewer</h2>
            <p>
              The server commits to one of five original plates. Your transcript
              locks before a judge on a separate browser sees the candidates.
            </p>
            <label className="future-check">
              <input
                type="checkbox"
                checked={consent}
                onChange={(e) => setConsent(e.target.checked)}
              />
              I agree to process and share my transcript with the invited judge
            </label>
            <button
              className="primary"
              disabled={busy || !consent}
              onClick={() => void send("remote_start", { consent })}
            >
              Seal a new target
            </button>
            <Resume
              label="I have a judge invitation"
              busy={busy}
              send={async (token) => {
                if (await send("judge_open", {}, token)) setJudgeRole(true);
              }}
            />
            <Resume
              label="Resume my viewer session"
              busy={busy}
              send={(token) => void send("remote_status", {}, token)}
            />
          </>
        )}
        {data?.phase === "viewing" && (
          <>
            <p className="eyebrow">Viewer packet · {packet?.cue ?? data.cue}</p>
            <h2>Record your impressions</h2>
            <label>
              Viewer transcript
              <textarea
                rows={4}
                maxLength={3000}
                value={text}
                onChange={(e) => setText(e.target.value)}
              />
            </label>
            <button
              className="primary"
              disabled={busy || !text.trim()}
              onClick={async () => {
                const response = await send("remote_lock", {
                  text,
                  consent: true,
                });
                if (response) setText("");
              }}
            >
              Lock transcript
            </button>
            <details className="lab-depth">
              <summary>Target commitment</summary>
              <code>
                {packet?.visibility === "blind_viewer"
                  ? packet.commitment
                  : data.commitment}
              </code>
            </details>
          </>
        )}
        {data?.phase === "judging" &&
          (judge ? (
            <>
              <p className="eyebrow">Blind judge packet</p>
              <h2>Choose closest first</h2>
              <blockquote>
                {judge.transcript.map((row) => row.text).join("\n")}
              </blockquote>
              <p>
                Tap all five plates in rank order. Tap a selected plate again to
                remove it.
              </p>
              <button
                className="primary"
                disabled={busy || rank.length !== 5}
                onClick={() => void rankAndReveal()}
              >
                Lock ranks and open the seal
              </button>
            </>
          ) : (
            <>
              <p className="eyebrow">Transcript locked</p>
              <h2>Pass the sealed invite</h2>
              <p>
                Invite a judge using another browser profile or device. They can
                use the judge entry on this room’s entrance.
              </p>
              <HoldCode
                label="Single-use judge code"
                value={data.invite ?? ""}
              />
              <button
                className="primary"
                disabled={busy}
                onClick={async () => {
                  const response = await send("remote_status");
                  if (response?.phase === "revealed") {
                    oracle.markExplored(43);
                    oracle.sound.cue("reveal");
                  }
                }}
              >
                Check for locked ranks
              </button>
            </>
          ))}
        {outcome && (
          <>
            <Payoff
              view={{
                status: "Both packets locked",
                title: `Target ranked ${outcome.judge_results[0]?.actual_target_rank} of 5`,
                lead: "The native engine verified the target commitment and the two pre-reveal locks.",
              }}
            />
            <details className="lab-depth">
              <summary>Protocol and result</summary>
              <p>
                The result describes one trial. Independence of the people and
                repeatability would require separate evidence.
              </p>
              <button
                className="secondary"
                onClick={() => download("fate-revealed-trial", outcome)}
              >
                Export revealed trial
              </button>
            </details>
          </>
        )}
        {data && !judgeRole && code && (
          <details className="lab-depth">
            <summary>Private session controls</summary>
            <HoldCode
              label="Viewer recovery code for this browser"
              value={code}
            />
            <p>Private sessions expire after an hour or a server restart.</p>
            <button
              className="text-button"
              onClick={() => void send("discard")}
              disabled={busy}
            >
              Discard private session
            </button>
          </details>
        )}
        {busy && <p role="status">Checking the archive…</p>}
        {error && <p role="alert">{error}</p>}
      </div>
    </div>
  );
}

const when = (value?: string) =>
  value
    ? new Intl.DateTimeFormat(undefined, {
        dateStyle: "medium",
        timeStyle: "short",
      }).format(new Date(value))
    : "";

export function DreamLedger({ oracle }: { oracle: Oracle }) {
  const { data, code, busy, error, send } = useVault();
  const [demo, setDemo] = useState(false);
  const [feature, setFeature] = useState("");
  const [days, setDays] = useState(1);
  const [text, setText] = useState("");
  const [consent, setConsent] = useState(false);
  const [known, setKnown] = useState(false);
  const [eventAt, setEventAt] = useState("");
  const [rating, setRating] = useState("insufficient_information");
  if (demo)
    return (
      <>
        <button className="text-button" onClick={() => setDemo(false)}>
          ← Open a prospective record
        </button>
        <StudyPage id={44} oracle={oracle} demoOnly />
      </>
    );
  const result = data?.result as DreamReport | undefined;
  const states = ["Plan", "Original lock", "Observed event", "Self-rating"];
  const phase = ["writing", "awaiting", "observed", "reported"].indexOf(
    data?.phase ?? "",
  );
  return (
    <div className="future-work future-work-ledger">
      <div className="future-apparatus" aria-label="Prospective dream timeline">
        <ol className="dream-track">
          {states.map((name, i) => (
            <li key={name} data-reached={i <= phase}>
              <i aria-hidden="true" />
              <b>{name}</b>
              <small>
                {i === 0 && data
                  ? when(data.due) + " · draft deadline"
                  : i === 1 && data?.lockedAt
                    ? when(data.lockedAt)
                    : i < phase
                      ? "Recorded"
                      : ""}
              </small>
            </li>
          ))}
        </ol>
        {data?.window && (
          <p className="instrument-note">
            Comparison window ends {when(data.window.end)}
          </p>
        )}
      </div>
      <div className="future-reading">
        {!data && (
          <>
            <p className="eyebrow">Prospective diary</p>
            <h2>Declare a comparison first</h2>
            <label>
              Feature to record
              <input
                value={feature}
                maxLength={300}
                onChange={(e) => setFeature(e.target.value)}
              />
            </label>
            <label>
              Observation window
              <select
                value={days}
                onChange={(e) => setDays(Number(e.target.value))}
              >
                {[1, 3, 7].map((n) => (
                  <option value={n} key={n}>
                    {n} {n === 1 ? "day" : "days"}
                  </option>
                ))}
              </select>
            </label>
            <label className="future-check">
              <input
                type="checkbox"
                checked={consent}
                onChange={(e) => setConsent(e.target.checked)}
              />
              Process this private diary for the comparison
            </label>
            <button
              className="primary"
              disabled={busy || !consent || !feature.trim()}
              onClick={() =>
                void send("dream_start", { text: feature, days, consent })
              }
            >
              Open recording slot
            </button>
            <button className="text-button" onClick={() => setDemo(true)}>
              Skip to a simulated ledger →
            </button>
            <Resume
              label="Resume a private diary"
              busy={busy}
              send={(token) => void send("dream_status", {}, token)}
            />
          </>
        )}
        {data?.phase === "writing" && (
          <>
            <h2>Lock the original entry</h2>
            <label>
              Dream as remembered
              <textarea
                value={text}
                rows={4}
                maxLength={3000}
                onChange={(e) => setText(e.target.value)}
              />
            </label>
            <label className="future-check">
              <input
                type="checkbox"
                checked={known}
                onChange={(e) => setKnown(e.target.checked)}
              />
              I already know the comparison outcome
            </label>
            <button
              className="primary"
              disabled={busy || !text.trim()}
              onClick={async () => {
                if (await send("dream_lock", { text, known, consent: true })) {
                  setText("");
                  oracle.markExplored(44);
                }
              }}
            >
              Lock dream text
            </button>
          </>
        )}
        {data?.phase === "awaiting" && (
          <>
            <Payoff
              view={{
                status: "Original entry locked",
                title: "Awaiting your observation",
                lead: "Return when an event has actually occurred. The original entry stays fixed.",
              }}
            />
            <details className="lab-depth">
              <summary>Record an event that occurred</summary>
              <label>
                Event time (UTC)
                <input
                  type="datetime-local"
                  step="1"
                  value={eventAt}
                  onChange={(e) => setEventAt(e.target.value)}
                />
              </label>
              <label>
                My self-authored account
                <textarea
                  rows={3}
                  value={text}
                  maxLength={3000}
                  onChange={(e) => setText(e.target.value)}
                />
              </label>
              <button
                className="secondary"
                disabled={busy || !eventAt || !text.trim()}
                onClick={async () => {
                  if (
                    await send("dream_observe", {
                      text,
                      at: eventAt + "Z",
                      consent: true,
                    })
                  )
                    setText("");
                }}
              >
                Record observed event
              </button>
            </details>
          </>
        )}
        {data?.phase === "observed" && (
          <>
            <h2>Compare the two entries</h2>
            {data.ratingAvailable ? (
              <>
                <label>
                  Your description
                  <select
                    value={rating}
                    onChange={(e) => setRating(e.target.value)}
                  >
                    <option value="match">Match</option>
                    <option value="nonmatch">Nonmatch</option>
                    <option value="insufficient_information">
                      Insufficient information
                    </option>
                  </select>
                </label>
                <button
                  className="primary"
                  disabled={busy}
                  onClick={() => void send("dream_finish", { rating })}
                >
                  Finish descriptive review
                </button>
              </>
            ) : (
              <>
                <p>The recording slot closes at {when(data.due)}.</p>
                <button
                  className="secondary"
                  disabled={busy}
                  onClick={() => void send("dream_status")}
                >
                  Check recording slot
                </button>
              </>
            )}
          </>
        )}
        {result && (
          <>
            <Payoff
              view={{
                status: "Descriptive review",
                title: `${result.pair_counts.eligible} eligible ${result.pair_counts.eligible === 1 ? "pair" : "pairs"}`,
                lead: "The native ledger reports the recorded chronology and your self-rating.",
              }}
            />
            <details className="lab-depth">
              <summary>Private report and source</summary>
              <a
                href="https://www.fadedpage.com/showbook.php?pid=20181016"
                target="_blank"
                rel="noreferrer"
              >
                Dunne source edition
              </a>
              <button
                className="secondary"
                onClick={() => download("fate-private-dream-report", result)}
              >
                Export private report
              </button>
            </details>
          </>
        )}
        {data && (
          <details className="lab-depth">
            <summary>Private session controls</summary>
            <HoldCode label="Recovery code for this browser" value={code} />
            {data.originalLock && <code>{data.originalLock}</code>}
            <p>
              The diary is held in server memory for its declared window. A
              server restart ends this session.
            </p>
            <button
              className="text-button"
              disabled={busy}
              onClick={() => void send("discard")}
            >
              Discard diary
            </button>
          </details>
        )}
        {busy && <p role="status">Checking the archive…</p>}
        {error && <p role="alert">{error}</p>}
      </div>
    </div>
  );
}
