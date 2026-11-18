import { useEffect, useRef, useState } from "react";
export function useSound() {
  const [on, setOn] = useState(false),
    [music, setMusic] = useState(0.1),
    [effects, setEffects] = useState(0.22);
  const ambient = useRef<HTMLAudioElement | null>(null),
    cues = useRef<HTMLAudioElement[]>([]);
  const enabled = useRef(false);
  enabled.current = on;
  useEffect(() => {
    if (ambient.current) ambient.current.volume = music;
  }, [music]);
  useEffect(() => {
    const visibility = () => {
      if (document.hidden) {
        ambient.current?.pause();
        cues.current.forEach((a) => a.pause());
      } else if (enabled.current) void ambient.current?.play().catch(() => {});
    };
    document.addEventListener("visibilitychange", visibility);
    return () => {
      document.removeEventListener("visibilitychange", visibility);
      ambient.current?.pause();
      cues.current.forEach((a) => a.pause());
    };
  }, []);
  async function toggle() {
    if (on) {
      ambient.current?.pause();
      cues.current.forEach((a) => a.pause());
      setOn(false);
      return;
    }
    if (!ambient.current) {
      ambient.current = new Audio("/art/fate_ambient_loop.wav");
      ambient.current.loop = true;
    }
    ambient.current.volume = music;
    try {
      await ambient.current.play();
      setOn(true);
    } catch {
      setOn(false);
    }
  }
  function cue(kind: "select" | "reveal") {
    if (!on || document.hidden) return;
    cues.current = cues.current.filter((a) => !a.ended);
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
