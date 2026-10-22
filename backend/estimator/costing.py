"""Two-year employer cost of the Switzerland to UK secondment.

The steps follow the brief: convert the home pay, work out the hypothetical
Swiss deductions, add the UK benefits, solve the tax-on-tax gross-up, then
total the employer cost. The figures and their sources are in
docs/decision-ledger.md, sections B and C. Amounts stay unrounded Decimals;
rounding to pence happens only when the response is built (views.to_json).
"""

from dataclasses import dataclass
from decimal import Decimal

from . import benefits, swiss_tax, uk_tax

# The assignment is fixed: two UK tax years, and year 1 carries the
# one-off relocation items.
YEARS = [(1, "Year 1 (2026/27)"), (2, "Year 2 (2027/28)")]

SOURCES = {
    "secondment_not_local_hire": {
        "label": "EIM11820: the UK host is treated as the employer for PAYE (GOV.UK)",
        "url": "https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim11820",
    },
    "social_security_convention": {
        "label": "UK/Switzerland Convention on social security coordination, Art. 14(1)",
        "url": "https://assets.publishing.service.gov.uk/media/61543391d3bf7f718a54c14c/CS_Swiss_4.2021_UK_Swiss_Social_Security_Coordination.pdf",
    },
    "social_security_convention_in_force": {
        "label": "UK/Switzerland Convention on social security coordination, in force 1 Oct 2023 (GOV.UK)",
        "url": "https://www.gov.uk/government/publications/ukswitzerland-convention-on-social-security-coordination-cs-switzerland-no42021",
    },
    "social_security_guidance": {
        "label": "Social security contributions for workers coming to the UK from the EEA or Switzerland (GOV.UK)",
        "url": "https://www.gov.uk/guidance/social-security-contributions-for-workers-coming-to-the-uk-from-the-eea-or-switzerland",
    },
    "prior_swiss_insurance": {
        "label": "JAC Advisory Decision 02/2025: prior insurance needed for Art. 14(1)",
        "url": "https://assets.publishing.service.gov.uk/media/6978805bf909df76c5e71f89/JAC-advisory-decision-02-2025.pdf",
    },
    "posting_certificate": {
        "label": "Posting workers to the UK: Swiss Federal Social Insurance Office (BSV)",
        "url": "https://www.bsv.admin.ch/de/entsandte",
    },
    "employer_national_insurance": {
        "label": "NIM16403: no Class 1A NICs where the worker is exempt under the convention (GOV.UK)",
        "url": "https://www.gov.uk/hmrc-internal-manuals/national-insurance-manual/nim16403",
    },
    "apprenticeship_levy": {
        "label": "Pay Apprenticeship Levy: the pay bill excludes workers outside UK NICs legislation (GOV.UK)",
        "url": "https://www.gov.uk/guidance/pay-apprenticeship-levy",
    },
    "workplace_pension": {
        "label": "TPR detailed guidance no. 3, para 47: seconded workers (The Pensions Regulator)",
        "url": "https://www.thepensionsregulator.gov.uk/en/document-library/automatic-enrolment-detailed-guidance/3-assessing-the-workforce",
    },
    "insurance_premium_deduction": {
        "label": "Federal insurance-premium deduction, maximum without pillar 2/3a (ESTV merkblatt)",
        "url": "https://www.estv2.admin.ch/stp/sm/2024/versicherungspraemien-zinsen-de-fr.pdf",
    },
    "sponsor_licence": {
        "label": "Apply for a sponsor licence: £1,682 for a medium or large sponsor (GOV.UK)",
        "url": "https://www.gov.uk/uk-visa-sponsorship-employers/apply-for-your-licence",
    },
}


@dataclass(frozen=True)
class AssignmentInputs:
    """The user's inputs, named as in the API request."""

    home_country: str
    host_country: str
    base_salary_chf: Decimal
    bonus_chf: Decimal
    exchange_rate_chf_per_gbp: Decimal
    housing_gbp_per_month: Decimal
    relocation_allowance_chf: Decimal
    moving_costs_gbp: Decimal
    temporary_housing_gbp: Decimal


