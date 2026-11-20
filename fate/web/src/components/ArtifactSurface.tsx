import { useEffect, useRef, type PointerEvent, type ReactNode } from "react";

/** Pointer light is decorative. Browser scroll and native controls keep their gestures. */
export function useArtifactLight(still: boolean) {
  const frame = useRef(0);
  const element = useRef<HTMLElement | null>(null);
  function reset() {
    cancelAnimationFrame(frame.current);
    element.current?.style.removeProperty("--light-x");
    element.current?.style.removeProperty("--light-y");
    element.current?.style.removeProperty("--tilt-x");
    element.current?.style.removeProperty("--tilt-y");
    element.current?.style.removeProperty("--foil-x");
    element.current = null;
  }
  useEffect(() => {
    if (still) reset();
    return reset;
  }, [still]);
  function move(event: PointerEvent<HTMLElement>) {
    if (still) return;
    const el = event.currentTarget;
    const { width, height, left, top } = el.getBoundingClientRect();
    const x = Math.max(0, Math.min(1, (event.clientX - left) / width));
    const y = Math.max(0, Math.min(1, (event.clientY - top) / height));
    element.current = el;
    cancelAnimationFrame(frame.current);
    frame.current = requestAnimationFrame(() => {
      el.style.setProperty("--light-x", `${x * 100}%`);
      el.style.setProperty("--light-y", `${y * 100}%`);
      el.style.setProperty("--tilt-x", `${(0.5 - y) * 8}deg`);
      el.style.setProperty("--tilt-y", `${(x - 0.5) * 12}deg`);
      el.style.setProperty("--foil-x", `${x * 100}%`);
    });
  }
  return {
    onPointerDown: move,
    onPointerMove: move,
    onPointerLeave: reset,
    onPointerUp: reset,
    onPointerCancel: reset,
  };
}

export function ArtifactSurface({
  children,
  still,
  className = "",
}: {
  children: ReactNode;
  still: boolean;
  className?: string;
}) {
  const light = useArtifactLight(still);
  return (
    <div className={`artifact-surface ${className}`} {...light}>
      {children}
    </div>
  );
}

export function SequenceMarks({
  step,
  total,
}: {
  step: number;
  total: number;
}) {
  return (
    <div className="sequence-marks" aria-hidden="true">
      {Array.from({ length: total }, (_, i) => (
        <i
          key={i}
          data-step={i === step ? "current" : i < step ? "seen" : "next"}
        />
      ))}
    </div>
  );
}
