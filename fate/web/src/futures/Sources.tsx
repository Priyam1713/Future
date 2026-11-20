import type { Source } from "./contracts";

export function Sources({
  sources,
  notes = [],
}: {
  sources: Source[];
  notes?: string[];
}) {
  return (
    <details className="lab-depth">
      <summary>Sources and method</summary>
      {notes.map((note, i) => (
        <p key={i}>{note}</p>
      ))}
      <ul>
        {sources.map((source) => (
          <li key={source.id}>
            {source.url.startsWith("https://") ||
            source.url.startsWith("http://") ? (
              <a href={source.url} target="_blank" rel="noreferrer">
                {source.title}
              </a>
            ) : (
              source.title
            )}
            {source.locator && <small>{source.locator}</small>}
          </li>
        ))}
      </ul>
    </details>
  );
}
