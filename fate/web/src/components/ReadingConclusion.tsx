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
      <p className="eyebrow">A THOUGHT TO TAKE WITH YOU</p>
      <h2>
        {kind === "tarot"
          ? "One thread to carry."
          : "Two lenses. One quiet pause."}
      </h2>
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
      <small>
        FATE’s reflection prompt uses the supplied source themes. You choose
        what resonates. Symbolic readings do not establish personal facts or
        future events.
      </small>
    </section>
  );
}
