import { ResultLeaf } from "./ResultLeaf";
export function ReadingConclusion({
  themes,
  kind,
}: {
  themes: string[];
  kind: "tarot" | "numerology";
}) {
  const clean = themes.map((theme) => theme.trim().replace(/\.$/, ""));
  const thread = clean.at(-1) ?? "";
  return (
    <section
      className="reading-conclusion"
      aria-label="A thought to take with you"
    >
      <ResultLeaf
        status="A thought to take with you"
        title={
          kind === "tarot"
            ? "One thread to carry."
            : "Two lenses. One quiet pause."
        }
        evidence={
          <details className="folio-depth">
            <summary>About this reflection</summary>
            <p>
              FATE’s prompt uses the supplied source themes. You choose what
              resonates. Symbolic readings do not establish personal facts or
              future events.
            </p>
          </details>
        }
      >
        <p className="conclusion-thread">
          {kind === "tarot"
            ? `Leave with “${thread}” in mind.`
            : `The name theme is “${clean[0]}”. The annual theme is “${thread}”.`}
        </p>
        <p>
          {kind === "tarot"
            ? "What small, thoughtful response to this theme would feel useful today?"
            : "Which theme speaks to the decision in front of you, and which feels less relevant?"}
        </p>
      </ResultLeaf>
    </section>
  );
}
