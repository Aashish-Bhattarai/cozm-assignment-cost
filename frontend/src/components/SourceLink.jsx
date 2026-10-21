// A small "Source" link to an official page; the API's label becomes the tooltip.

export default function SourceLink({ source }) {
  if (!source) {
    return null;
  }
  return (
    <a
      className="source-link"
      href={source.url}
      target="_blank"
      rel="noopener noreferrer"
      title={source.label}
    >
      Source
    </a>
  );
}

// Several sources for one row, shown as "Source 1", "Source 2", ...
export function SourceLinks({ sources }) {
  if (!sources || sources.length === 0) {
    return null;
  }
  return (
    <span className="source-links">
      {sources.map((source, index) => (
        <a
          key={source.url}
          className="source-link"
          href={source.url}
          target="_blank"
          rel="noopener noreferrer"
          title={source.label}
        >
          Source {index + 1}
        </a>
      ))}
    </span>
  );
}
