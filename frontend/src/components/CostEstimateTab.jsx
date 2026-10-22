import { useEffect, useState } from "react";
import { fetchEstimate } from "../api.js";
import { formatGBP } from "../format.js";
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

// One sentence saying which inputs the numbers on screen were calculated from.
function describeInputs(inputs, years) {
  const pay = Number(inputs.base_salary_chf) + Number(inputs.bonus_chf);
  const benefits = years
    .map((year, index) => `year ${index + 1}: ${formatGBP(year.benefits_total_cost)}`)
    .join(", ");
  return (
    `Based on CHF ${pay.toLocaleString("en-GB")} salary and bonus ` +
    `at £1 = CHF ${inputs.exchange_rate_chf_per_gbp}, plus benefits (${benefits}).`
  );
}

export default function CostEstimateTab() {
  const [values, setValues] = useState(INITIAL_VALUES);
  const [errors, setErrors] = useState({});
  const [result, setResult] = useState(null);
  // Loading from the start: the test case is estimated as soon as the page opens.
  const [isLoading, setIsLoading] = useState(true);
  // The inputs behind the numbers on screen, and a counter that changes with
  // every new result so the headline cards can briefly highlight the update.
  const [estimatedFor, setEstimatedFor] = useState(null);
  const [updateCount, setUpdateCount] = useState(0);
  const [inputsChanged, setInputsChanged] = useState(false);
  const [selectedYear, setSelectedYear] = useState(0);

  function showResponse(inputs, { data, errors: apiErrors }) {
    setIsLoading(false);
    if (apiErrors) {
      // Never leave a table for old inputs on screen next to an error.
      setResult(null);
      setErrors(apiErrors);
      return;
    }
    setResult(data);
    setEstimatedFor(inputs);
    setUpdateCount((count) => count + 1);
    setInputsChanged(false);
  }

  // Show the test case straight away, so the page never opens empty.
  useEffect(() => {
    fetchEstimate(INITIAL_VALUES).then((response) => showResponse(INITIAL_VALUES, response));
  }, []);

  function handleChange(name, value) {
    setValues((current) => ({ ...current, [name]: value }));
    setInputsChanged(true);
  }

  function handleSubmit(event) {
    event.preventDefault();
    setIsLoading(true);
    setErrors({});
    fetchEstimate(values).then((response) => showResponse(values, response));
  }

  // Quiet context line normally; an amber warning only when the form no
  // longer matches the numbers on screen.
  let status = null;
  if (isLoading) {
    status = "Calculating…";
  } else if (result && inputsChanged) {
    status = "Inputs changed: press Estimate cost to recalculate.";
  } else if (result) {
    status = describeInputs(estimatedFor, result.years);
  }

  const year = result?.years[selectedYear];

  return (
    <div className="estimate-layout">
      <aside className="inputs-panel">
        <CostForm
          values={values}
          errors={errors}
          busy={isLoading}
          onChange={handleChange}
          onSubmit={handleSubmit}
        />
      </aside>

      <div className="results">
        <p
          className={inputsChanged && result ? "status status-stale" : "status"}
          role="status"
          aria-live="polite"
        >
          {status}
        </p>

        {!result && !isLoading && (
          <p className="empty-state">
            No estimate to show yet. Check the messages in the form, then press
            Estimate cost.
          </p>
        )}

        {result && (
          <div className={isLoading ? "results-body is-updating" : "results-body"}>
            <AssignmentSummary
              key={updateCount}
              years={result.years}
              total={result.assignment_total}
              selectedYear={selectedYear}
            />

            <div className="year-switch" role="group" aria-label="Choose a year">
              {result.years.map((item, index) => (
                <button
                  key={item.label}
                  type="button"
                  className={index === selectedYear ? "year-button is-selected" : "year-button"}
                  aria-pressed={index === selectedYear}
                  onClick={() => setSelectedYear(index)}
                >
                  {item.label}
                </button>
              ))}
            </div>

            <YearCostTable year={year} />
            <WorkingDetails
              hostTax={year.host_tax}
              swissWorking={result.swiss_working}
              yearLabel={year.label}
            />

            <SocialSecurityNote socialSecurity={result.social_security} />
            <AssumptionsList assumptions={result.assumptions} />
            <SourcesList sources={result.sources} />
          </div>
        )}
      </div>
    </div>
  );
}
