import ErrorMessage from "./ErrorMessage.jsx";
import HelpText from "./HelpText.jsx";

// The number inputs, in display order. Values are kept as strings end to end;
// the API accepts numbers as strings and reports any problems per field.
const NUMBER_FIELDS = [
  {
    name: "base_salary_chf",
    label: "Base salary (CHF)",
    help: "Yearly salary in Switzerland, before any bonus.",
  },
  {
    name: "bonus_chf",
    label: "Bonus (CHF)",
    help: "Yearly bonus paid on top of the base salary.",
  },
  {
    name: "exchange_rate_chf_per_gbp",
    label: "Exchange rate (CHF per £1)",
    help: "How many Swiss francs one pound is worth, used to convert every figure.",
  },
  {
    name: "housing_gbp_per_month",
    label: "London housing (£ per month)",
    help: "Rent the employer pays for the employee in London, in both years.",
  },
  {
    name: "relocation_allowance_chf",
    label: "Relocation allowance (CHF, year 1)",
    help: "A one-off cash allowance for the move, paid in year 1 only.",
  },
  {
    name: "moving_costs_gbp",
    label: "Moving costs (£, year 1)",
    help: "One-off costs of moving to the UK, paid by the employer in year 1 only.",
  },
  {
    name: "temporary_housing_gbp",
    label: "Temporary housing (£, year 1)",
    help: "Short-term accommodation on arrival, paid in year 1 only.",
  },
];

export default function CostForm({ values, errors, busy, onChange, onSubmit }) {
  return (
    <form
      className="cost-form"
      onSubmit={onSubmit}
      // Validation errors come from the API so that they match its rules.
      noValidate
    >
      <ErrorMessage messages={errors.__all__} />

      <div className="form-grid">
        <div className="field">
          <label>
            Home country
            <select
              value={values.home_country}
              onChange={(event) => onChange("home_country", event.target.value)}
            >
              <option value="CH">Switzerland</option>
            </select>
          </label>
          <HelpText>Only Switzerland is supported in this exercise.</HelpText>
        </div>
        <div className="field">
          <label>
            Host country
            <select
              value={values.host_country}
              onChange={(event) => onChange("host_country", event.target.value)}
            >
              <option value="GB">United Kingdom</option>
            </select>
          </label>
          <HelpText>Only the United Kingdom is supported in this exercise.</HelpText>
        </div>

        {NUMBER_FIELDS.map((field) => (
          <div className="field" key={field.name}>
            <label>
              {field.label}
              <input
                type="number"
                step="any"
                value={values[field.name]}
                onChange={(event) => onChange(field.name, event.target.value)}
              />
            </label>
            <HelpText>{field.help}</HelpText>
            <ErrorMessage messages={errors[field.name]} />
          </div>
        ))}
      </div>

      <button type="submit" className="primary-button" disabled={busy}>
        Estimate cost
      </button>
    </form>
  );
}
