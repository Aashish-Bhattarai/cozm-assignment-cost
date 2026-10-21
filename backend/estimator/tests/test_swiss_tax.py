"""Tests for the hypothetical Swiss tax and social security module."""

from decimal import Decimal

from django.test import SimpleTestCase

from estimator.swiss_tax import (
    federal_income_tax,
    hypothetical_swiss_tax,
    round_down_to_hundred,
    social_security,
    zurich_simple_tax,
)


class SocialSecurityTests(SimpleTestCase):
    def test_170000_alv_ceiling_applies(self):
        ss = social_security(Decimal("170000"))
        self.assertEqual(ss.ahv_iv_eo, Decimal("9010.00"))
        self.assertEqual(ss.alv, Decimal("1630.20"))
        self.assertEqual(ss.total, Decimal("10640.20"))

    def test_100000_below_alv_ceiling(self):
        ss = social_security(Decimal("100000"))
        self.assertEqual(ss.alv, Decimal("1100.00"))


class RoundingTests(SimpleTestCase):
    def test_round_down_to_hundred(self):
        self.assertEqual(round_down_to_hundred(Decimal("152659.80")), Decimal("152600"))


class FederalIncomeTaxTests(SimpleTestCase):
    def test_below_first_band_is_zero(self):
        self.assertEqual(federal_income_tax(Decimal("18000")), Decimal("0"))

    def test_higher_band(self):
        self.assertEqual(federal_income_tax(Decimal("152659.80")), Decimal("7361.55"))

    def test_lower_band(self):
        self.assertEqual(federal_income_tax(Decimal("69933.60")), Decimal("965.43"))

    def test_matches_the_official_table_row_at_79000(self):
        # ESTV table 58c, 2026: 79 000 -> 1 318.82 (1,152.50 + 28 x 5.94).
        self.assertEqual(federal_income_tax(Decimal("79000")), Decimal("1318.82"))

    def test_flat_top_rate(self):
        self.assertEqual(federal_income_tax(Decimal("800000")), Decimal("92000.00"))


class ZurichSimpleTaxTests(SimpleTestCase):
    def test_at_first_slice_boundary(self):
        self.assertEqual(zurich_simple_tax(Decimal("7000")), Decimal("0"))

    def test_high_income(self):
        self.assertEqual(zurich_simple_tax(Decimal("151009.80")), Decimal("11235"))

    def test_middle_income(self):
        self.assertEqual(zurich_simple_tax(Decimal("68283.60")), Decimal("3390"))

    def test_income_reaching_the_12_and_13_percent_slices(self):
        # 16,339 up to 197,400; + 12% of 69,300 = 8,316 up to 266,700;
        # + 13% of the remaining 33,300 = 4,329.
        self.assertEqual(zurich_simple_tax(Decimal("300000")), Decimal("28984"))


class HypotheticalSwissTaxTests(SimpleTestCase):
    def test_assignment_case_170000(self):
        r = hypothetical_swiss_tax(Decimal("170000"))
        self.assertEqual(r.gross_salary, Decimal("170000"))
        self.assertEqual(r.social_security.total, Decimal("10640.20"))
        self.assertEqual(r.net_salary, Decimal("159359.80"))
        self.assertEqual(r.professional_expenses, Decimal("4000"))
        self.assertEqual(r.federal_taxable_income, Decimal("152659.80"))
        self.assertEqual(r.zurich_taxable_income, Decimal("151009.80"))
        self.assertEqual(r.federal_tax, Decimal("7361.55"))
        self.assertEqual(r.zurich_simple_tax, Decimal("11235"))
        self.assertEqual(r.cantonal_tax, Decimal("10673.25"))
        self.assertEqual(r.communal_tax, Decimal("13369.65"))
        self.assertEqual(r.personal_tax, Decimal("24"))
        self.assertEqual(r.total_tax, Decimal("31428.45"))

    def test_80000(self):
        self.assertEqual(
            hypothetical_swiss_tax(Decimal("80000")).total_tax, Decimal("8244.03")
        )

    def test_120000(self):
        self.assertEqual(
            hypothetical_swiss_tax(Decimal("120000")).total_tax, Decimal("17207.31")
        )

    def test_30000(self):
        self.assertEqual(
            hypothetical_swiss_tax(Decimal("30000")).total_tax, Decimal("1027.97")
        )

    def test_professional_expenses_minimum(self):
        r = hypothetical_swiss_tax(Decimal("30000"))
        self.assertEqual(r.professional_expenses, Decimal("2000"))

    def test_professional_expenses_maximum(self):
        r = hypothetical_swiss_tax(Decimal("170000"))
        self.assertEqual(r.professional_expenses, Decimal("4000"))

    def test_very_small_salary_never_gives_negative_taxable_income(self):
        r = hypothetical_swiss_tax(Decimal("3000"))
        self.assertEqual(r.federal_taxable_income, Decimal("0"))
        self.assertEqual(r.zurich_taxable_income, Decimal("0"))
        # Only the flat personal tax remains, which every resident pays.
        self.assertEqual(r.total_tax, Decimal("24"))
