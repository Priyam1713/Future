import type { Oracle } from "../hooks/useOracle";
import { OracleGallery } from "../gallery/OracleGallery";
export default function GalleryScreen({ oracle }: { oracle: Oracle }) {
  return (
    <div className="gallery-room living-gallery-page">
      <p className="eyebrow">FATE · SIX WORLDS</p>
      <h1 id="gallery-title" ref={oracle.heading} tabIndex={-1}>
        The Oracle <em>Gallery.</em>
      </h1>
      <p className="gallery-room-note">
        Follow a world that draws you in, or find any of the 54 open rooms.
      </p>
      <OracleGallery oracle={oracle} />
    </div>
  );
}
