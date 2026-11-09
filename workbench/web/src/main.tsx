import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Compass,
  FlaskConical,
  Users,
  EyeOff,
  GitCompareArrows,
  ChartNoAxesCombined,
  ArrowUpRight,
  Search,
  Sun,
  Moon,
  Download,
  Play,
  RotateCcw,
  Check,
  ShieldCheck,
} from "lucide-react";
import { Button } from "./components/ui/button";
import { Editor, Tree, CLIEditor, human } from "./editor";
import "./style.css";
type Any = any;
function scopeText(value: Any): string {
  if (value === null) return "";
  if (typeof value !== "object") return String(value);
  if (Array.isArray(value)) return value.map(scopeText).join("; ");
  return Object.entries(value)
    .map(([k, v]) => `${human(k)}: ${scopeText(v)}`)
    .join(" · ");
}
async function api(path: string, body?: Any, method?: string, key?: string) {
  const r = await fetch("/api" + path, {
    method: method || (body ? "POST" : "GET"),
    headers:
      body || method
        ? {
            "Content-Type": "application/json",
            "Idempotency-Key": key || crypto.randomUUID(),
          }
        : undefined,
    body: body
      ? typeof body === "string"
        ? body
        : JSON.stringify(body)
      : undefined,
  });
  const data = await r.json();
  if (!r.ok) throw Error(data.error || JSON.stringify(data));
  return data;
}
function download(value: Any, name: string, type = "application/json") {
  const a = document.createElement("a");
  const url = URL.createObjectURL(
    new Blob(
      [typeof value === "string" ? value : JSON.stringify(value, null, 2)],
      { type },
    ),
  );
  a.href = url;
  a.download = name;
  a.click();
  URL.revokeObjectURL(url);
}
function Field({
  label,
  value,
  onChange,
  type = "text",
  required = false,
}: {
  label: string;
  value: Any;
  onChange: (v: Any) => void;
  type?: string;
  required?: boolean;
}) {
  return (
    <label className="field">
      <span>{label}</span>
      {type === "textarea" ? (
        <textarea
          required={required}
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
      ) : (
        <input
          required={required}
          aria-label={label}
          type={type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
        />
      )}
    </label>
  );
}
function Notice({ children }: { children: React.ReactNode }) {
  return (
    <div className="notice">
      <ShieldCheck size={17} />
      <span>{children}</span>
    </div>
  );
}
function MarkdownResult({ id, value }: { id?: string; value: Any }) {
  const [text, setText] = useState("Loading Markdown…");
  useEffect(() => {
    let active = true;
    if (id)
      fetch("/api/records/" + id + "/markdown")
        .then((r) => r.text())
        .then((t) => {
          if (active) setText(t);
        })
        .catch((e) => {
          if (active) setText(String(e));
        });
    else
      setText(
        "# Future validation\n\n```json\n" +
          JSON.stringify(value, null, 2) +
          "\n```",
      );
    return () => {
      active = false;
    };
  }, [id, value]);
  return (
    <>
      <Button
        variant="outline"
        onClick={() => download(text, "future-result.md", "text/markdown")}
      >
        Export Markdown
      </Button>
      <pre className="code">{text}</pre>
    </>
  );
}
function App() {
  const [registry, setRegistry] = useState<Any>(),
    [page, setPage] = useState("Explore"),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false),
    [dark, setDark] = useState(localStorage.getItem("future-theme") === "dark");
  const [query, setQuery] = useState(""),
    [phase, setPhase] = useState(0),
    [category, setCategory] = useState(""),
    [detail, setDetail] = useState<Any>(),
    [req, setReq] = useState<Any>(),
    [raw, setRaw] = useState(""),
    [advanced, setAdvanced] = useState(false),
    [result, setResult] = useState<Any>(),
    [tab, setTab] = useState("Structured"),
    [origin, setOrigin] = useState("sample");
  const [records, setRecords] = useState<Any[]>([]),
    [dashboard, setDashboard] = useState<Any>(),
    [caseId, setCaseId] = useState(""),
    [mode, setMode] = useState("explore"),
    [hidden, setHidden] = useState(""),
    [notes, setNotes] = useState(""),
    [interpretation, setInterpretation] = useState(""),
    [assessor, setAssessor] = useState(""),
    [agreement, setAgreement] = useState("3"),
    [alternatives, setAlternatives] = useState("");
  const [nickname, setNickname] = useState(""),
    [scopes, setScopes] = useState<string[]>(["explore"]),
    [consented, setConsented] = useState(false),
    [retain, setRetain] = useState(false),
    [allowed, setAllowed] = useState(""),
    [participant, setParticipant] = useState(""),
    [title, setTitle] = useState(""),
    [studyLabel, setStudyLabel] = useState("");
  const [selected, setSelected] = useState<string[]>([]),
    [comparison, setComparison] = useState<Any>(),
    [deletion, setDeletion] = useState<Any>();
  const [filters, setFilters] = useState({
    technique: "",
    participant: "",
    study: "",
    since: "",
    until: "",
  });
  const [forecast, setForecast] = useState<Any>({
    question: "",
    probability: "1/2",
    cutoff: "",
    window_end: "",
    positive_rule: "",
    negative_rule: "",
    source_ref: "",
    evidence: "",
    reason: "",
    clarity_confirmed: false,
  });
  const [outcome, setOutcome] = useState<Any>({
      target_id: "q1",
      status: "resolved",
      value: "1",
      known_at: "",
      reason: "",
      evidence: "",
      assessor: "",
    }),
    [activeStudy, setActiveStudy] = useState(""),
    [advancedPlan, setAdvancedPlan] = useState("");
  async function task(fn: () => Promise<void>) {
    setBusy(true);
    setError("");
    try {
      await fn();
    } catch (e) {
      setError(String((e as Error).message));
    } finally {
      setBusy(false);
    }
  }
  async function refresh() {
    setRecords(await api("/records"));
    const q = new URLSearchParams(
      Object.fromEntries(Object.entries(filters).filter(([, v]) => v)),
    );
    setDashboard(await api("/dashboard?" + q));
  }
  useEffect(() => {
    task(async () => {
      setRegistry(await api("/registry"));
      await refresh();
    });
  }, []);
  useEffect(() => {
    document.documentElement.classList.toggle("dark", dark);
    localStorage.setItem("future-theme", dark ? "dark" : "light");
  }, [dark]);
  function navigate(p: string) {
    setPage(p);
    setError("");
    task(refresh);
  }
  async function open(id: number) {
    await task(async () => {
      const d = await api("/techniques/" + id);
      setDetail(d);
      setReq(d.sample);
      setRaw(JSON.stringify(d.sample, null, 2));
      setResult(null);
      setOrigin("sample");
      setAdvanced(false);
      setPage("Studio");
    });
  }
  function change(v: Any) {
    setReq(v);
    setRaw(JSON.stringify(v, null, 2));
    setOrigin("manual");
  }
  async function execute(validate = false) {
    await task(async () => {
      const r = advanced ? JSON.parse(raw) : req;
      if (validate) {
        setResult({ validation: await api("/validate", r) });
        return;
      }
      const v = await api("/sessions", {
        request: r,
        origin,
        case_id: caseId || null,
        mode,
        hidden_answer: hidden || null,
        alternatives: alternatives.split("\n").filter(Boolean),
        notes,
      });
      setHidden("");
      setResult(v);
      await refresh();
    });
  }
  const participants = records.filter((v) => v.kind === "participant"),
    cases = records.filter((v) => v.kind === "case"),
    sessions = records.filter((v) => v.kind === "session"),
    studies = records.filter((v) => v.kind === "study");
  const menu = [
    ["Explore", Compass],
    ["Studio", FlaskConical],
    ["Cases", Users],
    ["Blind & forecast", EyeOff],
    ["Compare", GitCompareArrows],
    ["Research", ChartNoAxesCombined],
  ] as const;
  function caseSelect() {
    return (
      <label className="field">
        <span>Case / permitted use</span>
        <select
          aria-label="Case"
          value={caseId}
          onChange={(e) => setCaseId(e.target.value)}
        >
          <option value="">Unlinked exploration / researcher forecast</option>
          {cases.map((c) => (
            <option value={c.id} key={c.id}>
              {c.title}
            </option>
          ))}
        </select>
      </label>
    );
  }
  function exportButtons() {
    return (
      <div className="actions">
        <Button
          variant="outline"
          onClick={() =>
            task(async () =>
              download(
                await (await fetch("/api/export")).text(),
                "future-workbench.json",
              ),
            )
          }
        >
          <Download size={15} />
          JSON export
        </Button>
        {["csv", "markdown"].map((f) => (
          <Button key={f} variant="ghost" asChild>
            <a
              href={"/api/export?format=" + f}
              download={"future-records." + (f === "csv" ? "csv" : "md")}
            >
              {f.toUpperCase()}
            </a>
          </Button>
        ))}
        <label className="button outline">
          Import JSON
          <input
            className="sr-only"
            type="file"
            accept="application/json,.json"
            aria-label="Import JSON"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file)
                task(async () => {
                  const v = await api("/import", await file.text());
                  await refresh();
                  setComparison(v);
                });
              e.target.value = "";
            }}
          />
        </label>
      </div>
    );
  }
  return (
    <div className="app">
      <aside>
        <a
          className="brand"
          href="#"
          onClick={(e) => {
            e.preventDefault();
            navigate("Explore");
          }}
        >
          <span className="mark">f</span>
          <span>
            future<span className="brand-sub">WORKBENCH / V1</span>
          </span>
        </a>
        <div className="nav-caption">RESEARCH ENVIRONMENT</div>
        <nav>
          {menu.map(([p, Icon]) => (
            <button
              key={p}
              className={page === p ? "active" : ""}
              onClick={() => navigate(p)}
            >
              <Icon size={19} />
              {p}
            </button>
          ))}
        </nav>
        <div className="sidebar-foot">
          <span className="dot" /> Local workspace
          <p>54 engines · frozen Core v1</p>
          <small>Private by default. No cloud connection.</small>
        </div>
      </aside>
      <div className="workspace">
        <header>
          <span>
            Future Lab <span className="muted">/</span> {page}
          </span>
          <div className="actions">
            <span className="badge">
              <span className="dot" /> localhost
            </span>
            <Button
              variant="ghost"
              aria-label="Toggle color theme"
              onClick={() => setDark(!dark)}
            >
              {dark ? <Sun size={18} /> : <Moon size={18} />}
            </Button>
          </div>
        </header>
        <main>
          <div className="page-head">
            <div className="eyebrow">YOUR LOCAL RESEARCH LABORATORY</div>
            <h1>
              {page === "Explore"
                ? "Explore the methods."
                : page === "Studio"
                  ? detail?.capability.name || "Testing studio"
                  : page === "Cases"
                    ? "People, with permission."
                    : page === "Blind & forecast"
                      ? "Commit before you know."
                      : page === "Compare"
                        ? "Inspect the differences."
                        : "Research, in perspective."}
            </h1>
            <p>
              {page === "Explore"
                ? "Choose a technique. Test its inputs. Follow the evidence."
                : page === "Studio"
                  ? "Native calculations, inspectable results and preserved provenance."
                  : page === "Cases"
                    ? "Pseudonymous participants, explicit consent and local case records."
                    : page === "Blind & forecast"
                      ? "Separate exploration, concealed answers and prospective forecasts."
                      : page === "Compare"
                        ? "Compare outputs descriptively. Score only compatible Lab studies."
                        : "Actual local records, with samples and scoring eligibility kept visible."}
            </p>
          </div>
          {error && (
            <div role="alert" className="error">
              <strong>Request could not complete</strong>
              <p>{error}</p>
              <Button variant="ghost" onClick={() => setError("")}>
                Dismiss
              </Button>
            </div>
          )}
          {busy && (
            <div role="status" className="loading">
              Working locally… native computations may take a moment.
            </div>
          )}
          {page === "Explore" && registry && (
            <>
              <div className="overview">
                <div>
                  <strong>54</strong>
                  <span>Retained techniques</span>
                </div>
                <div>
                  <strong>6</strong>
                  <span>Inventory phases</span>
                </div>
                <div>
                  <strong>3</strong>
                  <span>Lab scoreable engines</span>
                </div>
                <div className="overview-note">
                  A library of bounded methods.
                  <br />
                  <b>Computational verification ≠ empirical validity.</b>
                </div>
              </div>
              <div className="toolbar">
                <label className="search">
                  <Search size={18} />
                  <input
                    aria-label="Search techniques"
                    placeholder="Search techniques, scope or required data…"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                  />
                </label>
                <select
                  aria-label="Capability category"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                >
                  <option value="">All capability types</option>
                  {[
                    ...new Set<string>(
                      registry.entries.map((v: Any) => v.capability_type),
                    ),
                  ].map((v) => (
                    <option key={v}>{v}</option>
                  ))}
                </select>
              </div>
              <div className="phase-tabs">
                <button
                  className={!phase ? "selected" : ""}
                  onClick={() => setPhase(0)}
                >
                  All methods
                </button>
                {registry.phases.map((s: string, i: number) => (
                  <button
                    key={s}
                    className={phase === i + 1 ? "selected" : ""}
                    onClick={() => setPhase(i + 1)}
                  >
                    {i + 1} · {s.split(" & ")[0]}
                  </button>
                ))}
              </div>
              <div className="section-label">
                <span>METHOD DIRECTORY</span>
                <span>Original inventory IDs preserved</span>
              </div>
              <div className="cards">
                {registry.entries
                  .filter(
                    (v: Any) =>
                      (!phase || v.phase === phase) &&
                      (!category || v.capability_type === category) &&
                      JSON.stringify(v)
                        .toLowerCase()
                        .includes(query.toLowerCase()),
                  )
                  .map((e: Any) => (
                    <button
                      className="engine-card"
                      key={e.technique_id}
                      onClick={() => open(e.technique_id)}
                    >
                      <div className="card-top">
                        <span className="id">
                          {String(e.technique_id).padStart(2, "0")}
                        </span>
                        <ArrowUpRight size={19} />
                      </div>
                      <span className="eyebrow">
                        PHASE {e.phase} / {registry.phases[e.phase - 1]}
                      </span>
                      <h2>{e.name}</h2>
                      <p>{scopeText(e.supported_scope)}</p>
                      <div className="card-foot">
                        <span className="badge">{e.release_status}</span>
                        <small>{human(e.capability_type)}</small>
                      </div>
                    </button>
                  ))}
              </div>
              <Notice>
                Six excluded IDs remain excluded: 25, 27, 41, 42, 47, 48.
                Supported, experimental and unsupported boundaries follow each
                frozen release.
              </Notice>
            </>
          )}
          {page === "Studio" &&
            (!detail ? (
              <div className="empty">
                <FlaskConical />
                <h2>Choose a technique to begin</h2>
                <Button onClick={() => navigate("Explore")}>
                  Browse all 54 methods
                </Button>
              </div>
            ) : (
              <>
                <div className="studio-bar">
                  <span className="badge">
                    #{detail.capability.technique_id} ·{" "}
                    {detail.capability.release_status}
                  </span>
                  <span className="badge">
                    {detail.capability.capability_type}
                  </span>
                  <span className="badge">
                    {origin === "sample"
                      ? "Verified sample input"
                      : "Edited / user input"}
                  </span>
                  <Button variant="ghost" onClick={() => navigate("Explore")}>
                    Change technique
                  </Button>
                </div>
                <div className="studio-layout">
                  <section className="panel">
                    <div className="panel-head">
                      <h2>Configure a run</h2>
                      <span className="step">01 / INPUT</span>
                    </div>
                    <label className="field">
                      <span>Native operation</span>
                      <select
                        aria-label="Native operation"
                        value={req.operation}
                        onChange={(e) => {
                          const op = detail.capability.operations.find(
                            (o: Any) => o.command === e.target.value,
                          );
                          change({
                            technique_id: req.technique_id,
                            operation: op.command,
                            ...(op.adapter === "native_request"
                              ? { input: structuredClone(detail.sample.input) }
                              : {
                                  arguments:
                                    op.command === detail.sample.operation
                                      ? detail.sample.arguments
                                      : op.cli_arguments
                                          .filter(
                                            (f: Any) =>
                                              !f.names[0].startsWith("--"),
                                          )
                                          .map(() => ""),
                                }),
                          });
                        }}
                      >
                        {detail.capability.operations.map((o: Any) => (
                          <option key={o.command}>{o.command}</option>
                        ))}
                      </select>
                    </label>
                    <div className="actions">
                      <Button
                        variant="outline"
                        onClick={() => {
                          setReq(structuredClone(detail.sample));
                          setRaw(JSON.stringify(detail.sample, null, 2));
                          setOrigin("sample");
                          setResult(null);
                        }}
                      >
                        <RotateCcw size={14} />
                        Load verified sample
                      </Button>
                      <label className="check">
                        <input
                          type="checkbox"
                          checked={advanced}
                          onChange={(e) => setAdvanced(e.target.checked)}
                        />
                        Advanced JSON
                      </label>
                    </div>
                    <p className="hint">
                      Fields start from a verified native example; they are not
                      a complete schema. Pinned profile/hash fields stay
                      visible. Native validation checks dependent commitments.
                    </p>
                    {advanced ? (
                      <textarea
                        className="code raw"
                        aria-label="Advanced request JSON"
                        value={raw}
                        onChange={(e) => {
                          setRaw(e.target.value);
                          setOrigin("manual");
                        }}
                      />
                    ) : req.arguments ? (
                      <CLIEditor
                        op={detail.capability.operations.find(
                          (o: Any) => o.command === req.operation,
                        )}
                        args={req.arguments}
                        onChange={(a) => change({ ...req, arguments: a })}
                      />
                    ) : (
                      <Editor
                        key={req.technique_id}
                        value={req.input}
                        onChange={(v) => change({ ...req, input: v })}
                      />
                    )}
                    <details>
                      <summary>Session context & mode</summary>
                      {caseSelect()}
                      <label className="field">
                        <span>Testing mode</span>
                        <select
                          value={mode}
                          onChange={(e) => setMode(e.target.value)}
                        >
                          <option value="explore">Explore</option>
                          <option value="blind">Blind case testing</option>
                        </select>
                      </label>
                      <Field
                        label="Session notes"
                        type="textarea"
                        value={notes}
                        onChange={setNotes}
                      />
                      {mode === "blind" && (
                        <>
                          <Notice>
                            Assessor setup: enter a separate answer, then hand
                            the tester this screen after the run. The native
                            input must itself omit concealed answers. A local
                            database owner can inspect stored secrets.
                          </Notice>
                          <Field
                            label="Hidden answer (assessor setup)"
                            type="textarea"
                            value={hidden}
                            onChange={setHidden}
                          />
                          <Field
                            label="Optional comparison alternatives (one per line)"
                            type="textarea"
                            value={alternatives}
                            onChange={setAlternatives}
                          />
                        </>
                      )}
                    </details>
                    <div className="run-bar">
                      <Button disabled={busy} onClick={() => execute()}>
                        <Play size={15} />
                        Run technique
                      </Button>
                      <Button
                        variant="outline"
                        disabled={busy}
                        onClick={() => execute(true)}
                      >
                        Validate input
                      </Button>
                      <Button
                        variant="ghost"
                        onClick={() => {
                          setReq(structuredClone(detail.sample));
                          setRaw(JSON.stringify(detail.sample, null, 2));
                          setResult(null);
                          setHidden("");
                          setOrigin("sample");
                        }}
                      >
                        Reset
                      </Button>
                    </div>
                  </section>
                  <section className="panel results">
                    <div className="panel-head">
                      <h2>Inspect result</h2>
                      <span className="step">02 / OUTPUT</span>
                    </div>
                    {!result ? (
                      <div className="empty">
                        <Compass size={32} />
                        <h3>Ready when you are</h3>
                        <p>
                          Run the native engine to inspect structured output,
                          errors and provenance.
                        </p>
                      </div>
                    ) : (
                      <>
                        <div className="tabs">
                          {["Structured", "Markdown", "JSON", "Provenance"].map(
                            (t) => (
                              <button
                                className={tab === t ? "selected" : ""}
                                key={t}
                                onClick={() => setTab(t)}
                              >
                                {t}
                              </button>
                            ),
                          )}
                        </div>
                        <div className="actions">
                          <Button
                            variant="ghost"
                            onClick={() =>
                              task(async () =>
                                download(
                                  result.id
                                    ? await (
                                        await fetch("/api/records/" + result.id)
                                      ).text()
                                    : result,
                                  "future-run.json",
                                ),
                              )
                            }
                          >
                            <Download size={14} />
                            Export run
                          </Button>
                          <Button
                            variant="ghost"
                            onClick={() =>
                              task(async () => {
                                await navigator.clipboard.writeText(
                                  result.id
                                    ? await (
                                        await fetch("/api/records/" + result.id)
                                      ).text()
                                    : JSON.stringify(result, null, 2),
                                );
                              })
                            }
                          >
                            Copy JSON
                          </Button>
                          {result.id && !result.parent && (
                            <Button
                              variant="destructive"
                              onClick={() =>
                                task(async () => {
                                  setDeletion({
                                    ...(await api(
                                      `/records/${result.id}/deletion`,
                                    )),
                                    id: result.id,
                                  });
                                  setPage("Cases");
                                })
                              }
                            >
                              Delete unlinked run
                            </Button>
                          )}
                          <span className="badge">
                            {result.result?.execution_status ||
                              result.validation?.status}
                          </span>
                        </div>
                        {result.result?.native_error && (
                          <div className="error" role="alert">
                            {result.result.native_error.type}:{" "}
                            {result.result.native_error.message}
                            <pre>{result.result.native_stderr}</pre>
                          </div>
                        )}
                        {tab === "Structured" ? (
                          <Tree
                            value={
                              result.result?.native_output ??
                              result.validation ??
                              result
                            }
                            label="Native result"
                          />
                        ) : tab === "Provenance" ? (
                          <Tree
                            value={{
                              request: result.request,
                              provenance: result.result?.provenance,
                              request_sha256: result.result?.request_sha256,
                              output_sha256:
                                result.result?.native_output_sha256,
                              limits: result.result?.limits,
                            }}
                          />
                        ) : tab === "Markdown" ? (
                          <MarkdownResult
                            id={result.id}
                            value={result.validation}
                          />
                        ) : (
                          <pre className="code">
                            {JSON.stringify(result, null, 2)}
                          </pre>
                        )}
                        {result.mode === "blind" && (
                          <div className="blind-box">
                            {result.alternatives?.length > 0 && (
                              <Tree
                                value={result.alternatives}
                                label="Blinded alternatives (shuffled labels)"
                              />
                            )}
                            <h3>
                              {result.locked
                                ? "Interpretation locked"
                                : "Record interpretation before reveal"}
                            </h3>
                            {result.locked ? (
                              <Tree value={result.locked} />
                            ) : (
                              <>
                                <Field
                                  label="Immutable interpretation"
                                  type="textarea"
                                  value={interpretation}
                                  onChange={setInterpretation}
                                />
                                <Button
                                  disabled={busy || !interpretation}
                                  onClick={() =>
                                    task(async () => {
                                      setResult(
                                        await api(
                                          `/sessions/${result.id}/lock`,
                                          { interpretation },
                                        ),
                                      );
                                      await refresh();
                                    })
                                  }
                                >
                                  Lock interpretation
                                </Button>
                              </>
                            )}
                            {result.locked && !result.revealed && (
                              <Button
                                onClick={() =>
                                  task(async () => {
                                    setResult(
                                      await api(
                                        `/sessions/${result.id}/reveal`,
                                        {},
                                      ),
                                    );
                                    await refresh();
                                  })
                                }
                              >
                                Reveal answer
                              </Button>
                            )}
                            {result.revealed && (
                              <>
                                <Notice>Answer: {result.answer}</Notice>
                                <Field
                                  label="Independent assessor"
                                  value={assessor}
                                  onChange={setAssessor}
                                />
                                <Field
                                  label="Agreement (1–5, descriptive only)"
                                  type="number"
                                  value={agreement}
                                  onChange={setAgreement}
                                />
                                <Field
                                  label="Assessor notes"
                                  value={notes}
                                  onChange={setNotes}
                                />
                                <Button
                                  onClick={() =>
                                    task(async () => {
                                      setResult(
                                        await api(
                                          `/sessions/${result.id}/feedback`,
                                          {
                                            assessor,
                                            agreement: Number(agreement),
                                            notes,
                                          },
                                        ),
                                      );
                                      await refresh();
                                    })
                                  }
                                >
                                  Record feedback
                                </Button>
                              </>
                            )}
                          </div>
                        )}
                      </>
                    )}
                    <details className="scope">
                      <summary>Capability, sources & limits</summary>
                      <Tree value={detail.capability} />
                      <Tree
                        value={detail.source_catalogs}
                        label="Pinned source catalogs / rights & provenance"
                      />
                      <Tree
                        value={detail.profiles}
                        label="Pinned profile definitions"
                      />
                      <Tree
                        value={detail.release}
                        label="Frozen release / configuration matrix"
                      />
                    </details>
                  </section>
                </div>
              </>
            ))}
          {page === "Cases" && (
            <>
              <Notice>
                Collect only the data needed for the technique. No photograph
                uploads or new medical/image inference. Consent is a local
                declaration, not an external authorization system.
              </Notice>
              <div className="two-col">
                <form
                  className="panel"
                  onSubmit={(e) => {
                    e.preventDefault();
                    task(async () => {
                      await api("/participants", {
                        consent: consented,
                        nickname,
                        scopes,
                        techniques: allowed
                          ? allowed.split(",").map(Number)
                          : registry.entries.map((v: Any) => v.technique_id),
                        retain_frozen: retain,
                      });
                      await refresh();
                      setNickname("");
                      setConsented(false);
                    });
                  }}
                >
                  <h2>New participant</h2>
                  <Field
                    label="Nickname (optional)"
                    value={nickname}
                    onChange={setNickname}
                  />
                  <Field
                    label="Permitted technique IDs (comma separated; blank = all 54)"
                    value={allowed}
                    onChange={setAllowed}
                  />
                  <div className="checks">
                    {["explore", "blind", "prospective"].map((s) => (
                      <label className="check" key={s}>
                        <input
                          type="checkbox"
                          checked={scopes.includes(s)}
                          onChange={(e) =>
                            setScopes(
                              e.target.checked
                                ? [...scopes, s]
                                : scopes.filter((v) => v !== s),
                            )
                          }
                        />
                        {human(s)}
                      </label>
                    ))}
                  </div>
                  <label className="check">
                    <input
                      type="checkbox"
                      checked={consented}
                      onChange={(e) => setConsented(e.target.checked)}
                    />
                    Participant explicitly consents to these uses
                  </label>
                  <label className="check">
                    <input
                      type="checkbox"
                      checked={retain}
                      onChange={(e) => setRetain(e.target.checked)}
                    />
                    Separate consent: retain already-frozen research after
                    deleting active cases
                  </label>
                  <Button disabled={busy || !consented}>
                    Create participant
                  </Button>
                </form>
                <form
                  className="panel"
                  onSubmit={(e) => {
                    e.preventDefault();
                    task(async () => {
                      await api("/cases", {
                        participant_id: participant,
                        title,
                        study: studyLabel,
                        notes,
                      });
                      setTitle("");
                      await refresh();
                    });
                  }}
                >
                  <h2>New case</h2>
                  <label className="field">
                    <span>Participant</span>
                    <select
                      aria-label="Participant"
                      required
                      value={participant}
                      onChange={(e) => setParticipant(e.target.value)}
                    >
                      <option value="">Choose participant</option>
                      {participants.map((p) => (
                        <option key={p.id} value={p.id}>
                          {p.pseudonym} {p.nickname}
                        </option>
                      ))}
                    </select>
                  </label>
                  <Field
                    label="Case title"
                    value={title}
                    onChange={setTitle}
                    required
                  />
                  <Field
                    label="Study label (optional)"
                    value={studyLabel}
                    onChange={setStudyLabel}
                  />
                  <Field
                    label="Case notes"
                    type="textarea"
                    value={notes}
                    onChange={setNotes}
                  />
                  <Button disabled={busy}>Create case</Button>
                </form>
              </div>
              <div className="panel">
                <h2>Local records</h2>
                {!participants.length && (
                  <p className="empty">
                    No participants yet. Consent comes first.
                  </p>
                )}
                {participants.map((p) => (
                  <div className="record" key={p.id}>
                    <div>
                      <h3>
                        {p.pseudonym} {p.nickname}
                      </h3>
                      <p>
                        {p.scopes.join(" · ")} / {p.techniques.length} permitted
                        techniques
                      </p>
                      <small>
                        {p.retain_frozen
                          ? "Frozen retention separately consented"
                          : "No frozen retention consent"}
                      </small>
                    </div>
                    <div className="actions">
                      <Button
                        variant="outline"
                        onClick={() =>
                          task(async () =>
                            download(
                              await (
                                await fetch("/api/export?participant=" + p.id)
                              ).text(),
                              "participant.json",
                            ),
                          )
                        }
                      >
                        Export
                      </Button>
                      <Button
                        variant="destructive"
                        onClick={() =>
                          task(async () =>
                            setDeletion({
                              ...(await api(`/records/${p.id}/deletion`)),
                              id: p.id,
                            }),
                          )
                        }
                      >
                        Delete participant
                      </Button>
                    </div>
                  </div>
                ))}
                {cases.map((c) => (
                  <div className="record" key={c.id}>
                    <div>
                      <h3>{c.title}</h3>
                      <p>
                        {c.study} ·{" "}
                        {sessions.filter((s) => s.parent === c.id).length}{" "}
                        sessions
                      </p>
                      <p>{c.notes}</p>
                    </div>
                    <div className="actions">
                      <Button
                        variant="outline"
                        onClick={() => {
                          setCaseId(c.id);
                          navigate("Explore");
                        }}
                      >
                        Run a technique
                      </Button>
                      <Button
                        variant="destructive"
                        onClick={() =>
                          task(async () =>
                            setDeletion({
                              ...(await api(`/records/${c.id}/deletion`)),
                              id: c.id,
                            }),
                          )
                        }
                      >
                        Delete case
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
              <details className="panel">
                <summary>
                  Unlinked local runs & forecasts (
                  {[...sessions, ...studies].filter((v) => !v.parent).length})
                </summary>
                {[...sessions, ...studies]
                  .filter((v) => !v.parent)
                  .map((v) => (
                    <div className="record" key={v.id}>
                      <div>
                        <h3>
                          {v.kind === "study"
                            ? v.title
                            : `#${v.request.technique_id} ${v.request.operation}`}
                        </h3>
                        <small>
                          {v.created_at} · {v.origin || v.report.mode}
                        </small>
                      </div>
                      <Button
                        variant="destructive"
                        onClick={() =>
                          task(async () =>
                            setDeletion({
                              ...(await api(`/records/${v.id}/deletion`)),
                              id: v.id,
                            }),
                          )
                        }
                      >
                        Delete unlinked record
                      </Button>
                    </div>
                  ))}
              </details>
              {deletion && (
                <div
                  className="panel deletion"
                  role="dialog"
                  aria-label="Confirm deletion"
                >
                  <h2>Delete {deletion.records} local records?</h2>
                  <p>{deletion.notice}</p>
                  <p>
                    Frozen retention:{" "}
                    {deletion.separately_consented_frozen_retention
                      ? "separately consented, frozen copies retained"
                      : "not consented, all case data removed"}
                  </p>
                  <Button
                    variant="destructive"
                    onClick={() =>
                      task(async () => {
                        await api(
                          `/records/${deletion.id}`,
                          undefined,
                          "DELETE",
                        );
                        setDeletion(null);
                        setCaseId("");
                        setResult(null);
                        setActiveStudy("");
                        setHidden("");
                        setInterpretation("");
                        setNotes("");
                        setAlternatives("");
                        setAssessor("");
                        setSelected([]);
                        setComparison(undefined);
                        if (detail) {
                          setReq(structuredClone(detail.sample));
                          setRaw(JSON.stringify(detail.sample, null, 2));
                          setOrigin("sample");
                        }
                        await refresh();
                      })
                    }
                  >
                    Confirm local deletion
                  </Button>
                  <Button variant="ghost" onClick={() => setDeletion(null)}>
                    Cancel
                  </Button>
                </div>
              )}
              {exportButtons()}
            </>
          )}
          {page === "Blind & forecast" && (
            <>
              <Notice>
                Forecasts use the current server clock. Local timestamps and Git
                commits are not independently authenticated commitments. Only
                #49, #51 and #57 are admitted to quantitative Future Lab
                evaluation.
              </Notice>
              <div className="two-col">
                <section className="panel">
                  <h2>Blind sessions</h2>
                  <p>
                    Start in the Testing Studio, select a consented case and
                    Blind mode. Inputs freeze at execution. Lock the
                    interpretation before revealing the separate answer.
                  </p>
                  <Button variant="outline" onClick={() => navigate("Explore")}>
                    Choose a technique
                  </Button>
                  {sessions
                    .filter((s) => s.mode === "blind")
                    .map((s) => (
                      <div className="record" key={s.id}>
                        <div>
                          <b>
                            #{s.request.technique_id} ·{" "}
                            {s.locked ? "Locked" : "Awaiting interpretation"}
                          </b>
                          <small>
                            {s.created_at} ·{" "}
                            {s.revealed ? "Revealed" : "Answer concealed"}
                          </small>
                        </div>
                        <Button
                          variant="outline"
                          onClick={() =>
                            task(async () => {
                              const d = await api(
                                "/techniques/" + s.request.technique_id,
                              );
                              setDetail(d);
                              setReq(s.request);
                              setRaw(JSON.stringify(s.request, null, 2));
                              setResult(s);
                              setPage("Studio");
                            })
                          }
                        >
                          Open
                        </Button>
                      </div>
                    ))}
                </section>
                <form
                  className="panel"
                  onSubmit={(e) => {
                    e.preventDefault();
                    task(async () => {
                      await api("/studies", {
                        ...forecast,
                        case_id: caseId || null,
                        cutoff: new Date(forecast.cutoff).toISOString(),
                        window_end: new Date(forecast.window_end).toISOString(),
                      });
                      await refresh();
                    });
                  }}
                >
                  <h2>New prospective binary forecast</h2>
                  <p className="hint">
                    #51 Superforecasting · user-supplied, unvalidated · fixed
                    1/2 baseline. No synthetic outcomes are prefilled.
                  </p>
                  {caseSelect()}
                  {[
                    ["question", "Unambiguous future event"],
                    ["probability", "Probability (0–1 or fraction)"],
                    ["cutoff", "Forecast cutoff (local time)"],
                    [
                      "window_end",
                      "Complete observation window end (local time)",
                    ],
                    ["positive_rule", "Positive resolution rule"],
                    ["negative_rule", "Negative resolution rule"],
                    ["source_ref", "Independent resolution source / locator"],
                    ["evidence", "Self-authored protocol / evidence snapshot"],
                    ["reason", "Forecast reasoning"],
                  ].map(([k, label]) => (
                    <Field
                      key={k}
                      label={label}
                      required
                      type={
                        ["cutoff", "window_end"].includes(k)
                          ? "datetime-local"
                          : ["question", "evidence", "reason"].includes(k)
                            ? "textarea"
                            : "text"
                      }
                      value={forecast[k]}
                      onChange={(v) => setForecast({ ...forecast, [k]: v })}
                    />
                  ))}
                  <label className="check">
                    <input
                      type="checkbox"
                      checked={forecast.clarity_confirmed}
                      onChange={(e) =>
                        setForecast({
                          ...forecast,
                          clarity_confirmed: e.target.checked,
                        })
                      }
                    />
                    I confirm binary clarity, complete rules and no known
                    outcome
                  </label>
                  <Button disabled={busy || !forecast.clarity_confirmed}>
                    Lock prospective forecast
                  </Button>
                </form>
              </div>
              <details className="panel">
                <summary>Advanced #49 / #51 / #57 Lab plan</summary>
                <p>
                  Paste a complete native Lab plan. The server stamps
                  creation/selection and forecast issuance now, requires a
                  future cutoff and preserves all native chronology, rights,
                  hashes and admission guards. Existing frozen ledgers can be
                  imported through a Workbench export.
                </p>
                <textarea
                  aria-label="Advanced Lab plan"
                  className="code raw"
                  value={advancedPlan}
                  onChange={(e) => setAdvancedPlan(e.target.value)}
                />
                <Button
                  disabled={busy}
                  onClick={() =>
                    task(async () => {
                      await api("/studies", {
                        plan: JSON.parse(advancedPlan),
                        case_id: caseId || null,
                      });
                      await refresh();
                    })
                  }
                >
                  Validate & lock advanced plan
                </Button>
              </details>
              <section className="panel">
                <h2>Forecast ledger & independent outcomes</h2>
                {!studies.length && (
                  <p className="empty">
                    No prospective forecasts have been committed.
                  </p>
                )}
                {studies.map((s) => (
                  <div className="record" key={s.id}>
                    <div>
                      <h3>{s.title}</h3>
                      <p>
                        {s.report.mode} · #{s.report.technique_id} ·{" "}
                        {s.report.coverage.matched}/{s.report.coverage.planned}{" "}
                        matched{" "}
                        {s.dispositions.length ? "· SCORING SUSPENDED" : ""}
                      </p>
                      <small>Cutoff {s.ledger.plan.cutoff}</small>
                    </div>
                    <Button
                      variant="outline"
                      onClick={() => {
                        setActiveStudy(s.id);
                        setOutcome({
                          ...outcome,
                          target_id: s.ledger.plan.targets[0].id,
                        });
                      }}
                    >
                      Inspect / resolve
                    </Button>
                  </div>
                ))}
                {studies
                  .filter((s) => s.id === activeStudy)
                  .map((s) => (
                    <div key={s.id}>
                      <Tree
                        value={s.ledger}
                        label="Immutable native Lab ledger"
                      />
                      <Tree
                        value={s.report}
                        label="Matched scores, baseline & calibration"
                      />
                      <Tree
                        value={s.dispositions}
                        label="Versioned dispositions"
                      />
                      <form
                        onSubmit={(e) => {
                          e.preventDefault();
                          task(async () => {
                            await api(`/studies/${s.id}/outcome`, {
                              ...outcome,
                              known_at:
                                outcome.status === "resolved"
                                  ? new Date(outcome.known_at).toISOString()
                                  : null,
                            });
                            await refresh();
                          });
                        }}
                      >
                        <h3>Record independent resolution</h3>
                        <label className="field">
                          <span>Target</span>
                          <select
                            aria-label="Outcome target"
                            value={outcome.target_id}
                            onChange={(e) =>
                              setOutcome({
                                ...outcome,
                                target_id: e.target.value,
                              })
                            }
                          >
                            {s.ledger.plan.targets.map((t: Any) => (
                              <option key={t.id}>{t.id}</option>
                            ))}
                          </select>
                        </label>
                        <label className="field">
                          <span>Status</span>
                          <select
                            aria-label="Outcome status"
                            value={outcome.status}
                            onChange={(e) =>
                              setOutcome({ ...outcome, status: e.target.value })
                            }
                          >
                            {[
                              "resolved",
                              "missing",
                              "excluded",
                              "void",
                              "disputed",
                              "correction",
                            ].map((v) => (
                              <option key={v}>{v}</option>
                            ))}
                          </select>
                        </label>
                        {outcome.status === "resolved" && (
                          <>
                            <Field
                              label="Observed value (binary 0/1 or native numeric unit)"
                              value={outcome.value}
                              onChange={(v) =>
                                setOutcome({ ...outcome, value: v })
                              }
                            />
                            <Field
                              label="Outcome known at (local time)"
                              type="datetime-local"
                              required
                              value={outcome.known_at}
                              onChange={(v) =>
                                setOutcome({ ...outcome, known_at: v })
                              }
                            />
                          </>
                        )}
                        {[
                          ["assessor", "Independent assessor"],
                          ["reason", "Resolution reason"],
                          [
                            "evidence",
                            "Self-authored independent outcome evidence snapshot",
                          ],
                        ].map(([k, l]) => (
                          <Field
                            key={k}
                            label={l}
                            required
                            type="textarea"
                            value={outcome[k]}
                            onChange={(v) => setOutcome({ ...outcome, [k]: v })}
                          />
                        ))}
                        <Notice>
                          Void/disputed/correction are versioned, unscored
                          annotations. A committed numeric outcome is immutable.
                          Historical numeric replacement is deferred; annotation
                          does not rewrite or certify a corrected score.
                        </Notice>
                        <Button disabled={busy}>
                          Record outcome / disposition
                        </Button>
                      </form>
                    </div>
                  ))}
              </section>
            </>
          )}
          {page === "Compare" && (
            <>
              <Notice>
                Descriptive comparisons are available for all native runs.
                Quantitative comparisons use only compatible, undisputed Lab
                reports and their matched eligible targets.
              </Notice>
              <section className="panel">
                <h2>Select records</h2>
                {[...sessions, ...studies].map((v) => (
                  <label key={v.id} className="check record">
                    <input
                      type="checkbox"
                      checked={selected.includes(v.id)}
                      onChange={(e) =>
                        setSelected(
                          e.target.checked
                            ? [...selected, v.id]
                            : selected.filter((id) => id !== v.id),
                        )
                      }
                    />
                    {v.kind === "study"
                      ? v.title
                      : `#${v.request.technique_id} ${v.request.operation}`}{" "}
                    · {v.created_at}
                  </label>
                ))}
                {!sessions.length && !studies.length && (
                  <p>No runs yet. Start with a method in Explore.</p>
                )}
                <div className="actions">
                  <Button
                    disabled={selected.length < 2 || busy}
                    onClick={() =>
                      task(async () =>
                        setComparison(
                          await api("/compare", {
                            ids: selected,
                            quantitative: false,
                          }),
                        ),
                      )
                    }
                  >
                    Compare descriptively
                  </Button>
                  <Button
                    disabled={selected.length < 2 || busy}
                    variant="outline"
                    onClick={() =>
                      task(async () =>
                        setComparison(
                          await api("/compare", {
                            ids: selected,
                            quantitative: true,
                          }),
                        ),
                      )
                    }
                  >
                    Eligible matched scores
                  </Button>
                </div>
              </section>
              {comparison &&
                (comparison.records ? (
                  <div className="comparison">
                    {comparison.records.map((v: Any) => (
                      <section className="panel" key={v.id}>
                        <h2>
                          {v.kind === "study" ? v.title : v.request.operation}
                        </h2>
                        <Tree
                          value={v.request ?? v.ledger.plan}
                          label="Inputs & assumptions"
                        />
                        <Tree
                          value={v.result?.native_output ?? v.report}
                          label="Outputs"
                        />
                        <Tree
                          value={v.result?.provenance ?? v.dispositions}
                          label="Provenance / dispositions"
                        />
                      </section>
                    ))}
                  </div>
                ) : (
                  <section className="panel">
                    <Tree value={comparison} />
                  </section>
                ))}
            </>
          )}
          {page === "Research" && (
            <>
              <div className="panel">
                <div className="filters">
                  {[
                    ["technique", "Technique ID"],
                    ["participant", "Participant ID"],
                    ["study", "Study label"],
                    ["since", "Since (ISO)"],
                    ["until", "Until (ISO)"],
                  ].map(([k, label]) => (
                    <Field
                      key={k}
                      label={label}
                      value={filters[k as keyof typeof filters]}
                      onChange={(v) => setFilters({ ...filters, [k]: v })}
                    />
                  ))}
                  <Button onClick={() => task(refresh)}>Apply filters</Button>
                </div>
              </div>
              {dashboard && (
                <>
                  <div className="metrics">
                    {[
                      "cases",
                      "sessions",
                      "sample_sessions",
                      "submitted_interpretations",
                      "submitted_forecasts",
                      "pending",
                      "resolved",
                      "eligible_scored",
                      "missing",
                      "abstentions",
                      "rejected",
                    ].map((k) => (
                      <div className="metric" key={k}>
                        <strong>{dashboard[k]}</strong>
                        <span>{human(k)}</span>
                      </div>
                    ))}
                  </div>
                  <Notice>{dashboard.notice}</Notice>
                  <section className="panel">
                    <h2>Evidence & coverage</h2>
                    <Tree
                      value={dashboard.sessions_by_technique}
                      label="Sessions by technique"
                    />
                    {!dashboard.reports.length && (
                      <div className="empty">
                        No eligible forecast studies yet. No accuracy estimate
                        is available.
                      </div>
                    )}
                    {dashboard.reports.map((v: Any) => (
                      <div key={v.record_id}>
                        <h3>{v.report.target_definition}</h3>
                        {v.scoring_blocked && (
                          <Notice>
                            Scoring suspended by versioned disposition
                          </Notice>
                        )}
                        <Tree
                          value={v.report}
                          label="Native Lab report: matched baseline & calibration"
                        />
                      </div>
                    ))}
                  </section>
                </>
              )}
              {exportButtons()}
              <Notice>
                Portable exports omit unrevealed blind answers. Import restores
                verified records, not independent external authenticity.
                Downloaded exports and backups need separate deletion.
              </Notice>
            </>
          )}
          <footer>
            <span>FUTURE WORKBENCH / LOCAL FIRST</span>
            <span>Frozen engines. Explicit limits. Reproducible records.</span>
          </footer>
        </main>
      </div>
    </div>
  );
}
createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
