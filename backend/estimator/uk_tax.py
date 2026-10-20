"""UK income tax and the tax-on-tax gross-up, for the 2026/27 tax year (England).

Every rate and threshold below is a published HMRC / GOV.UK figure. SOURCES
holds the official link for each one so the front end can show it next to the
number.

All money is decimal.Decimal, constructed from strings, so the arithmetic is
exact. Nothing here rounds: rounding to pence happens only for display, in
later slices.
"""

from dataclasses import dataclass, field
from decimal import Decimal

# --- 2026/27 England rates and thresholds -----------------------------------

PERSONAL_ALLOWANCE = Decimal("12570")
ALLOWANCE_TAPER_START = Decimal("100000")

# Band limits are on taxable income (what is left after the personal allowance).
BASIC_RATE_BAND_LIMIT = Decimal("37700")
HIGHER_RATE_BAND_LIMIT = Decimal("125140")
BASIC_RATE = Decimal("0.20")
HIGHER_RATE = Decimal("0.40")
ADDITIONAL_RATE = Decimal("0.45")

# The gross-up iteration stops once two successive guesses differ by less
# than this (a ten-thousandth of a penny).
GROSS_UP_TOLERANCE = Decimal("0.000001")
MAX_GROSS_UP_ITERATIONS = 200

SOURCES = {
    "personal_allowance_and_taper": {
        "label": "Income Tax rates and Personal Allowances (GOV.UK)",
        "url": "https://www.gov.uk/income-tax-rates",
    },
    "tax_bands_2026_27": {
        "label": "Rates and thresholds for employers 2026 to 2027 (GOV.UK)",
        "url": "https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027",
    },
    "employer_paid_tax_is_taxable": {
        "label": "EIM00580: Pecuniary liability — tax paid by the employer is taxable (GOV.UK)",
        "url": "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim00580",
    },
    "grossing_up": {
        "label": "PAYE72028: Grossing up (GOV.UK)",
        "url": "https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye72028",
    },
}


def personal_allowance(income: Decimal) -> Decimal:
    """Return the personal allowance for a given income.

    Above £100,000 the allowance falls by £1 for every £2 of extra income,
    so it reaches zero at £125,140. The taper makes tax an unusual curve:
    the effective marginal rate between £100,000 and £125,140 is 60%, not
    40%, which is why the gross-up has to be solved numerically.
    """
    if income <= ALLOWANCE_TAPER_START:
        return PERSONAL_ALLOWANCE
    reduction = (income - ALLOWANCE_TAPER_START) / Decimal(2)
    return max(PERSONAL_ALLOWANCE - reduction, Decimal("0"))


def income_tax_bands(income: Decimal) -> list[dict]:
    """Split income across the rate bands and return the working per band.

    Returns one dict per band that actually receives income ("Basic rate",
    "Higher rate", "Additional rate") with its rate, the amount taxed in
    that band, and the tax due on it — so the UI can show how the total is
    built up. Bands apply to taxable income, not to gross income.
    """
    taxable = max(income - personal_allowance(income), Decimal("0"))

    bands = []
    for name, rate, band_start, band_end in [
        ("Basic rate", BASIC_RATE, Decimal("0"), BASIC_RATE_BAND_LIMIT),
        ("Higher rate", HIGHER_RATE, BASIC_RATE_BAND_LIMIT, HIGHER_RATE_BAND_LIMIT),
        ("Additional rate", ADDITIONAL_RATE, HIGHER_RATE_BAND_LIMIT, None),
    ]:
        # The last band has no upper limit: it stretches to the whole of
        # the taxable income.
        upper = band_end if band_end is not None else taxable
        amount = max(min(taxable, upper) - band_start, Decimal("0"))
        if amount > 0:
            bands.append({
                "band": name,
                "rate": rate,
                "taxable_amount": amount,
                "tax": amount * rate,
            })
    return bands


def income_tax(income: Decimal) -> Decimal:
    """Return the total income tax on a given income (unrounded)."""
    return sum((band["tax"] for band in income_tax_bands(income)), Decimal("0"))


@dataclass(frozen=True)
class GrossUpResult:
    """The answer to a tax-on-tax gross-up, with the working.

    ``iterations`` holds the trial value of T after every step so the UI
    can show how the answer was reached.
    """

    tax: Decimal
    iterations: list[Decimal] = field(default_factory=list)


def gross_up_tax(taxable_pay_before_tax: Decimal) -> GrossUpResult:
    """Find the UK tax T such that UKTax(pay + T) = T.

    When the employer pays the employee's UK income tax on top of the pay,
    that payment is itself taxable earnings (EIM00580), which is why the
    tax base is pay + T rather than just pay.

    A single multiplication gives the wrong answer: the personal allowance
    tapers away above £100,000 and the rate bands apply to a total that
    includes the very tax being solved for. So the fixed point is found by
    iteration: start from T = 0 and repeatedly set T = UKTax(pay + T) until
    it stops moving.
    """
    tax = Decimal("0")
    iterations = []
    for _ in range(MAX_GROSS_UP_ITERATIONS):
        next_tax = income_tax(taxable_pay_before_tax + tax)
        iterations.append(next_tax)
        if abs(next_tax - tax) < GROSS_UP_TOLERANCE:
            return GrossUpResult(tax=next_tax, iterations=iterations)
        tax = next_tax
    raise RuntimeError(
        f"Tax-on-tax did not converge within {MAX_GROSS_UP_ITERATIONS} iterations"
    )
