import { formatGBP, formatMultiple } from "../format.js";

// The three headline figures: each year and the whole assignment.
export default function AssignmentSummary({ years, total }) {
  const cards = [
    ...years.map((year) => ({
      label: year.label,
      cost: year.total_employer_cost,
      multiple: year.multiple_of_home_pay,
    })),
    {
      label: "Whole assignment",
      cost: total.total_employer_cost,
      multiple: total.multiple_of_home_pay,
    },
  ];

  return (
    <section className="summary-cards" aria-label="Total employer cost">
      {cards.map((card) => (
        <div className="summary-card" key={card.label}>
          <span className="summary-label">{card.label}</span>
          <strong className="summary-cost">{formatGBP(card.cost)}</strong>
          <span className="summary-multiple">
            {formatMultiple(card.multiple)} home pay
          </span>
        </div>
      ))}
    </section>
  );
}
