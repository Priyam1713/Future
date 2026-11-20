import type { Oracle } from "../hooks/useOracle";
import { ROOMS, type Id } from "./contracts";
import { StudyPage } from "./StudyPage";
import { DreamLedger, RemoteRoom } from "./SealedArchive";

export default function FutureScreen({
  id,
  oracle,
}: {
  id: Id;
  oracle: Oracle;
}) {
  const [slug, name, title] = ROOMS[id];
  const family = id >= 49 ? "tomorrow" : "dream";
  return (
    <article
      className={`future-room future-${family} future-room-${slug}`}
      data-still={oracle.reduced || oracle.paused}
    >
      <header className="future-entrance">
        <picture>
          <source
            media="(max-width:650px)"
            srcSet={`/art/future-${family}-720.webp`}
          />
          <img
            src={`/art/future-${family}-1440.webp`}
            width="1440"
            height="960"
            alt=""
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
            {family === "tomorrow"
              ? "The Tomorrow Machine"
              : "The Dream Archive"}{" "}
            · {name}
          </p>
          <h1>{title}</h1>
        </div>
      </header>
      <div className="future-stage">
        {id === 43 ? (
          <RemoteRoom oracle={oracle} />
        ) : id === 44 ? (
          <DreamLedger oracle={oracle} />
        ) : (
          <StudyPage id={id} oracle={oracle} />
        )}
      </div>
    </article>
  );
}
