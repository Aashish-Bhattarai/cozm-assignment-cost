"""Assignment benefits under UK tax rules, and whether each one is taxable.

Every benefit is tagged with exactly one of the three treatments below, so
the costing knows what to add to the taxable pay. The tagging follows
docs/decision-ledger.md, section D8.
"""

from dataclasses import dataclass
from decimal import Decimal

TAXABLE_CASH = "Taxable cash"
TAXABLE_BENEFIT_IN_KIND = "Taxable benefit in kind"
NOT_TAXABLE = "Not taxable in the UK"

# The first £8,000 of qualifying removal costs and benefits is free of tax.
# Moving costs and temporary housing share one limit, so the exemption is
# applied in that order: moving costs first, then temporary housing.
REMOVAL_EXEMPTION_LIMIT = Decimal("8000")

MONTHS_PER_YEAR = 12
ZERO = Decimal("0")

SOURCES = {
    "living_accommodation": {
        "label": "EIM11431: living accommodation is charged on the greater of the annual value and the rent (GOV.UK)",
        "url": "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim11431",
    },
    "relocation_exemption": {
        "label": "EIM03103: £8,000 exemption for removal expenses and benefits (GOV.UK)",
        "url": "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim03103",
    },
    "temporary_living_accommodation": {
        "label": "EIM03117: temporary accommodation counts against the £8,000 limit at cost to the employer (GOV.UK)",
        "url": "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim03117",
    },
    "relocation_excess": {
        "label": "Qualifying relocation costs over £8,000 must be reported on form P11D (GOV.UK)",
        "url": "https://www.gov.uk/expenses-and-benefits-relocation/what-to-report-and-pay",
    },
    "flat_rate_relocation_allowance": {
        "label": "EIM03139: flat-rate relocation allowances are taxable cash (GOV.UK)",
        "url": "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim03139",
    },
}


@dataclass(frozen=True)
class Benefit:
    """One benefit row in GBP, as shown in a year's cost breakdown."""

    name: str
    cost: Decimal
    tag: str
    taxable_amount: Decimal
    note: str
    source_key: str


def housing_benefit(rent_per_month: Decimal) -> Benefit:
    """Return the employer-paid London housing as a benefit in kind.

    EIM11431 charges the greater of the annual value and the rent paid by
    the person providing the accommodation; the annual value is assumed not
    higher than the rent, so the rent is the taxable amount.
    """
    annual_rent = rent_per_month * MONTHS_PER_YEAR
    return Benefit(
        name="Housing in London",
        cost=annual_rent,
        tag=TAXABLE_BENEFIT_IN_KIND,
        taxable_amount=annual_rent,
        note="Annual rent paid by the employer to the landlord; the annual value is assumed not higher than the rent.",
        source_key="living_accommodation",
    )


def removal_benefit_rows(
    name: str,
    cost: Decimal,
    exemption_left: Decimal,
    exempt_note: str,
    exempt_source_key: str,
) -> tuple[list[Benefit], Decimal]:
    """Split a qualifying removal cost across the shared £8,000 exemption.

    Returns the benefit rows plus the exemption still available for the next
    removal cost. A cost that is partly exempt becomes two rows, told apart
    by the suffix in the name; a fully covered cost keeps its plain name.
    Any part above the exemption is a taxable benefit in kind.
    """
    exempt = min(cost, exemption_left)
    excess = cost - exempt
    rows = []
    if exempt > 0:
        within_name = name if excess == 0 else f"{name} (within £8,000 relocation exemption)"
        rows.append(
            Benefit(within_name, exempt, NOT_TAXABLE, ZERO, exempt_note, exempt_source_key)
        )
    if excess > 0:
        rows.append(
            Benefit(
                f"{name} (above £8,000 relocation exemption)",
                excess,
                TAXABLE_BENEFIT_IN_KIND,
                excess,
                "Costs above the £8,000 relocation exemption; reportable on form P11D.",
                "relocation_excess",
            )
        )
    return rows, exemption_left - exempt


def assignment_benefits(
    year: int,
    housing_per_month: Decimal,
    relocation_allowance_gbp: Decimal,
    moving_costs: Decimal,
    temporary_housing: Decimal,
) -> list[Benefit]:
    """Return the UK benefits for one assignment year, in presentation order.

    Housing applies in every year. The relocation items are year 1 only:
    moving costs and temporary housing share the £8,000 removal exemption
    (applied in that order), and the relocation allowance is taxable cash
    because a flat-rate allowance has no place inside the exemption.
    Zero-value rows are left out.
    """
    benefit_rows = []
    if housing_per_month > 0:
        benefit_rows.append(housing_benefit(housing_per_month))
    if year == 1:
        exemption_left = REMOVAL_EXEMPTION_LIMIT
        rows, exemption_left = removal_benefit_rows(
            "Moving costs",
            moving_costs,
            exemption_left,
            exempt_note="Qualifying removal costs for the move to the UK, inside the £8,000 exemption.",
            exempt_source_key="relocation_exemption",
        )
        benefit_rows.extend(rows)
        rows, _ = removal_benefit_rows(
            "Temporary housing",
            temporary_housing,
            exemption_left,
            exempt_note="Temporary accommodation before permanent housing, counted against the £8,000 exemption at cost to the employer.",
            exempt_source_key="temporary_living_accommodation",
        )
        benefit_rows.extend(rows)
        if relocation_allowance_gbp > 0:
            benefit_rows.append(
                Benefit(
                    name="Relocation allowance",
                    cost=relocation_allowance_gbp,
                    tag=TAXABLE_CASH,
                    taxable_amount=relocation_allowance_gbp,
                    note="Cash allowance paid to the employee; flat-rate relocation allowances are taxed through PAYE.",
                    source_key="flat_rate_relocation_allowance",
                )
            )
    return benefit_rows
