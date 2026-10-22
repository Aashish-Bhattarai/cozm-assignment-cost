# Assignment Cost Estimate: Switzerland → UK

A small tool that estimates what it costs an employer to send an employee from Switzerland (Zurich) to the UK (London) for two years, and what the move needs for UK immigration.

- **Tab 1, cost estimate:** the total employer cost per year and over the whole assignment, under tax equalisation. The table follows the brief's four sections: home pay, assignment benefits (each tagged as taxable cash, a taxable benefit in kind, or not taxable in the UK), UK tax and employer charges, and the hypothetical Swiss deductions. The UK tax on tax is solved by iteration, and the working is shown.
- **Tab 2, immigration:** the work permit, the business visit before the assignment, passport rules, what the company must do, and the costs and timeline.

Every tax rule and immigration requirement links to the official page it came from. The decisions behind the figures, with their sources, are in [docs/decision-ledger.md](docs/decision-ledger.md).

**Walkthrough video (Loom):** _link added after recording_

## Requirements

- Python 3.12 or newer
- Node.js 20.19+ or 22.12+ (includes npm)

No API keys, accounts or environment variables are needed.

## Install and run

Open two terminals in the repository folder.

**Terminal 1: back end (Django, port 8000)**

Windows (PowerShell):
```powershell
cd backend
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python manage.py runserver
```

macOS / Linux:
```bash
cd backend
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python manage.py runserver
```

**Terminal 2: front end (React, port 5173)**
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173. The test case from the brief is filled in and calculated as soon as the page opens, so the cost for both years appears straight away. Change any input and press **Estimate cost** to update the figures. The immigration details are on the **Immigration** tab.

The front end forwards `/api` requests to the back end, so both must be running.

## Run the tests

Windows:
```powershell
cd backend
.venv\Scripts\python manage.py test
```

macOS / Linux:
```bash
cd backend
.venv/bin/python manage.py test
```

The tests cover the UK tax bands and the gross-up, the Swiss tax and social security, the benefit tagging, the full test-case figures for both years, the immigration costs, and the API's error messages for missing or malformed input.

## Test-case result

| | Year 1 (2026/27) | Year 2 (2027/28) |
|---|---|---|
| UK tax paid by the employer (including tax on tax) | £104,880.01 | £99,524.64 |
| Total employer cost | £271,726.69 (1.76× home pay) | £251,825.87 (1.63× home pay) |

Whole assignment: £523,552.56 (1.69× home pay). Immigration costs are shown separately on tab 2: £8,253.50 for a medium or large sponsor.

## How it is built

```
backend/                  Django project (calculation-only JSON API)
  config/                 settings and top-level URLs
  estimator/
    uk_tax.py             UK income tax 2026/27 and the tax-on-tax gross-up
    swiss_tax.py          hypothetical Swiss tax and social security (Zurich, 2026)
    benefits.py           UK tax treatment of each assignment benefit
    costing.py            the four-section cost table for both years
    immigration.py        immigration requirements, costs and timeline
    forms.py              input validation with readable error messages
    views.py, urls.py     POST /api/estimate and GET /api/immigration
    tests/                one test file per module
frontend/                 React app (Vite)
  src/api.js              calls to the back end
  src/components/         tabs, form, cost tables, immigration tab, source links
docs/decision-ledger.md   every decision with its official source
```

## AI tools used

- **Claude (Opus 5.5)**, through a coding-agent CLI: researching the tax and immigration rules against official sources, planning the structure, reviewing the generated code, and checking the figures and tests.
- **GLM 5.3 Flash**: writing code from detailed specifications, which was then reviewed, corrected and tested.
- **GLM 5.3 and Gemini 3.8 Flash**: independent reviews of the research decisions and figures against the official sources.

## Notes

This is an exercise, not tax advice. Assumptions (for example, that the employee stays on the Swiss employment contract as a secondee) are listed in the tool under the cost estimate and explained in the decision ledger.
