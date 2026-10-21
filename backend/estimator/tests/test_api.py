"""Tests for the JSON API endpoints."""

import json

from django.test import SimpleTestCase

TEST_CASE = {
    "home_country": "CH",
    "host_country": "GB",
    "base_salary_chf": "150000",
    "bonus_chf": "20000",
    "exchange_rate_chf_per_gbp": "1.10",
    "housing_gbp_per_month": "3000",
    "relocation_allowance_chf": "5000",
    "moving_costs_gbp": "6000",
    "temporary_housing_gbp": "4000",
}


class EstimateApiTests(SimpleTestCase):
    """The estimate endpoint, using the brief's test case."""

    databases = set()  # the estimate never touches the database

    def post_estimate(self, body: dict):
        return self.client.post(
            "/api/estimate", data=json.dumps(body), content_type="application/json"
        )

    def test_test_case_returns_the_ledger_totals_as_strings(self):
        response = self.post_estimate(TEST_CASE)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["years"][0]["total_employer_cost"], "271726.69")
        self.assertEqual(data["years"][1]["total_employer_cost"], "251825.87")
        self.assertEqual(data["assignment_total"]["total_employer_cost"], "523552.56")
        self.assertIsInstance(data["years"][0]["total_employer_cost"], str)
        self.assertEqual(data["years"][0]["multiple_of_home_pay"], "1.76")

    def test_missing_base_salary_gives_a_readable_error(self):
        body = {key: value for key, value in TEST_CASE.items() if key != "base_salary_chf"}
        response = self.post_estimate(body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["errors"]["base_salary_chf"], ["Enter the base salary in CHF."]
        )

    def test_non_numeric_salary_is_rejected(self):
        response = self.post_estimate({**TEST_CASE, "base_salary_chf": "abc"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("base_salary_chf", response.json()["errors"])

    def test_negative_salary_is_rejected(self):
        response = self.post_estimate({**TEST_CASE, "base_salary_chf": "-1"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("base_salary_chf", response.json()["errors"])

    def test_unsupported_home_country_is_rejected(self):
        response = self.post_estimate({**TEST_CASE, "home_country": "FR"})
        self.assertEqual(response.status_code, 400)
        self.assertIn("home_country", response.json()["errors"])

    def test_malformed_json_is_rejected(self):
        response = self.client.post(
            "/api/estimate", data="{not json", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["errors"]["__all__"], ["The request body must be valid JSON."]
        )

    def test_get_is_not_allowed(self):
        response = self.client.get("/api/estimate")
        self.assertEqual(response.status_code, 405)
