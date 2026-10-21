"""Immigration costs, requirements and timeline for the Switzerland → UK secondment.

Everything here comes from decision-ledger.md sections D2 (Swiss posting
certificate) and D11-D14. The sponsor size changes three figures: the sponsor
licence fee, the Immigration Skills Charge and therefore the total.
"""

from decimal import Decimal

# --- Fees (from decision-ledger D11-D14) --------------------------------------

VISA_FEE = Decimal("819")

# £1,035 per year of the visa. The visa lasts the certificate period plus
# 14 days; the surcharge is charged in 6-month blocks, rounded up, so
# 24 months + 14 days is charged as 30 months.
HEALTH_SURCHARGE_PER_YEAR = Decimal("1035")
HEALTH_SURCHARGE = HEALTH_SURCHARGE_PER_YEAR * 2 + HEALTH_SURCHARGE_PER_YEAR / 2  # 2,587.50

CERTIFICATE_OF_SPONSORSHIP_FEE = Decimal("525")

SPONSOR_LICENCE_FEE = {
    "medium_large": Decimal("1682"),
    "small": Decimal("611"),
}

# Charged for the first 12 months, then for each additional 6 months.
IMMIGRATION_SKILLS_CHARGE = {
    "medium_large": {"first_12_months": Decimal("1320"), "per_additional_6_months": Decimal("660")},
    "small": {"first_12_months": Decimal("480"), "per_additional_6_months": Decimal("240")},
}
CERTIFICATE_MONTHS = 24  # 6 April 2026 to 5 April 2028

ETA_FEE = Decimal("20")

SPONSOR_SIZES = {
    "medium_large": "Medium or large sponsor",
    "small": "Small sponsor",
}

SOURCES = {
    "senior_specialist_worker": {
        "label": "Senior or Specialist Worker visa",
        "url": "https://www.gov.uk/senior-specialist-worker-visa",
    },
    "senior_specialist_worker_eligibility": {
        "label": "Senior or Specialist Worker visa: eligibility",
        "url": "https://www.gov.uk/senior-specialist-worker-visa/eligibility",
    },
    "going_rates": {
        "label": "Global Business Mobility going rates for eligible occupations",
        "url": "https://www.gov.uk/government/publications/global-business-mobility-going-rates-for-eligible-occupations",
    },
    "visa_fees": {
        "label": "Home Office immigration and nationality fees, 8 October 2026",
        "url": "https://www.gov.uk/government/publications/visa-regulations-revised-table/home-office-immigration-and-nationality-fees-8-october-2026",
    },
    "health_surcharge": {
        "label": "Immigration Health Surcharge caseworker guidance",
        "url": "https://www.gov.uk/government/publications/immigration-health-surcharge-caseworker-guidance/immigration-health-surcharge-caseworker-guidance-accessible",
    },
    "health_surcharge_how_much": {
        "label": "How much you have to pay for the healthcare surcharge",
        "url": "https://www.gov.uk/healthcare-immigration-application/how-much-pay",
    },
    "ihs_reimbursement": {
        "label": "BSV: reimbursement of the UK health surcharge under the UK-Switzerland convention",
        "url": "https://backend.bsv.admin.ch/fileservice/sdweb-docs-prod-bsvmigch-files/files/2025/07/16/1cbc4e77-6b73-4dc6-a000-e0cc7df5a5ec.pdf",
    },
    "sponsor_licence": {
        "label": "Apply for a sponsor licence",
        "url": "https://www.gov.uk/uk-visa-sponsorship-employers/apply-for-your-licence",
    },
    "certificate_of_sponsorship": {
        "label": "Certificates of sponsorship",
        "url": "https://www.gov.uk/uk-visa-sponsorship-employers/certificates-of-sponsorship",
    },
    "immigration_skills_charge": {
        "label": "Pay the Immigration Skills Charge",
        "url": "https://www.gov.uk/uk-visa-sponsorship-employers/immigration-skills-charge",
    },
    "sponsor_part_2": {
        "label": "Sponsor a Worker guidance, part 2",
        "url": "https://www.gov.uk/government/publications/workers-and-temporary-workers-guidance-for-sponsors-part-2-sponsor-a-worker",
    },
    "sponsor_duties": {
        "label": "Sponsor a Worker guidance, part 3: sponsor duties and compliance",
        "url": "https://www.gov.uk/government/publications/workers-and-temporary-workers-guidance-for-sponsors-part-3-sponsor-duties-and-compliance",
    },
    "right_to_work": {
        "label": "Check a job applicant's right to work",
        "url": "https://www.gov.uk/check-job-applicant-right-to-work",
    },
    "swiss_posting": {
        "label": "BSV: entsandte Arbeitnehmerinnen und Arbeitnehmer (posting via ALPS)",
        "url": "https://www.bsv.admin.ch/de/entsandte",
    },
    "visiting_eu_swiss": {
        "label": "Visiting the UK as an EU, EEA or Swiss citizen",
        "url": "https://www.gov.uk/guidance/visiting-the-uk-as-an-eu-eea-or-swiss-citizen",
    },
    "eta": {
        "label": "Electronic travel authorisation (ETA)",
        "url": "https://www.gov.uk/eta",
    },
    "eta_apply": {
        "label": "Apply for an electronic travel authorisation (ETA)",
        "url": "https://www.gov.uk/eta/apply",
    },
    "visitor_activities": {
        "label": "Immigration Rules Appendix Visitor: permitted activities",
        "url": "https://www.gov.uk/guidance/immigration-rules/immigration-rules-appendix-visitor-permitted-activities",
    },
    "uk_border_control": {
        "label": "UK border control: before you leave for the UK",
        "url": "https://www.gov.uk/uk-border-control/before-you-leave-for-the-uk",
    },
    "evisa": {
        "label": "eVisa",
        "url": "https://www.gov.uk/evisa",
    },
}


