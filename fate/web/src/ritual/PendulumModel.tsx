import { useEffect, useRef } from "react";

export function PendulumModel({ still }: { still: boolean }) {
  const pivot = useRef<HTMLDivElement>(null),
    body = useRef<HTMLDivElement>(null);
  const animation = useRef<Animation | null>(null),
    drag = useRef<number | null>(null),
    angle = useRef(0);
  const stop = () => {
    animation.current?.cancel();
    animation.current = null;
  };
  useEffect(() => {
    const stopIfHidden = () => {
      if (document.hidden) stop();
    };
    document.addEventListener("visibilitychange", stopIfHidden);
    return () => {
      stop();
      document.removeEventListener("visibilitychange", stopIfHidden);
    };
  }, [still]);
  function swing(initial: number) {
    stop();
    if (!body.current) return;
    body.current.style.transform = "";
    if (still) return;
    const frames = Array.from({ length: 81 }, (_, i) => {
      const t = (i / 80) * 4;
      const a =
        i === 80 ? 0 : initial * Math.exp(-t * 0.94) * Math.cos(t * 7.2);
      return { transform: `rotate(${a}deg)` };
    });
    animation.current = body.current.animate(frames, {
      duration: 4000,
      easing: "linear",
    });
  }
  return (
    <div className="pendulum-plinth">
      <div
        className="pendulum-model"
        ref={pivot}
        aria-hidden="true"
        onPointerDown={(event) => {
          if (still) return;
          stop();
          drag.current = event.pointerId;
          angle.current = 0;
          event.currentTarget.setPointerCapture(event.pointerId);
        }}
        onPointerMove={(event) => {
          if (
            event.pointerId !== drag.current ||
            !pivot.current ||
            !body.current
          )
            return;
          const box = pivot.current.getBoundingClientRect();
          angle.current = Math.max(
            -44,
            Math.min(
              44,
              (-Math.atan2(
                event.clientX - box.left - box.width / 2,
                Math.max(45, event.clientY - box.top),
              ) *
                180) /
                Math.PI,
            ),
          );
          body.current.style.transform = `rotate(${angle.current}deg)`;
        }}
        onPointerUp={(event) => {
          if (event.pointerId === drag.current) {
            drag.current = null;
            swing(angle.current);
          }
        }}
        onPointerCancel={() => {
          drag.current = null;
          swing(0);
        }}
      >
        <i className="pendulum-pin" />
        <div className="pendulum-rig" ref={body}>
          <i className="pendulum-chain" />
          <i className="pendulum-weight" />
        </div>
        <div className="pendulum-arc" />
      </div>
      <button
        type="button"
        className="text-button"
        onClick={() => swing(36)}
        disabled={still}
      >
        Swing the display model
      </button>
      <p className="scope-note">
        Display motion is decorative and never enters the reading.
      </p>
    </div>
  );
}
