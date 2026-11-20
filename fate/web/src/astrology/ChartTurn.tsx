import { useEffect, useRef, type Dispatch, type SetStateAction } from "react";

const wrap = (angle: number) => ((((angle + 180) % 360) + 360) % 360) - 180;

export function ChartTurn({
  rotation,
  setRotation,
}: {
  rotation: number;
  setRotation: Dispatch<SetStateAction<number>>;
}) {
  const handle = useRef<HTMLDivElement>(null);
  const grab = useRef<{ id: number; x: number; angle: number } | null>(null);
  useEffect(() => {
    const element = handle.current;
    function turn(event: WheelEvent) {
      if (!event.shiftKey || event.ctrlKey || event.metaKey) return;
      const delta = event.deltaY || event.deltaX;
      if (!delta) return;
      event.preventDefault();
      setRotation((value) => wrap(value + Math.sign(delta) * 8));
    }
    element?.addEventListener("wheel", turn, { passive: false });
    return () => element?.removeEventListener("wheel", turn);
  }, [setRotation]);

  return (
    <div className="chart-turn-controls">
      <div
        className="chart-grip"
        ref={handle}
        aria-hidden="true"
        onPointerDown={(event) => {
          if (event.button !== 0 || !event.isPrimary) return;
          grab.current = {
            id: event.pointerId,
            x: event.clientX,
            angle: rotation,
          };
          event.currentTarget.setPointerCapture(event.pointerId);
          event.currentTarget.dataset.dragging = "true";
        }}
        onPointerMove={(event) => {
          const start = grab.current;
          if (start?.id !== event.pointerId) return;
          setRotation(wrap(start.angle + Math.round(event.clientX - start.x)));
        }}
        onLostPointerCapture={(event) => {
          grab.current = null;
          event.currentTarget.dataset.dragging = "false";
        }}
      >
        Drag to turn <span>· Shift + wheel</span>
      </div>
      <div className="chart-turn">
        <label>
          Turn the instrument{" "}
          <input
            type="range"
            min={-180}
            max={180}
            value={rotation}
            onChange={(event) => setRotation(event.target.valueAsNumber)}
            aria-valuetext={rotation + " degrees"}
          />
        </label>
        <button className="text-button" onClick={() => setRotation(0)}>
          Align Ascendant
        </button>
      </div>
    </div>
  );
}
