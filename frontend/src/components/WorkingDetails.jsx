import { formatCHF, formatGBP } from "../format.js";

// Labels for the Swiss working, keyed by the API's field names; the JSON key
// order already follows the calculation, so no separate ordering is needed.
const SWISS_WORKING_LABELS = {
  gross_salary_chf: "Gross salary",
  ahv_iv_eo_chf: "AHV/IV/EO contributions (5.3%)",
  alv_chf: "ALV contributions (1.1%, up to the ceiling)",
  social_security_total_chf: "Social security total",
  net_salary_chf: "Net salary",
  professional_expenses_chf: "Less: professional expenses",
  federal_insurance_deduction_chf: "Less: insurance premiums (federal)",
  zurich_insurance_deduction_chf: "Less: insurance premiums (Zurich)",
  federal_taxable_income_chf: "Federal taxable income",
  zurich_taxable_income_chf: "Zurich taxable income",
  federal_tax_chf: "Federal tax",
  zurich_simple_tax_chf: "Zurich simple tax",
  cantonal_tax_chf: "Cantonal tax (95% of simple tax)",
  communal_tax_chf: "Communal tax (119% of simple tax)",
  personal_tax_chf: "Personal tax (city of Zurich)",
  total_tax_chf: "Total Swiss tax",
};

function UkTaxBands({ bands }) {
  return (
    <table className="working-table">
      <thead>
        <tr>
          <th scope="col">Band</th>
          <th scope="col" className="money">Rate</th>
          <th scope="col" className="money">Taxable amount</th>
          <th scope="col" className="money">Tax</th>
        </tr>
      </thead>
      <tbody>
        {bands.map((band) => (
          <tr key={band.band}>
            <th scope="row">{band.band}</th>
            <td className="money">{(Number(band.rate) * 100).toFixed(0)}%</td>
            <td className="money">{formatGBP(band.taxable_amount)}</td>
            <td className="money">{formatGBP(band.tax)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function SwissWorking({ swissWorking }) {
  return (
    <table className="working-table">
      <thead>
        <tr>
          <th scope="col">Step</th>
          <th scope="col" className="money">Amount</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(swissWorking).map(([key, value]) => (
          <tr key={key}>
            <th scope="row">{SWISS_WORKING_LABELS[key]}</th>
            <td className="money">{formatCHF(value)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default function WorkingDetails({ hostTax, swissWorking, yearLabel }) {
  return (
    <details className="disclosure working-details">
      <summary>How the figures are worked out ({yearLabel})</summary>

      <h4>Taxable pay before tax (I)</h4>
      <p>{formatGBP(hostTax.taxable_pay_before_tax)}</p>

      <h4>Gross-up iterations</h4>
      <p className="help-text">
        The employer pays the UK tax on top of the pay, and that payment is itself
        taxed, so the tax is found by repeating the calculation until two guesses
        in a row agree.
      </p>
      <ol className="iterations">
        {hostTax.iterations.map((iteration, index) => (
          <li key={index}>{formatGBP(iteration)}</li>
        ))}
      </ol>

      <h4>UK tax bands on pay including the tax</h4>
      <UkTaxBands bands={hostTax.tax_bands} />

      <h4>Hypothetical Swiss tax working (CHF)</h4>
      <SwissWorking swissWorking={swissWorking} />
    </details>
  );
}
