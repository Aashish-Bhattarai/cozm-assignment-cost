"""Input form for the cost estimate, with readable error messages."""

from decimal import Decimal

from django import forms

from .costing import AssignmentInputs


class EstimateForm(forms.Form):
    """The estimate inputs, one field per contract request field.

    All money fields are DecimalFields with 2 decimal places; the exchange
    rate carries 4 because rates such as 1.1050 are normal in FX.
    """

    home_country = forms.ChoiceField(
        choices=[("CH", "Switzerland")],
        error_messages={"invalid_choice": "Only Switzerland is supported."},
    )
    host_country = forms.ChoiceField(
        choices=[("GB", "United Kingdom")],
        error_messages={"invalid_choice": "Only the United Kingdom is supported."},
    )
    base_salary_chf = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        error_messages={
            "required": "Enter the base salary in CHF.",
            "invalid": "Enter the base salary as a number.",
        },
    )
    bonus_chf = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        error_messages={
            "required": "Enter the bonus in CHF.",
            "invalid": "Enter the bonus as a number.",
        },
    )
    exchange_rate_chf_per_gbp = forms.DecimalField(
        max_digits=8,
        decimal_places=4,
        min_value=Decimal("0.0001"),
        error_messages={
            "required": "Enter the exchange rate in CHF per GBP.",
            "invalid": "Enter the exchange rate as a number.",
        },
    )
    housing_gbp_per_month = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        error_messages={
            "required": "Enter the monthly housing cost in GBP.",
            "invalid": "Enter the monthly housing cost as a number.",
        },
    )
    relocation_allowance_chf = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        error_messages={
            "required": "Enter the relocation allowance in CHF.",
            "invalid": "Enter the relocation allowance as a number.",
        },
    )
    moving_costs_gbp = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        error_messages={
            "required": "Enter the moving costs in GBP.",
            "invalid": "Enter the moving costs as a number.",
        },
    )
    temporary_housing_gbp = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        error_messages={
            "required": "Enter the temporary housing cost in GBP.",
            "invalid": "Enter the temporary housing cost as a number.",
        },
    )

    def to_inputs(self) -> AssignmentInputs:
        """Build the costing inputs from the cleaned form data."""
        return AssignmentInputs(
            home_country=self.cleaned_data["home_country"],
            host_country=self.cleaned_data["host_country"],
            base_salary_chf=self.cleaned_data["base_salary_chf"],
            bonus_chf=self.cleaned_data["bonus_chf"],
            exchange_rate_chf_per_gbp=self.cleaned_data["exchange_rate_chf_per_gbp"],
            housing_gbp_per_month=self.cleaned_data["housing_gbp_per_month"],
            relocation_allowance_chf=self.cleaned_data["relocation_allowance_chf"],
            moving_costs_gbp=self.cleaned_data["moving_costs_gbp"],
            temporary_housing_gbp=self.cleaned_data["temporary_housing_gbp"],
        )
