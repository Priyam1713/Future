import { useEffect, useRef, useState } from "react";

const preference = "fate.sound.muted.v1";
function prefersMute() {
  try {
    return localStorage.getItem(preference) === "true";
  } catch {
    return false;
  }
}

export function useSound(room: string) {
  const [on, setOn] = useState(false);
  const [music, setMusic] = useState(0.45);
  const [effects, setEffects] = useState(0.22);
  const muted = useRef(prefersMute());
  const enabled = useRef(false);
  const revision = useRef(0);
  const frame = useRef(0);
  const ambient = useRef<HTMLAudioElement | null>(null);
  const cues = useRef<HTMLAudioElement[]>([]);
  function fade(to: number, done?: () => void) {
    cancelAnimationFrame(frame.current);
    const audio = ambient.current;
    if (!audio) return;
    const from = audio.volume;
    const start = performance.now();
    const update = (now: number) => {
      const t = Math.min(1, (now - start) / 420);
      audio.volume = Math.max(0, Math.min(1, from + (to - from) * t));
      if (t === 1) done?.();
      else frame.current = requestAnimationFrame(update);
    };
    frame.current = requestAnimationFrame(update);
  }
  async function start() {
    if (muted.current || enabled.current || document.hidden) return;
    const attempt = ++revision.current;
    if (!ambient.current) {
      ambient.current = new Audio("/art/fate-ambient-v2.wav");
      ambient.current.loop = true;
      ambient.current.volume = 0;
    }
    try {
      await ambient.current.play();
    } catch {
      return;
    }
    if (revision.current !== attempt || muted.current || document.hidden)
      return;
    enabled.current = true;
    setOn(true);
    fade(music);
  }
  useEffect(() => {
    if (enabled.current) fade(music);
    const gesture = (event: MouseEvent) => {
      if (
        event.isTrusted &&
        !(
          event.target instanceof Element &&
          event.target.closest("[data-sound-toggle]")
        )
      )
        void start();
    };
    const visibility = () => {
      if (document.hidden) {
        ++revision.current;
        cancelAnimationFrame(frame.current);
        if (ambient.current) {
          ambient.current.pause();
          ambient.current.volume = 0;
        }
        cues.current.forEach((audio) => audio.pause());
        enabled.current = false;
        setOn(false);
      } else if (ambient.current && !muted.current) void start();
    };
    document.addEventListener("click", gesture);
    document.addEventListener("visibilitychange", visibility);
    return () => {
      document.removeEventListener("click", gesture);
      document.removeEventListener("visibilitychange", visibility);
    };
  }, [music]);
  useEffect(
    () => () => {
      ++revision.current;
      cancelAnimationFrame(frame.current);
      ambient.current?.pause();
      cues.current.forEach((audio) => audio.pause());
    },
    [],
  );
  useEffect(() => {
    if (!enabled.current || !ambient.current) return;
    fade(music * 0.55, () => {
      if (enabled.current) fade(music);
    });
  }, [room]);
  async function toggle() {
    ++revision.current;
    muted.current =
      enabled.current ||
      (!muted.current && Boolean(ambient.current && !ambient.current.paused));
    try {
      if (muted.current) localStorage.setItem(preference, "true");
      else localStorage.removeItem(preference);
    } catch {
      /* Sound remains configurable in the current tab. */
    }
    if (muted.current) {
      enabled.current = false;
      setOn(false);
      cues.current.forEach((audio) => audio.pause());
      fade(0, () => ambient.current?.pause());
    } else void start();
  }
  function cue(kind: "select" | "reveal") {
    if (!enabled.current || document.hidden) return;
    cues.current = cues.current.filter((a) => !a.ended && !a.paused);
    if (cues.current.length >= 3) return;
    const audio = new Audio(
      `/art/fate_${kind === "select" ? "oracle_select" : "card_reveal"}.wav`,
    );
    audio.volume = effects;
    cues.current.push(audio);
    void audio.play().catch(() => {});
  }
  return { on, toggle, cue, music, setMusic, effects, setEffects };
}