def home_pay(inputs: AssignmentInputs) -> dict:
    """Step 1: the home pay converted to GBP, as if the employee had stayed."""
    rate = inputs.exchange_rate_chf_per_gbp
    salary = inputs.base_salary_chf / rate
    bonus = inputs.bonus_chf / rate
    return {"salary": salary, "bonus": bonus, "total": salary + bonus}


def swiss_deductions(swiss: swiss_tax.SwissTaxResult, rate: Decimal) -> dict:
    """Step 2: the hypothetical Swiss tax and social security, in GBP."""
    tax = swiss.total_tax / rate
    social_security = swiss.social_security.total / rate
    return {
        "hypothetical_swiss_tax": tax,
        "hypothetical_swiss_social_security": social_security,
        "total": tax + social_security,
        "sources": {
            "hypothetical_swiss_tax": [
                swiss_tax.SOURCES[key]
                for key in (
                    "federal_tariff_2026",
                    "zurich_tariff_and_deductions_2026",
                    "canton_multiplier",
                    "city_multiplier",
                    "personal_tax",
                    "federal_professional_expenses",
                    "federal_insurance_premiums",
                )
            ],
            "hypothetical_swiss_social_security": [
                swiss_tax.SOURCES[key]
                for key in ("ahv_iv_eo_rate", "alv_rate_and_ceiling", "social_security_rates_2026")
            ],
        },
    }


def net_home_pay(swiss: swiss_tax.SwissTaxResult, rate: Decimal) -> Decimal:
    """Step 3: the home pay after the hypothetical Swiss deductions, in GBP."""
    net_chf = swiss.gross_salary - swiss.total_tax - swiss.social_security.total
    return net_chf / rate


def employer_charges() -> list[dict]:
    """Step 5: UK employer charges, all zero for a secondee under the convention."""
    return [
        {
            "name": "Employer National Insurance",
            "amount": Decimal("0"),
            "reason": "Swiss social security applies for the whole posting, so no UK Class 1 or Class 1A National Insurance is due.",
            "source": SOURCES["employer_national_insurance"],
        },
        {
            "name": "Apprenticeship Levy",
            "amount": Decimal("0"),
            "reason": "The levy pay bill excludes earnings of employees who are not subject to UK National Insurance contributions legislation.",
            "source": SOURCES["apprenticeship_levy"],
        },
        {
            "name": "Workplace pension auto-enrolment",
            "amount": Decimal("0"),
            "reason": "The employment contract remains with the Swiss employer, so the secondee is unlikely to be ordinarily working in the UK.",
            "source": SOURCES["workplace_pension"],
        },
    ]


def benefit_as_dict(benefit: benefits.Benefit) -> dict:
    """Convert a benefit row into the API contract's benefit object."""
    return {
        "name": benefit.name,
        "cost": benefit.cost,
        "tag": benefit.tag,
        "taxable_amount": benefit.taxable_amount,
        "note": benefit.note,
        "source": benefits.SOURCES[benefit.source_key],
    }


def multiple_of_home_pay(total: Decimal, home_pay_total: Decimal) -> Decimal:
    """The total cost as a multiple of the home pay (0 when home pay is 0)."""
    if home_pay_total == 0:
        return Decimal("0")
    return total / home_pay_total


