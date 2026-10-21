"""Hypothetical Swiss tax and social security for the 2026 tax year.

Estimates what a SINGLE person living in the city of Zurich would pay on a
gross salary: employee social security contributions (AHV/IV/EO and ALV)
plus federal, cantonal and communal income tax. Deliberately simplified:
no church tax, no occupational pension (BVG), no pillar 3a, no NBU.
"""

from dataclasses import dataclass
from decimal import Decimal

# --- Employee social security, 2026 ------------------------------------------

AHV_IV_EO_RATE = Decimal("0.053")  # 5.3%, no salary ceiling
ALV_RATE = Decimal("0.011")  # 1.1%, up to a salary ceiling
ALV_SALARY_CEILING = Decimal("148200")

# --- Deductions ---------------------------------------------------------------

# Professional expenses: 3% of net salary, clamped to [2000, 4000].
PROFESSIONAL_EXPENSES_RATE = Decimal("0.03")
PROFESSIONAL_EXPENSES_MIN = Decimal("2000")
PROFESSIONAL_EXPENSES_MAX = Decimal("4000")

# Maximum insurance-premium deduction for a single person. No pillar 2/3a
# contributions are deducted because this model leaves both out.
FEDERAL_INSURANCE_DEDUCTION = Decimal("2700")
ZURICH_INSURANCE_DEDUCTION = Decimal("4350")  # 2900 x 1.5

# --- Federal tariff 2026, single persons --------------------------------------
# (band_start, tax at band_start, tax per extra 100). Below 18,500: no tax.
FEDERAL_BANDS = [
    (Decimal("18500"), Decimal("25.41"), Decimal("0.77")),
    (Decimal("33200"), Decimal("138.60"), Decimal("0.88")),
    (Decimal("43500"), Decimal("229.20"), Decimal("2.64")),
    (Decimal("58000"), Decimal("612.00"), Decimal("2.97")),
    (Decimal("76200"), Decimal("1152.50"), Decimal("5.94")),
    (Decimal("82100"), Decimal("1502.95"), Decimal("6.60")),
    (Decimal("108900"), Decimal("3271.75"), Decimal("8.80")),
    (Decimal("141500"), Decimal("6140.55"), Decimal("11.00")),
    (Decimal("185100"), Decimal("10936.55"), Decimal("13.20")),
]
# Above this the whole taxable income is taxed at a flat 11.5%.
FEDERAL_TOP_RATE = Decimal("0.115")
FEDERAL_TOP_RATE_FROM = Decimal("794000")

# --- Zurich tariff 2026 (Grundtarif, single): (slice width or None, rate %) ---
ZURICH_SLICES = [
    (Decimal("7000"), Decimal("0")),
    (Decimal("5000"), Decimal("2")),
    (Decimal("4800"), Decimal("3")),
    (Decimal("8000"), Decimal("4")),
    (Decimal("9700"), Decimal("5")),
    (Decimal("11200"), Decimal("6")),
    (Decimal("13100"), Decimal("7")),
    (Decimal("17600"), Decimal("8")),
    (Decimal("34000"), Decimal("9")),
    (Decimal("33700"), Decimal("10")),
    (Decimal("53300"), Decimal("11")),
    (Decimal("69300"), Decimal("12")),
    (None, Decimal("13")),
]

CANTON_MULTIPLIER = Decimal("0.95")  # canton of Zurich, 2026
CITY_MULTIPLIER = Decimal("1.19")  # city of Zurich, 2026
PERSONAL_TAX = Decimal("24")  # flat personal tax, city of Zurich

SOURCES = {
    "ahv_iv_eo_rate": {
        "label": "AHV/IV/EO contribution rate 5.3% (AHV leaflet 2.01)",
        "url": "https://www.ahv-iv.ch/p/2.01.d",
    },
    "alv_rate_and_ceiling": {
        "label": "ALV contribution rate and salary ceiling (AHV leaflet 2.08)",
        "url": "https://www.ahv-iv.ch/p/2.08.d",
    },
    "social_security_rates_2026": {
        "label": "Federal Personnel Office payroll table 2026",
        "url": "https://www.epa.admin.ch/dam/de/sd-web/CtDDI6rw-V4N/Lohntabelle%202026.pdf",
    },
    "federal_tariff_2026": {
        "label": "Federal income tax tariff 2026, single persons (ESTV)",
        "url": "https://www.estv.admin.ch/dam/de/sd-web/gnde9CmEsalK/dbst-tairfe-58c-2026-dfi.pdf",
    },
    "federal_deductions_unchanged_2026": {
        "label": "ESTV: general deductions unchanged for 2026",
        "url": "https://www.estv.admin.ch/de/newnsb/VzaAUrhkPx2EPde4a6e3O",
    },
    "federal_professional_expenses": {
        "label": "Federal professional expenses deduction (ESTV merkblatt)",
        "url": "https://www.estv2.admin.ch/stp/sm/2024/berufskosten-de-fr.pdf",
    },
    "federal_insurance_premiums": {
        "label": "Federal insurance-premium deduction (ESTV merkblatt)",
        "url": "https://www.estv2.admin.ch/stp/sm/2024/versicherungspraemien-zinsen-de-fr.pdf",
    },
    "zurich_tariff_and_deductions_2026": {
        "label": "Zurich cantonal tax tariff and deductions 2026 (ESTV)",
        "url": "https://www.estv2.admin.ch/stp/kb/zh-de.pdf",
    },
    "canton_multiplier": {
        "label": "Canton of Zurich tax multiplier 2026 (ZH)",
        "url": "https://www.zh.ch/de/steuern-finanzen/steuern/steuerstatistiken/aktuelle-gemeinde-steuerfuesse.html",
    },
    "city_multiplier": {
        "label": "City of Zurich tax multiplier 2026 (Stadt Zuerich budget 2026)",
        "url": "https://www.stadt-zuerich.ch/de/aktuell/medienmitteilungen/2025/09/str-budget-2026.html",
    },
    "personal_tax": {
        "label": "Zurich personal tax (Personalsteuer, ZH lex 631.1)",
        "url": "https://www.notes.zh.ch/appl/zhlex_r.nsf/WebView/49B30E8052B9D928C125849A00480C6C/$File/631.1_8.6.97_107.pdf",
    },
    "estv_calculator": {
        "label": "ESTV Swiss tax calculator (reference checks)",
        "url": "https://swisstaxcalculator.estv.admin.ch/",
    },
}


