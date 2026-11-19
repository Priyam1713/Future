import { useState, useRef, useEffect, useLayoutEffect } from "react";
import { useSound } from "../useSound";
import { api, type Draw, type Envelope, type Commentary } from "../types";
import { EXPERIENCES } from "../experiences/contracts";
import { useCodex } from "../codex/useCodex";
import { chamberId, ROOMS, type ChamberSlug } from "../chambers/contracts";
import { ritualId, RITUAL_ROOMS, type RitualSlug } from "../ritual/contracts";
export type Screen =
  | RitualSlug
  | ChamberSlug
  | "explore"
  | "ritual"
  | "reading"
  | "western"
  | "numerology"
  | "codex"
  | "gallery";
export function useOracle() {
  const codex = useCodex();
  const [explored, setExplored] = useState<number[]>([]);
  function markExplored(id: number) {
    setExplored((previous) =>
      previous.includes(id) ? previous : [...previous, id],
    );
  }
  const [screen, setScreen] = useState<Screen>(() => {
    const wing = ritualId(location.hash.slice(1));
    if (wing) return RITUAL_ROOMS[wing].slug;
    const chamber = chamberId(location.hash.slice(1));
    if (chamber) return ROOMS[chamber].slug;
    return location.hash === "#western"
      ? "western"
      : location.hash === "#my-fate"
        ? "codex"
        : location.hash === "#gallery"
          ? "gallery"
          : "explore";
  });
  const [spread, setSpread] = useState<"one" | "three">("three");
  const [question, setQuestion] = useState(""),
    [reversals, setReversals] = useState(true);
  const [envelope, setEnvelope] = useState<Envelope | null>(null),
    [draw, setDraw] = useState<Draw | null>(null);
  const [revealed, setRevealed] = useState<number[]>([]),
    [busy, setBusy] = useState(false),
    [error, setError] = useState("");
  const [reduced, setReduced] = useState(
      () => matchMedia("(prefers-reduced-motion: reduce)").matches,
    ),
    [paused, setPaused] = useState(false);
  const [consent, setConsent] = useState(false),
    [ai, setAi] = useState<Commentary | null>(null),
    [aiBusy, setAiBusy] = useState(false),
    [aiError, setAiError] = useState("");
  const [gemini, setGemini] = useState(false);
  const dialog = useRef<HTMLDialogElement>(null),
    heading = useRef<HTMLHeadingElement>(null),
    seed = useRef(""),
    inflight = useRef(false),
    controller = useRef<AbortController | null>(null),
    aiController = useRef<AbortController | null>(null);
  const sound = useSound();
  const preferMainFocus = useRef(false);
  function skipToContent() {
    preferMainFocus.current = true;
    document.getElementById("main")?.focus();
  }
  const result = envelope?.result;
  function navigate(next: Screen) {
    preferMainFocus.current = false;
    // Each room keeps its existing CSS entrance. Avoid root screenshot
    // transitions around asynchronous screens and keyboard focus changes.
    history.pushState(null, "", next === "codex" ? "#my-fate" : `#${next}`);
    setScreen(next);
    setError("");
  }

  useEffect(() => {
    const fn = () => {
      preferMainFocus.current = false;
      const name = location.hash.slice(1);
      const wing = ritualId(name);
      if (wing) {
        setScreen(RITUAL_ROOMS[wing].slug);
        return;
      }
      const chamber = chamberId(name);
      if (chamber) {
        setScreen(ROOMS[chamber].slug);
        return;
      }
      setScreen(
        name === "western"
          ? "western"
          : name === "ritual"
            ? "ritual"
            : name === "my-fate"
              ? "codex"
              : name === "gallery"
                ? "gallery"
                : name === "numerology"
                  ? "numerology"
                  : name === "reading" && envelope
                    ? "reading"
                    : "explore",
      );
    };
    window.addEventListener("popstate", fn);
    return () => window.removeEventListener("popstate", fn);
  }, [envelope]);
  useLayoutEffect(() => {
    window.scrollTo({ top: 0, behavior: "instant" });
    if (preferMainFocus.current) {
      document.getElementById("main")?.focus({ preventScroll: true });
    } else heading.current?.focus({ preventScroll: true });
  }, [screen, Boolean(result)]);
  useEffect(() => {
    const media = matchMedia("(prefers-reduced-motion: reduce)");
    const change = () => setReduced(media.matches);
    media.addEventListener("change", change);
    void api<{ gemini_available: boolean }>("/api/health")
      .then((r) => setGemini(r.gemini_available))
      .catch(() => {});
    return () => {
      media.removeEventListener("change", change);
      controller.current?.abort();
      aiController.current?.abort();
    };
  }, []);
  function begin() {
    sound.cue("select");
    if (!envelope) {
      seed.current = "";
      setDraw(null);
    }
    navigate("ritual");
  }
  function fresh() {
    aiController.current?.abort();
    setAiBusy(false);
    setEnvelope(null);
    setDraw(null);
    setAi(null);
    setAiError("");
    setConsent(false);
    setRevealed([]);
    seed.current = "";
    navigate("ritual");
  }
  async function cast() {
    if (inflight.current) return;
    inflight.current = true;
    setBusy(true);
    setError("");
    if (!seed.current) {
      const bytes = crypto.getRandomValues(new Uint8Array(32));
      seed.current = Array.from(bytes, (b) =>
        b.toString(16).padStart(2, "0"),
      ).join("");
    }
    const request: Draw = { spread, question, reversals, seed: seed.current };
    const abort = new AbortController();
    controller.current = abort;
    const timeout = setTimeout(() => abort.abort(), 20000);
    try {
      const response = await api<Envelope>(
        EXPERIENCES[16].endpoint,
        request,
        abort.signal,
      );
      setEnvelope(response);
      setDraw(request);
      setRevealed([]);
      sound.cue("select");
    } catch (e) {
      setError(
        e instanceof Error && e.name !== "AbortError"
          ? e.message
          : "The connection faded. Try again with the same draw; your question is still here.",
      );
    } finally {
      clearTimeout(timeout);
      inflight.current = false;
      setBusy(false);
    }
  }
  function reveal(index: number) {
    if (revealed.includes(index)) return;
    setRevealed((prev) => (prev.includes(index) ? prev : [...prev, index]));
    sound.cue("reveal");
  }
  function readAll() {
    if (result) markExplored(16);
    if (result) setRevealed(result.readings.map((_, i) => i));
    navigate("reading");
  }
  function download() {
    if (!result) return;
    const blob = new Blob(
      [
        JSON.stringify(
          {
            application: "FATE · Block 01",
            artwork:
              "Pamela Colman Smith · Pam-A 1910 Archive Edition; original FATE observatory back; Waite 1922 text profile",
            ...result,
          },
          null,
          2,
        ),
      ],
      { type: "application/json" },
    );
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `fate-tarot-${result.replay.seed.slice(0, 8)}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  async function explain() {
    if (!consent || !draw || !envelope || aiBusy) return;
    setAiBusy(true);
    setAiError("");
    const abort = new AbortController();
    aiController.current = abort;
    const timeout = setTimeout(() => abort.abort(), 130000);
    try {
      setAi(
        await api<Commentary>(
          "/api/explain",
          { draw, receipt: envelope.receipt, cloud_consent: consent },
          abort.signal,
        ),
      );
    } catch (e) {
      if (!abort.signal.aborted)
        setAiError(
          e instanceof Error
            ? e.message
            : "Commentary unavailable. Your native reading is still here.",
        );
      else
        setAiError("Commentary timed out. Your native reading is still here.");
    } finally {
      clearTimeout(timeout);
      setAiBusy(false);
    }
  }
  const allRevealed = !!result && revealed.length === result.readings.length;

  return {
    codex,
    explored,
    markExplored,
    screen,
    spread,
    setSpread,
    question,
    setQuestion,
    reversals,
    setReversals,
    envelope,
    draw,
    revealed,
    busy,
    error,
    reduced,
    paused,
    setPaused,
    consent,
    setConsent,
    ai,
    setAi,
    aiBusy,
    aiError,
    gemini,
    dialog,
    heading,
    sound,
    result,
    navigate,
    begin,
    fresh,
    cast,
    reveal,
    readAll,
    download,
    explain,
    allRevealed,
    skipToContent,
  };
}
export type Oracle = ReturnType<typeof useOracle>;
