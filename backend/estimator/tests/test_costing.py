"""Tests for the two-year costing, against the ledger's section C figures."""

from decimal import ROUND_HALF_UP, Decimal

from django.test import SimpleTestCase

from estimator.costing import AssignmentInputs, estimate_assignment_cost
from estimator.uk_tax import income_tax

PENNY = Decimal("0.01")


def pennies(amount: Decimal) -> Decimal:
    return amount.quantize(PENNY, rounding=ROUND_HALF_UP)


def test_case_inputs() -> AssignmentInputs:
    return AssignmentInputs(
        home_country="CH",
        host_country="GB",
        base_salary_chf=Decimal("150000"),
        bonus_chf=Decimal("20000"),
        exchange_rate_chf_per_gbp=Decimal("1.10"),
        housing_gbp_per_month=Decimal("3000"),
        relocation_allowance_chf=Decimal("5000"),
        moving_costs_gbp=Decimal("6000"),
        temporary_housing_gbp=Decimal("4000"),
    )


class AssignmentCostTests(SimpleTestCase):
    def setUp(self):
        self.result = estimate_assignment_cost(test_case_inputs())
        self.year_one = self.result["years"][0]
        self.year_two = self.result["years"][1]

    def test_year_one_figures_match_the_ledger(self):
        self.assertEqual(self.year_one["label"], "Year 1 (2026/27)")
        self.assertEqual(pennies(self.year_one["host_tax"]["taxable_pay_before_tax"]), Decimal("158846.68"))
        self.assertEqual(pennies(self.year_one["host_tax"]["uk_income_tax"]), Decimal("104880.01"))
        self.assertEqual(pennies(self.year_one["total_employer_cost"]), Decimal("271726.69"))
        self.assertEqual(pennies(self.year_one["multiple_of_home_pay"]), Decimal("1.76"))

    def test_year_one_benefit_totals_match_the_ledger(self):
        # Housing 36,000 + moving 6,000 + temporary 4,000 + allowance 4,545.45.
        self.assertEqual(pennies(self.year_one["benefits_total_cost"]), Decimal("50545.45"))
        # Housing 36,000 + excess temporary 2,000 + allowance 4,545.45.
        self.assertEqual(pennies(self.year_one["taxable_benefits_total"]), Decimal("42545.45"))

    def test_year_one_deductions_match_the_ledger(self):
        deductions = self.year_one["deductions"]
        self.assertEqual(pennies(deductions["hypothetical_swiss_tax"]), Decimal("28571.32"))
        self.assertEqual(
            pennies(deductions["hypothetical_swiss_social_security"]), Decimal("9672.91")
        )
        self.assertEqual(pennies(deductions["total"]), Decimal("38244.23"))

    def test_year_one_gross_up_reaches_the_fixed_point(self):
        taxable_pay = self.year_one["host_tax"]["taxable_pay_before_tax"]
        tax = self.year_one["host_tax"]["uk_income_tax"]
        self.assertLess(abs(income_tax(taxable_pay + tax) - tax), Decimal("0.00001"))

    def test_year_one_employer_charges_are_all_zero(self):
        charges = self.year_one["host_tax"]["employer_charges"]
        self.assertEqual(
            [charge["name"] for charge in charges],
            ["Employer National Insurance", "Apprenticeship Levy", "Workplace pension auto-enrolment"],
        )
        self.assertTrue(all(charge["amount"] == 0 for charge in charges))

    def test_year_two_figures_match_the_ledger(self):
        self.assertEqual(self.year_two["label"], "Year 2 (2027/28)")
        self.assertEqual(pennies(self.year_two["host_tax"]["taxable_pay_before_tax"]), Decimal("152301.23"))
        self.assertEqual(pennies(self.year_two["host_tax"]["uk_income_tax"]), Decimal("99524.64"))
        self.assertEqual(pennies(self.year_two["total_employer_cost"]), Decimal("251825.87"))
        self.assertEqual(pennies(self.year_two["multiple_of_home_pay"]), Decimal("1.63"))

    def test_year_two_has_housing_as_its_only_benefit(self):
        self.assertEqual(
            [row["name"] for row in self.year_two["benefits"]], ["Housing in London"]
        )
        self.assertEqual(pennies(self.year_two["benefits_total_cost"]), Decimal("36000"))

    def test_assignment_total_sums_both_years(self):
        total = self.result["assignment_total"]
        self.assertEqual(pennies(total["total_employer_cost"]), Decimal("523552.56"))
        self.assertEqual(pennies(total["home_pay"]), Decimal("309090.91"))
        self.assertEqual(pennies(total["multiple_of_home_pay"]), Decimal("1.69"))

    def test_swiss_working_shows_the_chf_figures(self):
        swiss = self.result["swiss_working"]
        self.assertEqual(pennies(swiss["gross_salary_chf"]), Decimal("170000.00"))
        self.assertEqual(pennies(swiss["total_tax_chf"]), Decimal("31428.45"))
        self.assertEqual(pennies(swiss["social_security_total_chf"]), Decimal("10640.20"))

    def test_social_security_statement_applies_to_switzerland(self):
        statement = self.result["social_security"]
        self.assertEqual(statement["applies"], "Switzerland")
        self.assertTrue(statement["sources"])

    def test_eleven_assumptions_are_listed(self):
        self.assertEqual(len(self.result["assumptions"]), 11)

    def test_sources_merge_every_module(self):
        sources = self.result["sources"]
        self.assertIn("tax_bands_2026_27", sources)  # uk_tax
        self.assertIn("federal_tariff_2026", sources)  # swiss_tax
        self.assertIn("living_accommodation", sources)  # benefits
        self.assertIn("employer_national_insurance", sources)  # costing
