import { useEffect, useRef, useState, type CSSProperties } from "react";
import { initialQuality } from "../orb/policy";
import { useArtifactLight } from "../components/ArtifactSurface";

interface Props {
  reduced: boolean;
  paused: boolean;
  value?: number | null;
  label?: string;
  active?: boolean;
  decorative?: boolean;
}
/** Independent material layers: original brass, live glass, geometry, light and numbers.
 * Compositor transforms need no Pixi context or per-frame React updates. */
export function NumberDial({
  reduced,
  paused,
  value,
  label = "A language of patterns",
  active = false,
  decorative = false,
}: Props) {
  const host = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  const [hidden, setHidden] = useState(document.hidden);
  const [quality] = useState(initialQuality);
  const turn = useRef(0);
  const motion = !reduced && !paused && visible && !hidden;
  const light = useArtifactLight(!motion || decorative);
  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => setVisible(entry.isIntersecting),
      { rootMargin: "40px" },
    );
    if (host.current) observer.observe(host.current);
    const visibility = () => setHidden(document.hidden);
    document.addEventListener("visibilitychange", visibility);
    return () => {
      observer.disconnect();
      document.removeEventListener("visibilitychange", visibility);
    };
  }, []);
  function rotate() {
    turn.current += 23;
    host.current?.style.setProperty("--dial-turn", `${turn.current}deg`);
  }
  const material = (
    <>
      <span className="dial-aura" />
      <div className="dial-depth">
        <div className="dial-glass">
          <span className="dial-mist" />
          <span className="dial-caustic" />
        </div>
        <img
          className="dial-brass"
          loading="lazy"
          decoding="async"
          src="/art/number-dial-480.webp"
          srcSet="/art/number-dial-480.webp 480w, /art/number-dial-v1.webp 960w"
          sizes="(max-width:700px) 90vw, 480px"
          alt=""
          width="960"
          height="960"
          draggable={false}
        />
        <svg
          className="dial-geometry"
          viewBox="0 0 500 500"
          fill="none"
          aria-hidden="true"
        >
          <circle cx="250" cy="250" r="190" />
          <circle cx="250" cy="250" r="161" />
          <path d="M250 60 414.5 345 85.5 345Z M250 440 85.5 155 414.5 155Z" />
          <path d="M250 60V440M60 250H440" />
          {Array.from({ length: 36 }, (_, i) => (
            <path
              key={i}
              d="M250 62v5"
              transform={`rotate(${i * 10} 250 250)`}
            />
          ))}
        </svg>
        <div className="dial-numbers">
          {Array.from({ length: 9 }, (_, i) => (
            <span key={i} style={{ "--n": i } as CSSProperties}>
              <i>{i + 1}</i>
            </span>
          ))}
        </div>
        <div className="dial-reflection" />
        <div className="dial-core" key={String(value) + label}>
          <strong>{value ?? "∴"}</strong>
          <span>{label}</span>
        </div>
        <div className="dial-sparks">
          {Array.from({ length: 12 }, (_, i) => (
            <i key={i} style={{ "--n": i } as CSSProperties} />
          ))}
        </div>
      </div>
    </>
  );
  return (
    <div
      ref={host}
      className={`number-dial ${active ? "aligning" : ""} ${motion ? "dial-moving" : "dial-still"} ${quality === "low" ? "dial-economy" : ""}`}
      data-renderer="layered-compositor"
      data-quality={quality}
      data-render-state={motion ? "running" : "paused"}
      data-target-fps={quality === "low" ? 30 : 60}
      aria-hidden={decorative || undefined}
      {...light}
    >
      {decorative ? (
        <div className="dial-touch">{material}</div>
      ) : (
        <button
          className="dial-touch tactile"
          aria-label="Turn the celestial dial"
          onClick={rotate}
        >
          {material}
        </button>
      )}
    </div>
  );
}
