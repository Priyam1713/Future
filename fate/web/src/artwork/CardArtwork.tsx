import { useState } from "react";
import type { Card } from "../types";
import { artworkFor, CARD_BACK } from "./registry";

/** Artwork identity never selects cards or supplies interpretations. The frame,
 * DOM caption, pose and foil are independent of replaceable bitmap assets. */
export function CardArtwork({
  card,
  back = false,
}: {
  card?: Card;
  back?: boolean;
}) {
  const [failed, setFailed] = useState(false);
  const artwork = card ? artworkFor(card.id) : undefined;
  if (back)
    return (
      <span
        className="card-illustration illustrated-card card-back-art"
        role="img"
        aria-label="FATE observatory card back"
      >
        <img
          src={CARD_BACK}
          srcSet="/art/deck/fate-back-v1/card-back-360.webp 360w, /art/deck/fate-back-v1/card-back.webp 768w"
          sizes="(max-width:760px) 34vw, 220px"
          alt=""
          width="768"
          height="1152"
          decoding="async"
          draggable={false}
        />
        <span className="card-foil" aria-hidden="true" />
      </span>
    );
  return (
    <span
      className="card-illustration illustrated-card"
      role="img"
      aria-label={`${card?.name ?? "Card"} · Pamela Colman Smith illustration`}
      data-artwork-id={card?.id}
    >
      {artwork && !failed ? (
        <img
          src={artwork.src}
          srcSet={artwork.srcSet}
          sizes="(max-width:760px) 34vw, 220px"
          alt=""
          width={artwork.width}
          height={artwork.height}
          decoding="async"
          draggable={false}
          onError={() => setFailed(true)}
        />
      ) : (
        <span className="artwork-unavailable">
          <strong>{card?.name}</strong>
          <small>Illustration unavailable</small>
        </span>
      )}
      <span className="card-bevel" aria-hidden="true" />
      <span className="card-foil" aria-hidden="true" />
    </span>
  );
}