@dataclass(frozen=True)
class SocialSecurity:
    """Employee social security contributions on a gross salary."""

    ahv_iv_eo: Decimal
    alv: Decimal
    total: Decimal


@dataclass(frozen=True)
class SwissTaxResult:
    """The hypothetical Swiss tax, with the full working."""

    gross_salary: Decimal
    social_security: SocialSecurity
    net_salary: Decimal
    professional_expenses: Decimal
    federal_taxable_income: Decimal
    zurich_taxable_income: Decimal
    federal_tax: Decimal
    zurich_simple_tax: Decimal
    cantonal_tax: Decimal
    communal_tax: Decimal
    personal_tax: Decimal
    total_tax: Decimal


def social_security(gross_salary: Decimal) -> SocialSecurity:
    """Return the employee AHV/IV/EO and ALV contributions on a gross salary.

    AHV/IV/EO has no ceiling; ALV only applies up to the salary ceiling.
    """
    ahv_iv_eo = gross_salary * AHV_IV_EO_RATE
    alv_salary = min(gross_salary, ALV_SALARY_CEILING)
    alv = alv_salary * ALV_RATE
    return SocialSecurity(ahv_iv_eo=ahv_iv_eo, alv=alv, total=ahv_iv_eo + alv)


def round_down_to_hundred(amount: Decimal) -> Decimal:
    """Round down to a whole CHF 100; both tariffs disregard amounts below 100."""
    return (amount // 100) * 100


def professional_expenses(net_salary: Decimal) -> Decimal:
    """Return the professional-expenses deduction: 3% of net salary, clamped."""
    expenses = net_salary * PROFESSIONAL_EXPENSES_RATE
    return min(max(expenses, PROFESSIONAL_EXPENSES_MIN), PROFESSIONAL_EXPENSES_MAX)


def federal_income_tax(taxable_income: Decimal) -> Decimal:
    """Return the federal income tax for 2026 (unrounded).

    The tariff is progressive: each band adds tax_per_extra_100 per CHF 100
    above the band start. Very high incomes switch to a flat 11.5% of the
    whole taxable income instead of continuing up the bands.
    """
    taxable_income = round_down_to_hundred(taxable_income)
    if taxable_income <= 0:
        return Decimal("0")
    if taxable_income >= FEDERAL_TOP_RATE_FROM:
        return taxable_income * FEDERAL_TOP_RATE
    tax = Decimal("0")
    for band_start, tax_at_start, per_extra_100 in reversed(FEDERAL_BANDS):
        if taxable_income >= band_start:
            tax = tax_at_start + (taxable_income - band_start) / 100 * per_extra_100
            break
    return tax


def zurich_simple_tax(taxable_income: Decimal) -> Decimal:
    """Return the Zurich simple tax (einfache Staatssteuer) for 2026, unrounded.

    The tariff fills successive slices of taxable income, each at its own
    percentage rate; the last slice has no width and covers the rest.
    """
    taxable_income = round_down_to_hundred(taxable_income)
    if taxable_income <= 0:
        return Decimal("0")
    tax = Decimal("0")
    remaining = taxable_income
    for width, rate_percent in ZURICH_SLICES:
        if width is None:
            taxed = remaining
        else:
            taxed = min(remaining, width)
        tax += taxed * rate_percent / 100
        remaining -= taxed
        if remaining <= 0:
            break
    return tax


def hypothetical_swiss_tax(gross_salary: Decimal) -> SwissTaxResult:
    """Return the full hypothetical Swiss tax working for a gross salary.

    gross_salary is salary plus bonus as passed in by the caller. Federal and
    Zurich taxable income differ because the two tariffs allow different
    insurance-premium deductions.
    """
    ss = social_security(gross_salary)
    net_salary = gross_salary - ss.total
    expenses = professional_expenses(net_salary)
    income_after_deductions = net_salary - expenses

    # Deductions can exceed a very small income; taxable income never goes below zero.
    federal_taxable_income = max(income_after_deductions - FEDERAL_INSURANCE_DEDUCTION, Decimal("0"))
    zurich_taxable_income = max(income_after_deductions - ZURICH_INSURANCE_DEDUCTION, Decimal("0"))

    federal_tax = federal_income_tax(federal_taxable_income)
    simple_tax = zurich_simple_tax(zurich_taxable_income)
    cantonal_tax = simple_tax * CANTON_MULTIPLIER
    communal_tax = simple_tax * CITY_MULTIPLIER

    total_tax = federal_tax + cantonal_tax + communal_tax + PERSONAL_TAX
    return SwissTaxResult(
        gross_salary=gross_salary,
        social_security=ss,
        net_salary=net_salary,
        professional_expenses=expenses,
        federal_taxable_income=federal_taxable_income,
        zurich_taxable_income=zurich_taxable_income,
        federal_tax=federal_tax,
        zurich_simple_tax=simple_tax,
        cantonal_tax=cantonal_tax,
        communal_tax=communal_tax,
        personal_tax=PERSONAL_TAX,
        total_tax=total_tax,
    )
