import { useRef, type PointerEvent, type ReactNode } from "react";

/** Tilt is an imperative, bounded visual response, never reading state. */
export function PhysicalCard({
  children,
  still,
}: {
  children: ReactNode;
  still: boolean;
}) {
  const ref = useRef<HTMLDivElement>(null),
    raf = useRef(0);
  function move(event: PointerEvent) {
    if (still) return;
    const el = ref.current!,
      r = el.getBoundingClientRect();
    const x = Math.max(
        -1,
        Math.min(1, ((event.clientX - r.left) / r.width) * 2 - 1),
      ),
      y = Math.max(
        -1,
        Math.min(1, ((event.clientY - r.top) / r.height) * 2 - 1),
      );
    cancelAnimationFrame(raf.current);
    raf.current = requestAnimationFrame(() => {
      if (!ref.current) return;
      el.style.setProperty("--tilt-x", `${-y * 5}deg`);
      el.style.setProperty("--tilt-y", `${x * 7}deg`);
      el.style.setProperty("--foil-x", `${(x + 1) * 50}%`);
    });
  }
  function reset() {
    cancelAnimationFrame(raf.current);
    ref.current?.style.setProperty("--tilt-x", "0deg");
    ref.current?.style.setProperty("--tilt-y", "0deg");
  }
  return (
    <div
      ref={ref}
      className="physical-card"
      onPointerMove={move}
      onPointerLeave={reset}
      onPointerUp={reset}
      onPointerCancel={reset}
    >
      {children}
    </div>
  );
}
