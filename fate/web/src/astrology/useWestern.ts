import { useEffect, useRef, useState } from "react";
import type { Oracle } from "../hooks/useOracle";
import { api } from "../types";
import type {
  WesternInput,
  WesternEnvelope,
  WesternCommentary,
} from "./contracts";
export function useWestern(oracle: Oracle) {
  const [envelope, setEnvelope] = useState<WesternEnvelope | null>(null),
    [stage, setStage] = useState<"input" | "ritual" | "reading">("input"),
    [step, setStep] = useState(0),
    [selected, setSelected] = useState("Sun"),
    [busy, setBusy] = useState(false),
    [error, setError] = useState(""),
    [consent, setConsent] = useState(false),
    [ai, setAi] = useState<WesternCommentary | null>(null),
    [aiBusy, setAiBusy] = useState(false),
    [aiError, setAiError] = useState("");
  const controller = useRef<AbortController | null>(null),
    aiController = useRef<AbortController | null>(null),
    inflight = useRef(false),
    q = useRef<WesternInput | null>(null),
    heading = useRef<HTMLHeadingElement>(null);
  useEffect(
    () => () => {
      controller.current?.abort();
      aiController.current?.abort();
    },
    [],
  );
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "instant" });
    heading.current?.focus({ preventScroll: true });
  }, [stage]);
  async function calculate(input: WesternInput) {
    if (inflight.current) return;
    inflight.current = true;
    setBusy(true);
    setError("");
    const c = new AbortController();
    controller.current = c;
    const timer = setTimeout(() => c.abort(), 30000);
    try {
      const r = await api<WesternEnvelope>("/api/western", input, c.signal);
      if (c.signal.aborted) return;
      q.current = input;
      setEnvelope(r);
      setStage("ritual");
      setStep(0);
      setSelected("Sun");
      oracle.sound.cue("select");
    } catch (e) {
      setError(
        c.signal.aborted
          ? "The calculation timed out. Your entries are still here; please retry."
          : e instanceof Error
            ? e.message
            : "The connection faded. Please retry.",
      );
    } finally {
      clearTimeout(timer);
      inflight.current = false;
      setBusy(false);
    }
  }
  function finish() {
    setStage("reading");
    setSelected("Sun");
    oracle.markExplored(1);
    oracle.sound.cue("reveal");
  }
  function reveal() {
    if (step < 2) {
      setStep(step + 1);
      setSelected(step === 0 ? "Moon" : "Ascendant");
      oracle.sound.cue("reveal");
    } else finish();
  }
  async function explain() {
    if (!consent || !q.current || !envelope || aiBusy) return;
    setAiBusy(true);
    setAiError("");
    const c = new AbortController();
    aiController.current = c;
    const timer = setTimeout(() => c.abort(), 130000);
    try {
      setAi(
        await api<WesternCommentary>(
          "/api/western/explain",
          { draw: q.current, receipt: envelope.receipt, cloud_consent: true },
          c.signal,
        ),
      );
    } catch (e) {
      if (!c.signal.aborted)
        setAiError(e instanceof Error ? e.message : "Commentary unavailable.");
      else setAiError("Commentary timed out; your native chart is still here.");
    } finally {
      clearTimeout(timer);
      setAiBusy(false);
    }
  }
  function reset() {
    aiController.current?.abort();
    setAi(null);
    setAiError("");
    setConsent(false);
    setEnvelope(null);
    setStage("input");
  }
  return {
    envelope,
    result: envelope?.result,
    stage,
    step,
    selected,
    setSelected,
    busy,
    error,
    calculate,
    finish,
    reveal,
    reset,
    heading,
    consent,
    setConsent,
    ai,
    aiBusy,
    aiError,
    explain,
  };
}
