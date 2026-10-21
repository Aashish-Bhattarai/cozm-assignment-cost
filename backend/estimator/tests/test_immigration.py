"""Tests for the immigration costs and requirements module."""

from decimal import Decimal

from django.test import SimpleTestCase

from estimator.immigration import immigration_guidance


def sources_of(entries: list) -> set:
    """The set of source URLs referenced by a list of items, costs or steps."""
    return {entry["source"]["url"] for entry in entries}


class GuidanceTests(SimpleTestCase):
    def test_totals(self):
        self.assertEqual(
            immigration_guidance("medium_large")["total_cost"], Decimal("8253.50")
        )
        self.assertEqual(immigration_guidance("small")["total_cost"], Decimal("5502.50"))

    def test_health_surcharge(self):
        costs = {c["item"]: c for c in immigration_guidance("medium_large")["costs"]}
        self.assertEqual(
            costs["Immigration Health Surcharge"]["amount"], Decimal("2587.50")
        )

    def test_immigration_skills_charge(self):
        for size, expected in [("medium_large", Decimal("2640")), ("small", Decimal("960"))]:
            costs = {c["item"]: c for c in immigration_guidance(size)["costs"]}
            self.assertEqual(
                costs["Immigration Skills Charge"]["amount"], expected, msg=size
            )

    def test_section_titles_and_order(self):
        titles = [s["title"] for s in immigration_guidance("medium_large")["sections"]]
        self.assertEqual(
            titles,
            [
                "Work permit",
                "Business visit before the assignment",
                "Passport",
                "What the company must do",
            ],
        )

    def test_every_item_has_an_https_source(self):
        for size in ["medium_large", "small"]:
            result = immigration_guidance(size)
            for section in result["sections"]:
                self.assertTrue(sources_of(section["items"]), msg=section["title"])
                for url in sources_of(section["items"]):
                    self.assertTrue(url.startswith("https://"), msg=url)
            self.assertTrue(sources_of(result["timeline"]))
            for url in sources_of(result["timeline"]):
                self.assertTrue(url.startswith("https://"), msg=url)

    def test_every_cost_has_payer_note_and_https_source(self):
        for size in ["medium_large", "small"]:
            for cost in immigration_guidance(size)["costs"]:
                self.assertIn(cost["payer"], [
                    "Employee (the employer may reimburse)",
                    "Employee (reimbursable under the UK-Switzerland convention)",
                    "Employer (UK subsidiary)",
                ])
                self.assertTrue(cost["note"])
                self.assertTrue(cost["source"]["url"].startswith("https://"))

    def test_unknown_sponsor_size_raises(self):
        with self.assertRaises(ValueError):
            immigration_guidance("huge")