def _source(key: str) -> dict:
    """Look up a source by key, so item builders can reference it briefly."""
    return SOURCES[key]


def _item(text: str, source_key: str) -> dict:
    return {"text": text, "source": _source(source_key)}


def _cost(item: str, amount: Decimal, payer: str, note: str, source_key: str) -> dict:
    return {
        "item": item,
        "amount": amount,
        "payer": payer,
        "note": note,
        "source": _source(source_key),
    }


def work_permit_section() -> dict:
    """Section 1: the visa route itself."""
    return {
        "title": "Work permit",
        "summary": "Senior or Specialist Worker visa (Global Business Mobility)",
        "items": [
            _item(
                "This is the intra-company transfer route: the employee stays employed "
                "by the Swiss company and keeps the Swiss contract. The Skilled Worker "
                "route would instead require a UK employment.",
                "senior_specialist_worker",
            ),
            _item(
                "Eligibility: the employee must have worked for the employer outside "
                "the UK, and be paid at least £52,500 or the going rate for the job, "
                "whichever is higher. There is no minimum time with the employer when "
                "the salary is £73,900 or more.",
                "senior_specialist_worker_eligibility",
            ),
            _item(
                "The job must be an eligible occupation at the going rate.",
                "going_rates",
            ),
            _item(
                "The visa lasts the time given on the certificate of sponsorship plus "
                "14 days (or 5 years, whichever is shorter).",
                "senior_specialist_worker",
            ),
            _item(
                "A decision usually takes 3 weeks when applying from outside the UK. "
                "You can apply up to 3 months before the start date.",
                "senior_specialist_worker",
            ),
            _item("The visa is issued as an eVisa.", "evisa"),
        ],
    }


def business_visit_section() -> dict:
    """Section 2: visiting the UK before the assignment starts."""
    return {
        "title": "Business visit before the assignment",
        "summary": "No visa needed for Swiss nationals, but an ETA is required",
        "items": [
            _item(
                "Swiss citizens do not need a visa for business visits, but they do "
                "need an electronic travel authorisation (ETA).",
                "visiting_eu_swiss",
            ),
            _item(
                f"The ETA costs £{ETA_FEE}.",
                "eta",
            ),
            _item(
                "The ETA decision usually arrives by email within a day, but it can "
                "take up to 3 working days. It lasts for 2 years or until the "
                "passport expires.",
                "eta_apply",
            ),
            _item(
                "Allowed on a business visit: meetings, conferences and site visits. "
                "Not allowed: productive work.",
                "visitor_activities",
            ),
        ],
    }


def passport_section() -> dict:
    """Section 3: travel documents."""
    return {
        "title": "Passport",
        "summary": "A passport is needed for the whole stay",
        "items": [
            _item(
                "A passport is required. A Swiss national identity card is only "
                "accepted with EU Settlement Scheme status, a family permit, a "
                "Frontier Worker permit or an S2 Healthcare Visitor permit.",
                "uk_border_control",
            ),
            _item(
                "The passport should be valid for the whole of the stay.",
                "uk_border_control",
            ),
        ],
    }


