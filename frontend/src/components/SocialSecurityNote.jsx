import { SourceLinks } from "./SourceLink.jsx";

// Which social security system applies during the assignment, and the rule
// that decides it, with official sources.
export default function SocialSecurityNote({ socialSecurity }) {
  return (
    <details className="disclosure">
      <summary>Social security: {socialSecurity.applies} applies</summary>
      <p>{socialSecurity.rule}</p>
      <SourceLinks sources={socialSecurity.sources} />
    </details>
  );
}
