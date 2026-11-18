import manifest from "./deck-manifest.json";
export const DECK = manifest;
export const CARD_BACK = "/art/deck/fate-back-v1/card-back.webp";
export type ArtworkEntry = (typeof manifest.cards)[keyof typeof manifest.cards];
export function artworkFor(cardId: string): ArtworkEntry | undefined {
  return (manifest.cards as Record<string, ArtworkEntry>)[cardId];
}
