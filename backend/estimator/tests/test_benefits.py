"""Tests for the UK tax treatment of the assignment benefits."""

from decimal import ROUND_HALF_UP, Decimal

from django.test import SimpleTestCase

from estimator.benefits import (
    NOT_TAXABLE,
    REMOVAL_EXEMPTION_LIMIT,
    TAXABLE_BENEFIT_IN_KIND,
    TAXABLE_CASH,
    assignment_benefits,
)

PENNY = Decimal("0.01")


def pennies(amount: Decimal) -> Decimal:
    return amount.quantize(PENNY, rounding=ROUND_HALF_UP)


def year_one_rows() -> list:
    # The brief's test case: £3,000 housing, CHF 5,000 allowance at 1.10,
    # £6,000 moving costs and £4,000 temporary housing.
    return assignment_benefits(
        year=1,
        housing_per_month=Decimal("3000"),
        relocation_allowance_gbp=Decimal("5000") / Decimal("1.10"),
        moving_costs=Decimal("6000"),
        temporary_housing=Decimal("4000"),
    )


class BenefitTagTests(SimpleTestCase):
    def test_tag_wording_matches_the_contract(self):
        # The frontend matches on these exact strings.
        self.assertEqual(TAXABLE_CASH, "Taxable cash")
        self.assertEqual(TAXABLE_BENEFIT_IN_KIND, "Taxable benefit in kind")
        self.assertEqual(NOT_TAXABLE, "Not taxable in the UK")
        self.assertEqual(REMOVAL_EXEMPTION_LIMIT, Decimal("8000"))


class YearOneBenefitTests(SimpleTestCase):
    def test_rows_come_out_in_presentation_order(self):
        self.assertEqual(
            [row.name for row in year_one_rows()],
            [
                "Housing in London",
                "Moving costs",
                "Temporary housing (within £8,000 relocation exemption)",
                "Temporary housing (above £8,000 relocation exemption)",
                "Relocation allowance",
            ],
        )

    def test_rows_carry_one_tag_each(self):
        self.assertEqual(
            [row.tag for row in year_one_rows()],
            [
                TAXABLE_BENEFIT_IN_KIND,
                NOT_TAXABLE,
                NOT_TAXABLE,
                TAXABLE_BENEFIT_IN_KIND,
                TAXABLE_CASH,
            ],
        )

    def test_housing_is_taxed_on_the_annual_rent(self):
        housing = year_one_rows()[0]
        self.assertEqual(housing.cost, Decimal("36000"))
        self.assertEqual(housing.taxable_amount, Decimal("36000"))

    def test_moving_costs_fit_inside_the_exemption(self):
        moving = year_one_rows()[1]
        self.assertEqual(moving.cost, Decimal("6000"))
        self.assertEqual(moving.taxable_amount, Decimal("0"))

    def test_temporary_housing_is_split_at_the_exemption_limit(self):
        # Moving costs used £6,000 of the £8,000, so only £2,000 of the
        # £4,000 temporary housing stays exempt.
        within, above = year_one_rows()[2:4]
        self.assertEqual(within.cost, Decimal("2000"))
        self.assertEqual(within.taxable_amount, Decimal("0"))
        self.assertEqual(above.cost, Decimal("2000"))
        self.assertEqual(above.taxable_amount, Decimal("2000"))

    def test_relocation_allowance_is_taxable_cash(self):
        allowance = year_one_rows()[4]
        self.assertEqual(allowance.tag, TAXABLE_CASH)
        self.assertEqual(pennies(allowance.cost), Decimal("4545.45"))
        self.assertEqual(allowance.taxable_amount, allowance.cost)

    def test_taxable_total_is_42545_45(self):
        total = sum((row.taxable_amount for row in year_one_rows()), Decimal("0"))
        self.assertEqual(pennies(total), Decimal("42545.45"))


class YearTwoBenefitTests(SimpleTestCase):
    def test_year_two_has_housing_only(self):
        rows = assignment_benefits(
            year=2,
            housing_per_month=Decimal("3000"),
            relocation_allowance_gbp=Decimal("5000"),
            moving_costs=Decimal("6000"),
            temporary_housing=Decimal("4000"),
        )
        self.assertEqual([row.name for row in rows], ["Housing in London"])
        self.assertEqual(rows[0].cost, Decimal("36000"))
        self.assertEqual(rows[0].tag, TAXABLE_BENEFIT_IN_KIND)


class SmallRemovalCostTests(SimpleTestCase):
    def test_removals_inside_the_limit_stay_tax_free(self):
        # £3,000 + £4,000 is within the £8,000 exemption, so no taxable row.
        rows = assignment_benefits(
            year=1,
            housing_per_month=Decimal("3000"),
            relocation_allowance_gbp=Decimal("0"),
            moving_costs=Decimal("3000"),
            temporary_housing=Decimal("4000"),
        )
        self.assertEqual(
            [row.name for row in rows], ["Housing in London", "Moving costs", "Temporary housing"]
        )
        taxable = sum((row.taxable_amount for row in rows), Decimal("0"))
        self.assertEqual(taxable, Decimal("36000"))
