import { formatGBP, formatMultiple } from "../format.js";

// The headline figures for the whole two-year assignment.
export default function AssignmentSummary({ total }) {
  return (
    <section className="assignment-summary">
      <h2>Whole assignment</h2>
      <p className="summary-figure">
        Total employer cost: <strong>{formatGBP(total.total_employer_cost)}</strong>
      </p>
      <p>
        That is {formatMultiple(total.multiple_of_home_pay)} the employee's home pay
        of {formatGBP(total.home_pay)} over the two years.
      </p>
    </section>
  );
}
