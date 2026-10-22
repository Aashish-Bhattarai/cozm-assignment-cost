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

// Several sources for one row, shown compactly as "Sources 1 2 3"; each
// number's tooltip and accessible name carry the source's full title.
export function SourceLinks({ sources }) {
  if (!sources || sources.length === 0) {
    return null;
  }
  return (
    <span className="source-links">
      <span className="source-links-label">Sources</span>
      {sources.map((source, index) => (
        <a
          key={source.url}
          className="source-link"
          href={source.url}
          target="_blank"
          rel="noopener noreferrer"
          title={source.label}
          aria-label={`Source ${index + 1}: ${source.label}`}
        >
          {index + 1}
        </a>
      ))}
    </span>
  );
}
