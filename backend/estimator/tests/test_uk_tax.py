"""Tests for the UK income tax and tax-on-tax gross-up maths."""

from decimal import ROUND_HALF_UP, Decimal

from django.test import SimpleTestCase

from estimator.uk_tax import gross_up_tax, income_tax, personal_allowance

PENNY = Decimal("0.01")


class PersonalAllowanceTests(SimpleTestCase):
    def test_full_allowance_below_taper(self):
        self.assertEqual(personal_allowance(Decimal("50000")), Decimal("12570"))

    def test_allowance_untouched_at_taper_start(self):
        self.assertEqual(personal_allowance(Decimal("100000")), Decimal("12570"))

    def test_allowance_tapers_one_for_two_above_100k(self):
        # £10,000 above the taper start: allowance drops by £5,000.
        self.assertEqual(personal_allowance(Decimal("110000")), Decimal("7570"))

    def test_allowance_is_exactly_zero_at_125140(self):
        self.assertEqual(personal_allowance(Decimal("125140")), Decimal("0"))

    def test_allowance_stays_zero_above_125140(self):
        self.assertEqual(personal_allowance(Decimal("200000")), Decimal("0"))


class IncomeTaxTests(SimpleTestCase):
    def test_no_tax_at_the_personal_allowance(self):
        self.assertEqual(income_tax(Decimal("12570")), Decimal("0"))

    def test_top_of_the_basic_rate_band(self):
        # Taxable £37,700 at 20%.
        self.assertEqual(income_tax(Decimal("50270")), Decimal("7540"))

    def test_tax_at_100000_includes_the_tapered_allowance(self):
        # Full allowance still applies at £100,000: taxable £87,430,
        # so 7,540 + 0.40 x 49,730.
        self.assertEqual(income_tax(Decimal("100000")), Decimal("27432"))

    def test_tax_at_125140_where_the_allowance_is_gone(self):
        # Taxable £125,140: 7,540 + 0.40 x 87,440.
        self.assertEqual(income_tax(Decimal("125140")), Decimal("42516"))

    def test_additional_rate_kicks_in_above_125140(self):
        # 42,516 + 0.45 x (200,000 - 125,140).
        self.assertEqual(income_tax(Decimal("200000")), Decimal("76203"))


class GrossUpTests(SimpleTestCase):
    # Assignment test case (docs/decision-ledger.md, section C): I is the net
    # home pay after hypothetical deductions plus the taxable benefits.

    def test_year_one_case_rounds_to_the_expected_figure(self):
        result = gross_up_tax(Decimal("158846.68181818"))
        self.assertEqual(
            result.tax.quantize(PENNY, rounding=ROUND_HALF_UP),
            Decimal("104880.01"),
        )

    def test_year_one_case_satisfies_the_fixed_point(self):
        # The definition of the answer: taxing pay + T must give back T.
        pay = Decimal("158846.68181818")
        result = gross_up_tax(pay)
        residual = abs(income_tax(pay + result.tax) - result.tax)
        self.assertLess(residual, Decimal("0.00001"))

    def test_year_two_case_rounds_to_the_expected_figure(self):
        result = gross_up_tax(Decimal("152301.22727273"))
        self.assertEqual(
            result.tax.quantize(PENNY, rounding=ROUND_HALF_UP),
            Decimal("99524.64"),
        )

    def test_zero_pay_needs_no_tax(self):
        result = gross_up_tax(Decimal("0"))
        self.assertEqual(result.tax, Decimal("0"))

    def test_iterations_record_the_working(self):
        result = gross_up_tax(Decimal("158846.68181818"))
        self.assertTrue(result.iterations)
        self.assertEqual(result.iterations[-1], result.tax)
