import { useState } from "react";
import { fetchEstimate } from "../api.js";
import AssignmentSummary from "./AssignmentSummary.jsx";
import AssumptionsList from "./AssumptionsList.jsx";
import CostForm from "./CostForm.jsx";
import SocialSecurityNote from "./SocialSecurityNote.jsx";
import SourcesList from "./SourcesList.jsx";
import WorkingDetails from "./WorkingDetails.jsx";
import YearCostTable from "./YearCostTable.jsx";

// The exercise's test case doubles as the prefill.
const INITIAL_VALUES = {
  home_country: "CH",
  host_country: "GB",
  base_salary_chf: "150000",
  bonus_chf: "20000",
  exchange_rate_chf_per_gbp: "1.10",
  housing_gbp_per_month: "3000",
  relocation_allowance_chf: "5000",
  moving_costs_gbp: "6000",
  temporary_housing_gbp: "4000",
};

export default function CostEstimateTab() {
  const [values, setValues] = useState(INITIAL_VALUES);
  const [errors, setErrors] = useState({});
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  function handleChange(name, value) {
    setValues((current) => ({ ...current, [name]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setIsLoading(true);
    setErrors({});

    const { data, errors: apiErrors } = await fetchEstimate(values);
    setIsLoading(false);

    if (apiErrors) {
      // Never leave a table for old inputs on screen next to an error.
      setResult(null);
      setErrors(apiErrors);
      return;
    }
    setResult(data);
  }

  return (
    <div>
      <CostForm
        values={values}
        errors={errors}
        busy={isLoading}
        onChange={handleChange}
        onSubmit={handleSubmit}
      />

      {result && (
        <div className="results">
          <AssignmentSummary total={result.assignment_total} />

          {result.years.map((year) => (
            <section className="year-section" key={year.label}>
              <YearCostTable year={year} />
              <WorkingDetails
                hostTax={year.host_tax}
                swissWorking={result.swiss_working}
                yearLabel={year.label}
              />
            </section>
          ))}

          <SocialSecurityNote socialSecurity={result.social_security} />
          <AssumptionsList assumptions={result.assumptions} />
          <SourcesList sources={result.sources} />
        </div>
      )}
    </div>
  );
}
