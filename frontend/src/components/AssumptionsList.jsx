import SourceLink from "./SourceLink.jsx";

// The assumptions behind the estimate; an assumption from the brief itself has
// no source, and SourceLink renders nothing in that case.
export default function AssumptionsList({ assumptions }) {
  return (
    <section className="note">
      <h2>Assumptions</h2>
      <ul>
        {assumptions.map((assumption) => (
          <li key={assumption.text}>
            {assumption.text} <SourceLink source={assumption.source} />
          </li>
        ))}
      </ul>
    </section>
  );
}
