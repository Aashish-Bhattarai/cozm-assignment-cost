"""HTTP layer: validate the input, run the costing, shape the JSON.

All money is rounded for display here, and only here, so the costing keeps
working with unrounded Decimals.
"""

import json
from decimal import ROUND_HALF_UP, Decimal

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from .costing import estimate_assignment_cost
from .forms import EstimateForm
from .immigration import immigration_guidance

TWO_PLACES = Decimal("0.01")


def money(amount: Decimal) -> str:
    """Round a money amount or ratio to 2 decimals, half up, as a string."""
    return str(amount.quantize(TWO_PLACES, rounding=ROUND_HALF_UP))


def to_json(value, key=None):
    """Convert an estimate result into JSON-safe values, recursively.

    Decimals are rounded for display: a "rate" is shown exactly as
    computed, and everything else — money and multiples alike — is shown
    with 2 decimals.
    """
    if isinstance(value, dict):
        return {name: to_json(item, key=name) for name, item in value.items()}
    if isinstance(value, list):
        return [to_json(item, key=key) for item in value]
    if isinstance(value, Decimal):
        if key == "rate":
            return str(value)
        return money(value)
    return value


def form_error_messages(form: EstimateForm) -> dict:
    """Flatten Django's errors into the contract's {"field": ["message"]} shape."""
    return {
        field: [error["message"] for error in errors]
        for field, errors in form.errors.get_json_data().items()
    }


@require_POST
def estimate(request):
    """POST /api/estimate: cost the fixed two-year assignment."""
    try:
        body = json.loads(request.body)
    except ValueError:
        # Covers invalid JSON and bytes that are not valid UTF-8 text.
        return JsonResponse(
            {"errors": {"__all__": ["The request body must be valid JSON."]}},
            status=400,
        )
    if not isinstance(body, dict):
        return JsonResponse(
            {"errors": {"__all__": ["The request body must be a JSON object."]}},
            status=400,
        )
    form = EstimateForm(data=body)
    if not form.is_valid():
        return JsonResponse({"errors": form_error_messages(form)}, status=400)
    return JsonResponse(to_json(estimate_assignment_cost(form.to_inputs())))


@require_GET
def immigration(request):
    """GET /api/immigration: the UK immigration route, costs and timeline."""
    sponsor_size = request.GET.get("sponsor_size", "medium_large")
    try:
        guidance = immigration_guidance(sponsor_size)
    except ValueError as error:
        return JsonResponse({"errors": {"sponsor_size": [str(error)]}}, status=400)
    return JsonResponse(to_json(guidance))
