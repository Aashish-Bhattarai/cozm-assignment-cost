import ErrorMessage from "./ErrorMessage.jsx";
import HelpText from "./HelpText.jsx";

// The number inputs, in display order. Values are kept as strings end to end;
// the API accepts numbers as strings and reports any problems per field.
const NUMBER_FIELDS = [
  {
    name: "base_salary_chf",
    label: "Base salary (CHF)",
    help: "Per year, before bonus.",
  },
  {
    name: "bonus_chf",
    label: "Bonus (CHF)",
    help: "Per year.",
  },
  {
    name: "exchange_rate_chf_per_gbp",
    label: "CHF per £1",
    help: "Converts every figure.",
  },
  {
    name: "housing_gbp_per_month",
    label: "Housing (£/month)",
    help: "London rent, both years.",
  },
  {
    name: "relocation_allowance_chf",
    label: "Relocation (CHF)",
    help: "Cash allowance, year\u00a01.",
  },
  {
    name: "moving_costs_gbp",
    label: "Moving costs (£)",
    help: "Flights, shipping, year\u00a01.",
  },
  {
    name: "temporary_housing_gbp",
    label: "Temporary housing (£)",
    help: "First 4\u00a0weeks, year\u00a01.",
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
          <HelpText>Switzerland only.</HelpText>
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
          <HelpText>United Kingdom only.</HelpText>
        </div>

        {NUMBER_FIELDS.map((field) => (
          <div className="field" key={field.name}>
            <label>
              {field.label}
              <input
                type="number"
                step="any"
                value={values[field.name]}
                aria-invalid={Boolean(errors[field.name])}
                onChange={(event) => onChange(field.name, event.target.value)}
              />
            </label>
            <HelpText>{field.help}</HelpText>
            <ErrorMessage messages={errors[field.name]} />
          </div>
        ))}
      </div>

      <button type="submit" className="primary-button" disabled={busy}>
        {busy ? "Calculating…" : "Estimate cost"}
      </button>
    </form>
  );
}
