import { useEffect, useRef, useState } from "react";
import { api } from "../types";
import { EXPERIENCES } from "../experiences/contracts";
import type {
  NumberCommentary,
  NumberEnvelope,
  NumberInput,
} from "../experiences/contracts";
import type { Oracle } from "../hooks/useOracle";
const today = () => new Date().toLocaleDateString("en-CA");
export function useNumerology(oracle: Oracle) {
  const [input, setInput] = useState<NumberInput>({
    name: "",
    birth: "",
    target: today(),
    basis: "birth",
    y_roles: "",
  });
  const [envelope, setEnvelope] = useState<NumberEnvelope | null>(null);
  const [stage, setStage] = useState<"input" | "ritual" | "reading">("input");
  const [step, setStep] = useState(0),
    [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  const [consent, setConsent] = useState(false),
    [ai, setAi] = useState<NumberCommentary | null>(null),
    [aiBusy, setAiBusy] = useState(false),
    [aiError, setAiError] = useState("");
  const abort = useRef<AbortController | null>(null),
    aiAbort = useRef<AbortController | null>(null),
    inflight = useRef(false);
  const request = useRef<NumberInput | null>(null);
  const heading = useRef<HTMLHeadingElement>(null);
  useEffect(
    () => () => {
      abort.current?.abort();
      aiAbort.current?.abort();
    },
    [],
  );
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "instant" });
    heading.current?.focus({ preventScroll: true });
  }, [stage]);
  function change<K extends keyof NumberInput>(key: K, value: NumberInput[K]) {
    setInput((p) => ({
      ...p,
      [key]: value,
      ...(key === "name" ? { y_roles: "" } : {}),
    }));
  }
  async function calculate() {
    if (inflight.current) return;
    inflight.current = true;
    setBusy(true);
    setError("");
    const controller = new AbortController();
    abort.current = controller;
    const timeout = setTimeout(() => controller.abort(), 20000);
    const q = { ...input, name: input.name.trim() };
    try {
      const response = await api<NumberEnvelope>(
        EXPERIENCES[4].endpoint,
        q,
        controller.signal,
      );
      request.current = q;
      setEnvelope(response);
      setStep(0);
      setStage("ritual");
      oracle.sound.cue("select");
    } catch (e) {
      if (!controller.signal.aborted)
        setError(
          e instanceof Error
            ? e.message
            : "The connection faded. Please retry.",
        );
      else
        setError(
          "The calculation timed out. Your entries are still here; please retry.",
        );
    } finally {
      clearTimeout(timeout);
      inflight.current = false;
      setBusy(false);
    }
  }
  function reveal() {
    if (step < 2) {
      setStep((p) => p + 1);
      oracle.sound.cue("reveal");
    } else finish();
  }
  function finish() {
    setStage("reading");
    oracle.markExplored(4);
    oracle.sound.cue("reveal");
  }
  function fresh() {
    aiAbort.current?.abort();
    setAi(null);
    setAiBusy(false);
    setAiError("");
    setConsent(false);
    setEnvelope(null);
    setStage("input");
  }
  async function explain() {
    if (!consent || !request.current || !envelope || aiBusy) return;
    const controller = new AbortController();
    aiAbort.current = controller;
    setAiBusy(true);
    setAiError("");
    const timeout = setTimeout(() => controller.abort(), 130000);
    try {
      setAi(
        await api<NumberCommentary>(
          "/api/numerology/explain",
          {
            draw: request.current,
            receipt: envelope.receipt,
            cloud_consent: true,
          },
          controller.signal,
        ),
      );
    } catch (e) {
      setAiError(
        e instanceof Error && e.name !== "AbortError"
          ? e.message
          : "Commentary unavailable. Your native reading is still here.",
      );
    } finally {
      clearTimeout(timeout);
      setAiBusy(false);
    }
  }
  function download() {
    if (!envelope) return;
    const url = URL.createObjectURL(
      new Blob([JSON.stringify(envelope.result, null, 2)], {
        type: "application/json",
      }),
    );
    const a = document.createElement("a");
    a.href = url;
    a.download = "fate-numerology.json";
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  return {
    input,
    change,
    envelope,
    result: envelope?.result,
    stage,
    step,
    busy,
    error,
    calculate,
    reveal,
    finish,
    fresh,
    heading,
    consent,
    setConsent,
    ai,
    aiBusy,
    aiError,
    explain,
    download,
  };
}
export type Numerology = ReturnType<typeof useNumerology>;