def estimate_year(
    year: int, label: str, inputs: AssignmentInputs, swiss: swiss_tax.SwissTaxResult
) -> dict:
    """Cost one assignment year and return it in the API response shape."""
    rate = inputs.exchange_rate_chf_per_gbp
    pay = home_pay(inputs)
    deductions = swiss_deductions(swiss, rate)
    net_pay = net_home_pay(swiss, rate)

    # Step 4: the benefits, with the relocation allowance converted to GBP.
    # I = net home pay + taxable benefits: the employer pays the UK tax on
    # top of both, and that payment is itself taxable (the tax-on-tax).
    benefit_rows = benefits.assignment_benefits(
        year,
        housing_per_month=inputs.housing_gbp_per_month,
        relocation_allowance_gbp=inputs.relocation_allowance_chf / rate,
        moving_costs=inputs.moving_costs_gbp,
        temporary_housing=inputs.temporary_housing_gbp,
    )
    benefits_cost = sum((row.cost for row in benefit_rows), Decimal("0"))
    taxable_benefits = sum((row.taxable_amount for row in benefit_rows), Decimal("0"))
    taxable_pay = net_pay + taxable_benefits

    # Step 5: solve the tax-on-tax fixed point, then show how the final tax
    # splits across the rate bands on the total that includes the tax.
    gross_up = uk_tax.gross_up_tax(taxable_pay)
    tax_bands = uk_tax.income_tax_bands(taxable_pay + gross_up.tax)

    # Step 6: the employer pays home pay, all benefit costs and the UK tax,
    # and saves the hypothetical Swiss deductions.
    total = pay["total"] + benefits_cost + gross_up.tax - deductions["total"]
    return {
        "label": label,
        "home_pay": pay,
        "benefits": [benefit_as_dict(row) for row in benefit_rows],
        "benefits_total_cost": benefits_cost,
        "taxable_benefits_total": taxable_benefits,
        "host_tax": {
            "taxable_pay_before_tax": taxable_pay,
            "uk_income_tax": gross_up.tax,
            "iterations": list(gross_up.iterations),
            "tax_bands": tax_bands,
            "employer_charges": employer_charges(),
            "total": gross_up.tax,
            "sources": list(uk_tax.SOURCES.values()),
        },
        "deductions": deductions,
        "total_employer_cost": total,
        "multiple_of_home_pay": multiple_of_home_pay(total, pay["total"]),
    }


def assignment_total(years: list[dict]) -> dict:
    """Both years added up, set against the total home pay."""
    total = sum((year["total_employer_cost"] for year in years), Decimal("0"))
    home_pay_total = sum((year["home_pay"]["total"] for year in years), Decimal("0"))
    return {
        "total_employer_cost": total,
        "home_pay": home_pay_total,
        "multiple_of_home_pay": multiple_of_home_pay(total, home_pay_total),
    }


def swiss_working(swiss: swiss_tax.SwissTaxResult) -> dict:
    """The full hypothetical Swiss tax working, in CHF, for the UI."""
    return {
        "gross_salary_chf": swiss.gross_salary,
        "ahv_iv_eo_chf": swiss.social_security.ahv_iv_eo,
        "alv_chf": swiss.social_security.alv,
        "social_security_total_chf": swiss.social_security.total,
        "net_salary_chf": swiss.net_salary,
        "professional_expenses_chf": swiss.professional_expenses,
        "federal_insurance_deduction_chf": swiss_tax.FEDERAL_INSURANCE_DEDUCTION,
        "zurich_insurance_deduction_chf": swiss_tax.ZURICH_INSURANCE_DEDUCTION,
        "federal_taxable_income_chf": swiss.federal_taxable_income,
        "zurich_taxable_income_chf": swiss.zurich_taxable_income,
        "federal_tax_chf": swiss.federal_tax,
        "zurich_simple_tax_chf": swiss.zurich_simple_tax,
        "cantonal_tax_chf": swiss.cantonal_tax,
        "communal_tax_chf": swiss.communal_tax,
        "personal_tax_chf": swiss.personal_tax,
        "total_tax_chf": swiss.total_tax,
    }


