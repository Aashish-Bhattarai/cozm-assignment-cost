// Every official source the estimate relies on, with its full title, so the
// reader can check any rule without hunting through the tables. A page used
// for two rules is listed once.
export default function SourcesList({ sources }) {
  const seenUrls = new Set();
  const entries = Object.entries(sources).filter(([, source]) => {
    if (seenUrls.has(source.url)) {
      return false;
    }
    seenUrls.add(source.url);
    return true;
  });
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
