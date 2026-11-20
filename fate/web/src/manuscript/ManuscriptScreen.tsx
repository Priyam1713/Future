import type { Oracle } from "../hooks/useOracle";
import { ArchiveRoom } from "./ArchiveRoom";
import { CompassRoom } from "./CompassRoom";
import { SkyRoom } from "./SkyRoom";
import { ENVIRONMENTS, ROOMS, type ArchiveId, type Id } from "./contracts";

export default function ManuscriptScreen({
  id,
  oracle,
}: {
  id: Id;
  oracle: Oracle;
}) {
  const [slug, name, title, environment] = ROOMS[id];
  return (
    <article
      className={`folio-room folio-${environment} folio-${slug}`}
      data-still={oracle.reduced || oracle.paused}
    >
      <header className="folio-entrance">
        <picture>
          <source
            media="(max-width: 650px)"
            srcSet={`/art/folio-${environment}-720.webp`}
          />
          <img
            src={`/art/folio-${environment}-1440.webp`}
            alt=""
            width="1440"
            height="960"
            fetchPriority="high"
          />
        </picture>
        <div>
          <button
            className="text-button"
            onClick={() => oracle.navigate("gallery")}
          >
            ← Oracle Gallery
          </button>
          <p className="eyebrow">
            {ENVIRONMENTS[environment]}
            {id !== 40 && ` · ${name}`}
          </p>
          <h1>{title}</h1>
        </div>
      </header>
      <div className="folio-stage">
        {id === 40 ? (
          <CompassRoom oracle={oracle} />
        ) : id === 5 || id === 6 || id === 7 ? (
          <SkyRoom id={id} oracle={oracle} />
        ) : (
          <ArchiveRoom id={id as ArchiveId} oracle={oracle} />
        )}
      </div>
    </article>
  );
}
