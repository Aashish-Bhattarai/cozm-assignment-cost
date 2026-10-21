// Every official source the estimate relies on, with its full title, so the
// reader can check any rule without hunting through the tables.
export default function SourcesList({ sources }) {
  return (
    <section className="note">
      <h2>Official sources</h2>
      <ul>
        {Object.entries(sources).map(([key, source]) => (
          <li key={key}>
            <a href={source.url} target="_blank" rel="noopener noreferrer">
              {source.label}
            </a>
          </li>
        ))}
      </ul>
    </section>
  );
}