def social_security_statement() -> dict:
    """Why Swiss social security applies and no UK National Insurance is due."""
    return {
        "applies": "Switzerland",
        "rule": (
            "Under Article 14(1) of the UK–Switzerland social security convention, an "
            "employee posted from Switzerland to the UK stays in the Swiss system when "
            "the employment contract with the Swiss company continues, the posting is "
            "expected to last no more than 24 months, and the employee is not sent to "
            "replace another posted worker. The Swiss employer obtains the posting "
            "certificate from its AHV compensation office as evidence; no UK National "
            "Insurance is then due."
        ),
        "sources": [
            SOURCES["social_security_convention"],
            SOURCES["social_security_convention_in_force"],
            SOURCES["social_security_guidance"],
            SOURCES["employer_national_insurance"],
            SOURCES["prior_swiss_insurance"],
            SOURCES["posting_certificate"],
        ],
    }


def assumptions(swiss: swiss_tax.SwissTaxResult) -> list[dict]:
    """The standing assumptions shown with the estimate (ledger section E)."""
    # The Swiss employer pays the same AHV/IV/EO and ALV rates as the employee.
    employer_contributions = swiss.social_security.total
    return [
        {
            "text": "The employee stays employed by the Swiss company for the whole assignment; the UK subsidiary is only the host (a secondment, not a local hire).",
            "source": SOURCES["secondment_not_local_hire"],
        },
        {
            "text": "Swiss social security keeps applying because the posting lasts no more than 24 months and the employee does not replace another posted worker; the Swiss posting certificate is assumed to be issued.",
            "source": SOURCES["social_security_convention"],
        },
        {
            "text": "No occupational pension (BVG) and no pillar 3a contributions are deducted; insurance-premium deductions are taken at the statutory maximum, and non-occupational accident insurance is left out.",
            "source": SOURCES["insurance_premium_deduction"],
        },
        {
            "text": "The Swiss 2026 tariffs and the Zurich multipliers are carried into the second year, because the 2027 values are not yet published.",
            "source": swiss_tax.SOURCES["canton_multiplier"],
        },
        {
            "text": "UK 2026/27 rates are used for both years, at the England rates (the employee lives in London).",
            "source": uk_tax.SOURCES["tax_bands_2026_27"],
        },
        {
            "text": "The annual value of the London housing is assumed not higher than the rent paid, and temporary-workplace relief is not claimed because London is the main residence for the posting.",
            "source": benefits.SOURCES["living_accommodation"],
        },
        {
            "text": "The relocation allowance is treated as taxable cash, not as reimbursement of qualifying removal costs.",
            "source": benefits.SOURCES["flat_rate_relocation_allowance"],
        },
        {
            "text": f"The Swiss employer's own social security contributions (CHF {employer_contributions:,.2f} a year) are not added to the total, because the employer would bear them without the assignment too.",
            "source": swiss_tax.SOURCES["social_security_rates_2026"],
        },
        {
            "text": "UK workplace pension auto-enrolment does not apply, because the employment contract remains with the Swiss employer.",
            "source": SOURCES["workplace_pension"],
        },
        {
            "text": "The UK sponsor is medium or large and needs a sponsor licence; the immigration costs are shown separately.",
            "source": SOURCES["sponsor_licence"],
        },
        {
            "text": "The figures are estimates for planning the assignment, not tax advice.",
            "source": None,
        },
    ]


def all_sources() -> dict:
    """Every source used anywhere in the estimate, keyed for the UI."""
    return {**uk_tax.SOURCES, **swiss_tax.SOURCES, **benefits.SOURCES, **SOURCES}


def estimate_assignment_cost(inputs: AssignmentInputs) -> dict:
    """Cost the fixed two-year assignment, in the API response shape.

    All money stays as unrounded Decimals; the view rounds for display.
    """
    swiss = swiss_tax.hypothetical_swiss_tax(inputs.base_salary_chf + inputs.bonus_chf)
    years = [estimate_year(year, label, inputs, swiss) for year, label in YEARS]
    return {
        "years": years,
        "assignment_total": assignment_total(years),
        "swiss_working": swiss_working(swiss),
        "social_security": social_security_statement(),
        "assumptions": assumptions(swiss),
        "sources": all_sources(),
    }