def company_duties_section() -> dict:
    """Section 4: what the UK subsidiary and the Swiss employer must do."""
    return {
        "title": "What the company must do",
        "summary": "Duties of the UK subsidiary and the Swiss employer",
        "items": [
            _item(
                "The UK subsidiary must hold a sponsor licence to assign a "
                "certificate of sponsorship.",
                "sponsor_licence",
            ),
            _item(
                "The UK subsidiary assigns the certificate of sponsorship.",
                "certificate_of_sponsorship",
            ),
            _item(
                "The UK subsidiary pays the Immigration Skills Charge. Swiss "
                "nationals are not covered by the exemption that applies to EU "
                "nationals.",
                "sponsor_part_2",
            ),
            _item(
                "The UK subsidiary must complete a right to work check before the "
                "employee starts work.",
                "right_to_work",
            ),
            _item(
                "The UK subsidiary must report changes (for example a change of "
                "role or salary) within 10 working days.",
                "sponsor_duties",
            ),
            _item(
                "The Swiss employer applies for the Swiss posting certificate "
                "through ALPS at its AHV compensation office, so Swiss social "
                "security continues during the assignment.",
                "swiss_posting",
            ),
        ],
    }


def _skills_charge(sponsor_size: str) -> Decimal:
    """Immigration Skills Charge for the certificate period."""
    rates = IMMIGRATION_SKILLS_CHARGE[sponsor_size]
    additional_6_month_periods = (CERTIFICATE_MONTHS - 12) // 6
    return rates["first_12_months"] + rates["per_additional_6_months"] * additional_6_month_periods


def _costs(sponsor_size: str) -> list[dict]:
    """The five visa-related costs, each with its payer and source."""
    return [
        _cost(
            "Visa application fee",
            VISA_FEE,
            "Employee (the employer may reimburse)",
            "Fee for a visa of up to 3 years, applied for from outside the UK.",
            "visa_fees",
        ),
        _cost(
            "Immigration Health Surcharge",
            HEALTH_SURCHARGE,
            "Employee (reimbursable under the UK-Switzerland convention)",
            "The visa lasts the certificate period plus 14 days; the surcharge is "
            "charged in 6-month blocks, so 24 months + 14 days is charged as 30 "
            "months. It is reimbursed under the UK-Switzerland convention while "
            "the employee stays in Swiss health insurance.",
            "health_surcharge",
        ),
        _cost(
            "Sponsor licence",
            SPONSOR_LICENCE_FEE[sponsor_size],
            "Employer (UK subsidiary)",
            "Only if the UK subsidiary does not already hold a sponsor licence.",
            "sponsor_licence",
        ),
        _cost(
            "Certificate of sponsorship",
            CERTIFICATE_OF_SPONSORSHIP_FEE,
            "Employer (UK subsidiary)",
            "One certificate is assigned for the visa application.",
            "certificate_of_sponsorship",
        ),
        _cost(
            "Immigration Skills Charge",
            _skills_charge(sponsor_size),
            "Employer (UK subsidiary)",
            "Charge for a 24-month certificate: the first 12 months plus two "
            "further 6-month periods.",
            "immigration_skills_charge",
        ),
    ]


def _timeline() -> list[dict]:
    return [
        {
            "step": "Sponsor licence (if the UK subsidiary does not already hold one)",
            "duration": "Usually less than 8 weeks; a paid priority service is available.",
            "source": _source("sponsor_licence"),
        },
        {
            "step": "Assign the certificate of sponsorship",
            "duration": "Done by the UK subsidiary once the licence is granted. Request the "
            "certificate allocation with the licence application: extra certificates "
            "can take up to 12 weeks.",
            "source": _source("certificate_of_sponsorship"),
        },
        {
            "step": "Visa application",
            "duration": "Decision usually within 3 weeks when applying from outside the UK.",
            "source": _source("senior_specialist_worker"),
        },
        {
            "step": "Total lead time if the UK subsidiary needs a licence",
            "duration": "About 11 weeks.",
            "source": _source("sponsor_licence"),
        },
        {
            "step": "ETA for a business visit before the assignment",
            "duration": "Decision usually within a day, up to 3 working days.",
            "source": _source("eta_apply"),
        },
    ]


def immigration_guidance(sponsor_size: str) -> dict:
    """Return the immigration section of the API response.

    Raises ValueError for a sponsor size other than "medium_large" or "small".
    """
    if sponsor_size not in SPONSOR_SIZES:
        raise ValueError(
            f"Unknown sponsor size {sponsor_size!r}. "
            f"Expected one of: {', '.join(sorted(SPONSOR_SIZES))}."
        )
    costs = _costs(sponsor_size)
    return {
        "sponsor_size": sponsor_size,
        "sections": [
            work_permit_section(),
            business_visit_section(),
            passport_section(),
            company_duties_section(),
        ],
        "costs": costs,
        "total_cost": sum((cost["amount"] for cost in costs), Decimal("0")),
        "timeline": _timeline(),
    }
