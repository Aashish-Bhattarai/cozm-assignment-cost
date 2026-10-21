// Money arrives from the API as strings with exactly two decimals
// (for example "154545.45"), so formatting only adds separators and a symbol.

function groupThousands(wholePart) {
  return wholePart.replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

function formatAmount(value) {
  const [wholePart, decimals = ""] = String(value).split(".");
  return `${groupThousands(wholePart)}.${decimals.padEnd(2, "0")}`;
}

export function formatGBP(value) {
  return `£${formatAmount(value)}`;
}

export function formatCHF(value) {
  return `CHF ${formatAmount(value)}`;
}

// A cost multiple such as "1.76" becomes "1.76×".
export function formatMultiple(value) {
  return `${formatAmount(value)}×`;
}
