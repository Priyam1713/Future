/** Exact renderer-derived static composition, also used without WebGL/motion. */
export function OrbPoster() {
  return (
    <div className="orb-fallback" aria-hidden="true">
      <img
        className="orb-poster"
        src="/art/orb-poster-v2.webp"
        alt=""
        width="960"
        height="960"
        fetchPriority="high"
      />
    </div>
  );
}
