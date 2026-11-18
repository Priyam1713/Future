import { useEffect, useRef, useState } from "react";
import type { OrbController } from "./orb/createOrbScene";
import { OrbPoster } from "./orb/OrbPoster";

/** React owns lifecycle and the poster; the renderer owns no readable UI. */
export default function Orb({
  reduced,
  paused,
}: {
  reduced: boolean;
  paused: boolean;
}) {
  const host = useRef<HTMLDivElement>(null),
    controller = useRef<OrbController | null>(null);
  const latest = useRef({ reduced, paused });
  latest.current = { reduced, paused };
  const [ready, setReady] = useState(false);
  useEffect(() => {
    const element = host.current!,
      abort = new AbortController();
    let started = false,
      idle: number | undefined,
      raf = 0;
    const start = () => {
      if (
        started ||
        abort.signal.aborted ||
        matchMedia("(prefers-reduced-motion: reduce)").matches
      )
        return;
      started = true;
      const initialize = () => {
        void import("./orb/createOrbScene")
          .then(({ createOrbScene }) =>
            createOrbScene(element, latest.current, abort.signal, setReady),
          )
          .then((scene) => {
            if (abort.signal.aborted) scene.destroy();
            else {
              scene.update(latest.current);
              controller.current = scene;
            }
          })
          .catch(() => {
            if (!abort.signal.aborted) setReady(false);
          });
      };
      raf = requestAnimationFrame(() => {
        if ("requestIdleCallback" in window)
          idle = window.requestIdleCallback(initialize, { timeout: 700 });
        else initialize();
      });
    };
    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting) start();
      },
      { rootMargin: "80px" },
    );
    observer.observe(element);
    const media = matchMedia("(prefers-reduced-motion: reduce)");
    const resume = () => {
      if (!media.matches) start();
    };
    media.addEventListener("change", resume);
    return () => {
      abort.abort();
      observer.disconnect();
      media.removeEventListener("change", resume);
      cancelAnimationFrame(raf);
      if (idle !== undefined) window.cancelIdleCallback(idle);
      controller.current?.destroy();
      controller.current = null;
    };
  }, []);
  useEffect(
    () => controller.current?.update({ reduced, paused }),
    [reduced, paused],
  );
  return (
    <div
      ref={host}
      className={`orb ${ready ? "orb-ready" : ""}`}
      data-renderer={ready ? "pixi" : "artwork"}
    >
      <OrbPoster />
    </div>
  );
}
