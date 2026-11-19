import type { Oracle } from "../hooks/useOracle";
import { OracleGallery } from "../gallery/OracleGallery";
export default function GalleryScreen({ oracle }: { oracle: Oracle }) {
  return (
    <div className="gallery-room page-enter">
      <p className="eyebrow">54 TRADITIONS · SIX COLLECTIONS</p>
      <h1 id="gallery-title" ref={oracle.heading} tabIndex={-1}>
        Follow your <em>curiosity.</em>
      </h1>
      <p className="gallery-room-note">
        Two rooms open. A whole universe to discover.
      </p>
      <OracleGallery oracle={oracle} libraryOnly />
    </div>
  );
}
