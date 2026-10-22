import { useEffect, useState } from "react";
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

function timeNow() {
  return new Date().toLocaleTimeString([], { hour: "numeric", minute: "2-digit", second: "2-digit" });
}

export default function CostEstimateTab() {
  const [values, setValues] = useState(INITIAL_VALUES);
  const [errors, setErrors] = useState({});
  const [result, setResult] = useState(null);
  // Loading from the start: the test case is estimated as soon as the page opens.
  const [isLoading, setIsLoading] = useState(true);
  const [updatedAt, setUpdatedAt] = useState(null);
  const [inputsChanged, setInputsChanged] = useState(false);
  const [selectedYear, setSelectedYear] = useState(0);

  function showResponse({ data, errors: apiErrors }) {
    setIsLoading(false);
    if (apiErrors) {
      // Never leave a table for old inputs on screen next to an error.
      setResult(null);
      setErrors(apiErrors);
      return;
    }
    setResult(data);
    setUpdatedAt(timeNow());
    setInputsChanged(false);
  }

  // Show the test case straight away, so the page never opens empty.
  useEffect(() => {
    fetchEstimate(INITIAL_VALUES).then(showResponse);
  }, []);

  function handleChange(name, value) {
    setValues((current) => ({ ...current, [name]: value }));
    setInputsChanged(true);
  }

  function handleSubmit(event) {
    event.preventDefault();
    setIsLoading(true);
    setErrors({});
    fetchEstimate(values).then(showResponse);
  }

  let status = "";
  if (isLoading) {
    status = "Calculating…";
  } else if (result && inputsChanged) {
    status = "Inputs changed: press Estimate cost to recalculate.";
  } else if (result) {
    status = `Estimate updated at ${updatedAt}.`;
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
          className={inputsChanged ? "status status-stale" : "status"}
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
            <AssignmentSummary years={result.years} total={result.assignment_total} />

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
