import SourceLink from "./SourceLink.jsx";

// Which social security system applies during the assignment, and the rule
// that decides it, with official sources.
export default function SocialSecurityNote({ socialSecurity }) {
  return (
    <section className="note">
      <h2>Social security</h2>
      <p>
        <strong>{socialSecurity.applies}</strong> applies. {socialSecurity.rule}
      </p>
      <p className="source-list">
        {socialSecurity.sources.map((source) => (
          <SourceLink key={source.url} source={source} />
        ))}
      </p>
    </section>
  );
}
