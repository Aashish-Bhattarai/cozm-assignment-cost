import { formatGBP, formatMultiple } from "../format.js";
import SourceLink, { SourceLinks } from "./SourceLink.jsx";

// The section headings follow the order of the brief.
function SectionRow({ title }) {
  return (
    <tr className="section-row">
      <th colSpan={5} scope="colgroup">
        {title}
      </th>
    </tr>
  );
}

export default function YearCostTable({ year }) {
  const { home_pay: homePay, host_tax: hostTax, deductions } = year;

  return (
    <table className="cost-table">
      <caption className="visually-hidden">{year.label}</caption>
      <thead>
        <tr>
          <th scope="col">Item</th>
          <th scope="col" className="money">
            Cost
          </th>
          <th scope="col">Tax treatment</th>
          <th scope="col" className="money">
            Taxable amount
          </th>
          <th scope="col">Source</th>
        </tr>
      </thead>

      <tbody>
        <SectionRow title="1. Home pay" />
        <tr>
          <td>Salary</td>
          <td className="money">{formatGBP(homePay.salary)}</td>
          <td colSpan={3} />
        </tr>
        <tr>
          <td>Bonus</td>
          <td className="money">{formatGBP(homePay.bonus)}</td>
          <td colSpan={3} />
        </tr>
        <tr className="subtotal-row">
          <td>Home pay total</td>
          <td className="money">{formatGBP(homePay.total)}</td>
          <td colSpan={3} />
        </tr>
      </tbody>

      <tbody>
        <SectionRow title="2. Assignment benefits" />
        {year.benefits.map((benefit) => (
          <tr key={benefit.name}>
            <td>
              {benefit.name}
              {benefit.note && <small className="row-note">{benefit.note}</small>}
            </td>
            <td className="money">{formatGBP(benefit.cost)}</td>
            <td>
              <span className="tag">{benefit.tag}</span>
            </td>
            <td className="money">{formatGBP(benefit.taxable_amount)}</td>
            <td>
              <SourceLink source={benefit.source} />
            </td>
          </tr>
        ))}
        <tr className="subtotal-row">
          <td>Benefits total</td>
          <td className="money">{formatGBP(year.benefits_total_cost)}</td>
          <td />
          <td className="money">{formatGBP(year.taxable_benefits_total)}</td>
          <td />
        </tr>
      </tbody>

      <tbody>
        <SectionRow title="3. Host tax and charges paid by the employer" />
        <tr>
          <td>
            UK income tax
            <small className="row-note">
              The employer pays the tax as well, and that payment is itself taxed,
              so the figure is the grossed-up amount.
            </small>
          </td>
          <td className="money">{formatGBP(hostTax.uk_income_tax)}</td>
          <td colSpan={2} />
          <td>
            <SourceLinks sources={hostTax.sources} />
          </td>
        </tr>
        {hostTax.employer_charges.map((charge) => (
          <tr key={charge.name}>
            <td>
              {charge.name}
              <small className="row-note">{charge.reason}</small>
            </td>
            <td className="money">{formatGBP(charge.amount)}</td>
            <td colSpan={2} />
            <td>
              <SourceLink source={charge.source} />
            </td>
          </tr>
        ))}
        <tr className="subtotal-row">
          <td>Host tax and charges total</td>
          <td className="money">{formatGBP(hostTax.total)}</td>
          <td colSpan={3} />
        </tr>
      </tbody>

      <tbody>
        <SectionRow title="4. Deductions" />
        <tr>
          <td>
            Hypothetical Swiss income tax
            <small className="row-note">
              Withheld from the employee's home pay, so it reduces the cost.
            </small>
          </td>
          <td className="money">-{formatGBP(deductions.hypothetical_swiss_tax)}</td>
          <td colSpan={2} />
          <td>
            <SourceLinks sources={deductions.sources.hypothetical_swiss_tax} />
          </td>
        </tr>
        <tr>
          <td>
            Hypothetical Swiss social security
            <small className="row-note">
              Withheld from the employee's home pay, so it reduces the cost.
            </small>
          </td>
          <td className="money">
            -{formatGBP(deductions.hypothetical_swiss_social_security)}
          </td>
          <td colSpan={2} />
          <td>
            <SourceLinks sources={deductions.sources.hypothetical_swiss_social_security} />
          </td>
        </tr>
        <tr className="subtotal-row">
          <td>Deductions total</td>
          <td className="money">-{formatGBP(deductions.total)}</td>
          <td colSpan={3} />
        </tr>
      </tbody>

      <tbody>
        <tr className="total-row">
          <td>
            Total employer cost
            <small className="row-note">
              Each line is rounded to the penny; totals are calculated before
              rounding, so adding the lines by hand can differ by 1p.
            </small>
          </td>
          <td className="money">{formatGBP(year.total_employer_cost)}</td>
          <td colSpan={3} />
        </tr>
        <tr>
          <td>Multiple of home pay</td>
          <td className="money">{formatMultiple(year.multiple_of_home_pay)}</td>
          <td colSpan={3} />
        </tr>
      </tbody>
    </table>
  );
}
