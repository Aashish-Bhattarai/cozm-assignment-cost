import { useEffect, useState } from "react";
import { fetchImmigration } from "../api.js";
import { formatGBP } from "../format.js";
import ErrorMessage from "./ErrorMessage.jsx";
import SourceLink from "./SourceLink.jsx";

const SPONSOR_SIZES = [
  { value: "medium_large", label: "Medium or large sponsor" },
  { value: "small", label: "Small sponsor" },
];

export default function ImmigrationTab() {
  const [sponsorSize, setSponsorSize] = useState("medium_large");
  const [data, setData] = useState(null);
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(true);

  // Fetch whenever the sponsor size changes. The cancelled flag stops an
  // older, slower response from overwriting a newer one.
  useEffect(() => {
    let cancelled = false;

    fetchImmigration(sponsorSize).then(({ data: result, errors: apiErrors }) => {
      if (cancelled) {
        return;
      }
      setIsLoading(false);
      if (apiErrors) {
        setErrors(apiErrors);
      } else {
        setErrors({});
        setData(result);
      }
    });

    return () => {
      cancelled = true;
    };
  }, [sponsorSize]);

  function handleSponsorSizeChange(value) {
    setSponsorSize(value);
    setIsLoading(true);
    setErrors({});
  }

  return (
    <div className="immigration">
      <div className="field field-inline">
        <label>
          Sponsor size
          <select
            value={sponsorSize}
            onChange={(event) => handleSponsorSizeChange(event.target.value)}
          >
            {SPONSOR_SIZES.map((size) => (
              <option key={size.value} value={size.value}>
                {size.label}
              </option>
            ))}
          </select>
        </label>
        <ErrorMessage messages={errors.__all__ ?? errors.sponsor_size} />
      </div>

      {isLoading && <p className="status">Loading…</p>}

      {data && !isLoading && (
        <div>
          <div className="info-grid">
            {data.sections.map((section) => (
              <section className="info-card" key={section.title}>
                <h3>{section.title}</h3>
                <p className="info-summary">{section.summary}</p>
                <ul>
                  {section.items.map((item) => (
                    <li key={item.text}>
                      {item.text} <SourceLink source={item.source} />
                    </li>
                  ))}
                </ul>
              </section>
            ))}
          </div>

          <table className="cost-table">
            <caption>Costs</caption>
            <thead>
              <tr>
                <th scope="col">Item</th>
                <th scope="col" className="money">Amount</th>
                <th scope="col">Payer</th>
                <th scope="col">Note</th>
                <th scope="col">Source</th>
              </tr>
            </thead>
            <tbody>
              {data.costs.map((cost) => (
                <tr key={cost.item}>
                  <td>{cost.item}</td>
                  <td className="money">{formatGBP(cost.amount)}</td>
                  <td>{cost.payer}</td>
                  <td>{cost.note}</td>
                  <td>
                    <SourceLink source={cost.source} />
                  </td>
                </tr>
              ))}
              <tr className="total-row">
                <td>Total</td>
                <td className="money">{formatGBP(data.total_cost)}</td>
                <td colSpan={3} />
              </tr>
            </tbody>
          </table>

          <table className="cost-table">
            <caption>Timeline</caption>
            <thead>
              <tr>
                <th scope="col">Step</th>
                <th scope="col">Duration</th>
                <th scope="col">Source</th>
              </tr>
            </thead>
            <tbody>
              {data.timeline.map((entry) => (
                <tr key={entry.step}>
                  <td>{entry.step}</td>
                  <td>{entry.duration}</td>
                  <td>
                    <SourceLink source={entry.source} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
