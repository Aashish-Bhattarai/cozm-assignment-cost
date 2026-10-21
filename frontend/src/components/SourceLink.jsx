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
