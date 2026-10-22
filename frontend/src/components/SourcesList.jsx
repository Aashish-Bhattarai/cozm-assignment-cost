// Every official source the estimate relies on, with its full title, so the
// reader can check any rule without hunting through the tables.
export default function SourcesList({ sources }) {
  const entries = Object.entries(sources);
  return (
    <details className="disclosure">
      <summary>Official sources ({entries.length})</summary>
      <ul>
        {entries.map(([key, source]) => (
          <li key={key}>
            <a href={source.url} target="_blank" rel="noopener noreferrer">
              {source.label}
            </a>
          </li>
        ))}
      </ul>
    </details>
  );
}
