# Decision ledger: Cozm Assignment Cost Tool (Switzerland → UK)

Status: FINAL CANDIDATE, 20 Oct 2026. Every decision is grounded in the brief or an official page. FX £1 = CHF 1.10 (brief).

## A. Brief requirements → how each is met

| Check | Requirement | How we meet it |
|---|---|---|
| 1 | Runs from README on a clean machine | README gives exact install/run steps; no keys needed (the tool calls no external API) |
| 2 | Work permit, business visa, passport | Immigration tab sections D13–D16 |
| 3 / 9 | Every tax rule and immigration requirement links to an official page | Each figure in this ledger carries the URL shown here (gov.uk, legislation.gov.uk, admin.ch family) |
| 4 | No secrets | None required |
| 5 / 6 | Own repo, ≥5 commits on ≥2 days | Candidate commits each slice |
| 7 | README names AI tools | README section |
| 8 | Test-case inputs accepted, table for both years | Section C |
| 10 | Python + Django back end | Calculation in Python/Django |
| 11 | ≥1 passing test | Test asserts the gross-up fixed point and the test-case figures |
| 12 | Clear error on bad input | Input validation with readable messages |
| 15 | A figure agrees with its cited page | Every input figure quoted verbatim below |

## B. Decisions

### D1. Secondment, not local hire
- **Decision:** the employee stays employed by the Swiss company; the UK subsidiary is the host and operates PAYE.
- **Brief:** "A Swiss company, sending the employee to its UK subsidiary, which runs a UK payroll"; "Home → host"; hypothetical tax; "Decide which country's social security applies".
- **Official:** EIM11820 https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim11820 : "Where an employee works for someone in the UK but is employed and paid by an employer outside the UK the person in the UK for whom the employee works is treated, for the purposes of the PAYE regulations, as making any payments of or on account of PAYE income." Law: ITEPA s689 https://www.legislation.gov.uk/ukpga/2003/1/section/689 ; PAYE81511 https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye81511
- **Reasoning:** every element of the brief (home pay, hypothetical tax, choosing a social security system) only makes sense for an employee who remains employed at home.

### D2. Social security: Swiss system applies; no UK National Insurance
- **Decision:** Swiss AHV/IV/EO + ALV continue for the whole assignment; no UK employee Class 1, employer Class 1 or Class 1A NI.
- **Rule (Convention Art. 14(1)):** "…shall continue to be subject to the legislation of the first State, provided that: (a) the anticipated duration of such work does not exceed 24 months; and (b) that person is not sent to replace another detached worker." https://assets.publishing.service.gov.uk/media/61543391d3bf7f718a54c14c/CS_Swiss_4.2021_UK_Swiss_Social_Security_Coordination.pdf ; in force 1 Oct 2023: https://www.gov.uk/government/publications/ukswitzerland-convention-on-social-security-coordination-cs-switzerland-no42021 ("It fully entered into force on 1 October 2023.")
- **GOV.UK:** "coming to work temporarily in the UK for up to 2 years"; "The certificate can be used as evidence that you do not need to pay National Insurance in the UK." https://www.gov.uk/guidance/social-security-contributions-for-workers-coming-to-the-uk-from-the-eea-or-switzerland
- **Class 1A:** NIM16403: "an employer is not liable to pay Class 1A NICs in respect of benefits provided to a worker … if the worker is exempt from NICs because they are covered by any of the modifications listed at NIM16401." https://www.gov.uk/hmrc-internal-manuals/national-insurance-manual/nim16403
- **Conditions shown in the tool:** 6 Apr 2026 – 5 Apr 2028 does not exceed 24 months; not replacing another posted worker (assumption); employment relationship with the Swiss employer maintained and ≥1 month prior Swiss insurance (JAC Advisory Decision 02/2025: "having been subject to the legislation of the State in which the employer is established for at least one month can be considered as meeting the prior minimum period of time" https://assets.publishing.service.gov.uk/media/6978805bf909df76c5e71f89/JAC-advisory-decision-02-2025.pdf ; he has 3 years); posting certificate obtained by the Swiss employer via ALPS at its AHV compensation office (https://www.bsv.admin.ch/de/entsandte : "Ein Arbeitgeber, der eine Person entsenden möchte, stellt bei der AHV-Ausgleichskasse einen Antrag durch eine Webapplikation im Bereich der Unterstellung (ALPS)").
- **Tool wording:** "No UK NI, provided the Swiss posting certificate is issued."

### D3. Hypothetical Swiss social security (employee share): CHF 10,640.20
- AHV/IV/EO 5.3% × 170,000 = 9,010.00; ALV 1.1% × 148,200 (ceiling) = 1,630.20.
- **Brief:** "Hypothetical Swiss social security covers the employee's AHV/IV/EO and unemployment insurance contributions. Leave out the occupational pension (BVG)."
- **Official 2026:** Federal Personnel Office rates "gültig ab 01.01.2026 … AHV/IV/EO … 5.300% [Arbeitgeber] 5.300% [Arbeitnehmer] … ALV bis Fr. 148'200 … 1.10% 1.10%" https://www.epa.admin.ch/dam/de/sd-web/CtDDI6rw-V4N/Lohntabelle%202026.pdf ; AHV leaflet 2.01 (Stand 1.1.2026) "ziehen Sie 5,3 % des Lohns Ihrer Arbeitnehmenden … ab" https://www.ahv-iv.ch/p/2.01.d ; ALV leaflet 2.08 "Bis zu einem jährlichen Höchstbetrag von 148 200 Franken beträgt der Beitragssatz an die ALV 2,2 %" https://www.ahv-iv.ch/p/2.08.d
- **NBU (non-occupational accident insurance) excluded:** not in the brief's list, and there is no official rate: "Angaben über die Nettoprämiensätze können nicht gemacht werden, da jeder Versicherer einen individuellen Prämientarif erstellt." https://sozialversicherungen.admin.ch/de/d/6877/download?version=17

### D4. Hypothetical Swiss income tax: CHF 31,428.45 (tax year 2026, Zurich city, single, no church tax, no BVG)
- **Brief:** "the federal, cantonal and communal income tax a single person living in the city of Zurich would pay on the same salary and bonus, with no church tax… Leave out the occupational pension (BVG)."
- **Method:** computed in code from official tariffs (no external API at runtime).
- **Deductions** (consistent with "no BVG"; no pillar 3a assumed because the brief gives none):
  - AHV/IV/EO 9,010 + ALV 1,630.20 (D3)
  - Flat professional expenses: 3% of net salary, min 2,000, max 4,000 → 4,000. Federal: https://www.estv2.admin.ch/stp/sm/2024/berufskosten-de-fr.pdf ; Zurich VPBU (from tax period 2026): "3% des Nettolohns, mindestens jedoch Fr. 2000 höchstens Fr. 4000" https://www.estv2.admin.ch/stp/kb/zh-de.pdf ; 2026 unchanged: "Bei den Abzügen ändert sich aufgrund der geringen Teuerung nichts … Auch hier ergeben sich für das Steuerjahr 2026 … keine Änderungen" https://www.estv.admin.ch/de/newnsb/VzaAUrhkPx2EPde4a6e3O
  - Insurance premiums, at the statutory maximum for a person WITHOUT pillar 2/3a contributions: federal 2,700 ("Dito, für Steuerpflichtige ohne Beiträge an die Säulen 2 und 3a" https://www.estv2.admin.ch/stp/sm/2024/versicherungspraemien-zinsen-de-fr.pdf ; unchanged for 2026 per the EFD release above); Zurich 2,900 × 1.5 = 4,350 (§31 Abs. 1 lit. g StG: "von Fr. 2900 für die übrigen Steuerpflichtigen. Für Steuerpflichtige ohne Beiträge gemäss lit. d und e erhöhen sich diese Abzüge um die Hälfte." https://www.estv2.admin.ch/stp/kb/zh-de.pdf). Applied at the maximum, as the ESTV calculator does.
- **Federal:** taxable 170,000 − 9,010 − 1,630.20 − 4,000 − 2,700 = 152,659.80. 2026 tariff (VKP): "für 141 500 Franken Einkommen … 6140.55 … und für je weitere 100 Franken Einkommen 11.00 mehr" → 6,140.55 + 111 × 11.00 = **7,361.55**. https://www.estv.admin.ch/dam/de/sd-web/gnde9CmEsalK/dbst-tairfe-58c-2026-dfi.pdf
- **Zurich simple tax:** taxable 170,000 − 9,010 − 1,630.20 − 4,000 − 4,350 = 151,009.80; 2026 basic tariff (§35 StG, "Gültig ab Steuerperiode 2026") cumulative 10,476 to 144,100, then 11% → 10,476 + 69 × 11 = **11,235** (per full CHF 100). https://www.estv2.admin.ch/stp/kb/zh-de.pdf
- **Multipliers:** canton 95% → 10,673.25 ("liegt für die Jahre 2026 und 2027 bei 95 Prozent der einfachen Staatssteuer" https://www.zh.ch/de/steuern-finanzen/steuern/steuerstatistiken/aktuelle-gemeinde-steuerfuesse.html); city 119% → 13,369.65 ("Der Steuerfuss soll bei 119 Prozent bleiben" https://www.stadt-zuerich.ch/de/aktuell/medienmitteilungen/2025/09/str-budget-2026.html ; the ESTV calculator's 2026 result applies 119%).
- **Personal tax:** CHF 24 (§200 StG "Die Personalsteuer beträgt Fr. 24." https://www.notes.zh.ch/appl/zhlex_r.nsf/WebView/49B30E8052B9D928C125849A00480C6C/$File/631.1_8.6.97_107.pdf).
- **Total:** 7,361.55 + 10,673.25 + 13,369.65 + 24 = **CHF 31,428.45**.
- **Reconciliation with the ESTV calculator** https://swisstaxcalculator.estv.admin.ch/ : the calculator always adds an age-based BVG deduction (5,988 at age 40), NBU 593 and the "with pension" premium caps (1,800 / 2,900). With those defaults, the same code gives CHF 29,578, identical to the calculator's 2026 result for CHF 170,000, Zurich, single, no church tax. The tool displays this reconciliation.

### D5. Same rates in both years
- UK 2026/27 for both years (brief: "Use 2026/27 UK rates for both years").
- Swiss: 2026 tariffs for both years. Canton 95% is legislated for 2027 too (zh.ch above); the city 119% for 2027 and the 2027 inflation adjustments are not yet published, so 2026 values are carried forward (assumption). Hypothetical tax is computed per year on annual pay, ignoring the mismatch between the Swiss calendar year and the UK April–April year (assumption).

### D6. UK income tax 2026/27 (England)
- Personal allowance £12,570; "goes down by £1 for every £2 that your adjusted net income is above £100,000 … zero if your income is £125,140 or above" https://www.gov.uk/income-tax-rates
- Bands on taxable income: "Basic tax rate 20% Up to £37,700; Higher tax rate 40% From £37,701 to £125,140; Additional tax rate 45% Above £125,140" https://www.gov.uk/guidance/rates-and-thresholds-for-employers-2026-to-2027

### D7. Tax on tax (gross-up by iteration)
- **Brief:** I = net home pay after hypothetical deductions + taxable benefits; T = UKTax(I + T); "Solve it by iteration".
- **Official basis that employer-paid tax is taxable:** EIM00580 (pecuniary liability; case table "Employee's income tax | Hartland v Diggines") https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim00580 ; grossing up EIM07700 https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim07700 ; PAYE72028 https://www.gov.uk/hmrc-internal-manuals/paye-manual/paye72028 ; tax equalisation HS212 https://www.gov.uk/government/publications/tax-equalisation-hs212-self-assessment-helpsheet/tax-equalisation-2026-hs212
- **Method:** T0 = 0; T(n+1) = UKTax(I + T(n)); stop when |T(n+1) − T(n)| < £0.000001; figures rounded to pence only for display. Each iteration is shown in the output; the closed form is used only as a cross-check.

### D8. Benefits: UK tags
| Benefit | Tag | Taxable amount | Source |
|---|---|---|---|
| Housing £3,000/month, rent paid to landlord | **Taxable benefit in kind** (rent paid; annual value assumed ≤ rent) | £36,000/yr | EIM11431: "the greater of - the annual value … and - the rent paid for the taxable period by the person providing it" https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim11431 |
| Moving costs £6,000 (yr 1) | **Not taxable in the UK** (qualifying removal expense, inside the £8,000 exemption) | £0 | EIM03103: "exempts from tax the first £8,000 of removal expenses and benefits" https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim03103 ; move from abroad accepted once UK resident: EIM03104 https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim03104 |
| Temporary housing £4,000 (yr 1), first £2,000 | **Not taxable in the UK** (uses the rest of the £8,000 exemption) | £0 | EIM03117: "applies where the employee intends to move to permanent accommodation… the measure of the benefit to be charged or counted against the £8,000 limit is the cost to the employer" https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim03117 |
| Temporary housing £4,000 (yr 1), remaining £2,000 | **Taxable benefit in kind** (excess over £8,000) | £2,000 | https://www.gov.uk/expenses-and-benefits-relocation/what-to-report-and-pay : "You do not have to report or deduct anything for qualifying costs up to £8,000. Qualifying costs over £8,000 … report on form P11D" |
| Relocation allowance CHF 5,000 cash (yr 1) | **Taxable cash** | £4,545.45 | EIM03139: "strictly there is no place for flat-rate allowances, which should be subject to PAYE" https://www.gov.uk/hmrc-internal-manuals/employment-income-manual/eim03139 |
- The law exempts the first £8,000 of the pooled qualifying costs; which item absorbs the £2,000 excess is a presentation choice (exemption applied in the order listed). The taxable total is £2,000 either way.
- Temporary-workplace relief (ITEPA s339) not claimed: London is the employee's main residence for the posting ("Many overseas postings are for limited periods of one, two or three years: the accommodation that the employee intends to occupy for the duration of the posting is the permanent accommodation for this purpose" EIM03117).

### D9. Employer cost composition
- Total employer cost = home pay (CHF 170,000 / 1.10) + full cost of all benefits + T − hypothetical Swiss tax / 1.10 − hypothetical Swiss social security / 1.10 (brief sections 1–4).
- **Swiss employer contributions** (5.3% AHV/IV/EO + 1.1% ALV = CHF 10,640.20/yr ≈ £9,672.91; EPA 2026 source above) continue under D2 but are excluded from the total. The brief's section 3 is "Host tax and charges", and home pay is "as if the employee had stayed in Switzerland", so the employer would bear them anyway. The tool shows them in the assumptions with the amount.
- No UK employer charges apply:
  - National Insurance: none (D2). Apprenticeship Levy: "Your pay bill must not include earnings … of employees who are not subject to UK National Insurance contributions legislation" https://www.gov.uk/guidance/pay-apprenticeship-levy
  - Workplace pension auto-enrolment: not applicable to a secondee whose contract stays abroad. TPR detailed guidance no. 3, para 47: "Where a non-UK employer is placing a worker on a secondment basis to a UK employer … If the worker's contract remains with the employer located outside the UK and there is an expectation on the part of the employer that the worker will return to work which is based outside the UK for their non-UK employer at the end of their placement, the worker is unlikely to be considered to be ordinarily working in the UK." Example: "The UK employer knows that they do not have to carry out an assessment for Sophie because her contract of employment is not with them." https://www.thepensionsregulator.gov.uk/en/document-library/automatic-enrolment-detailed-guidance/3-assessing-the-workforce

### D10. Exchange rate
- £1 = CHF 1.10, both years, user-editable input (brief: "fixed for both years; make it an input").

## C. Test-case result

Net home pay = (170,000 − 31,428.45 − 10,640.20) / 1.10 = **£116,301.23**. Hypothetical tax £28,571.32; hypothetical social security £9,672.91; home pay £154,545.45.

| | Year 1 (2026/27) | Year 2 (2027/28) |
|---|---|---|
| 1. Home pay | £154,545.45 | £154,545.45 |
| 2. Benefits (cost) | housing 36,000 + moving 6,000 + temporary 4,000 + relocation cash 4,545.45 = £50,545.45 | housing £36,000 |
| Taxable benefits | 36,000 + 2,000 + 4,545.45 = £42,545.45 | £36,000 |
| I | £158,846.68 | £152,301.23 |
| 3. UK tax T (iterated; check UKTax(I+T) = T) | £104,880.01 | £99,524.64 |
| UK employer NI | £0 (D2) | £0 |
| 4. Hypothetical deductions | −£28,571.32 − £9,672.91 | same |
| **Total employer cost** | **£271,726.69 (1.76× home pay)** | **£251,825.87 (1.63×)** |

Two-year total **£523,552.56 (1.69×)**. All figures are computed unrounded (T solved to < £0.000000001) and rounded only for display; T matches the closed form (0.45·I − 13,797)/0.55 that holds once the personal allowance is fully withdrawn.

## D. Immigration (tab 2)

### D11. Work permit: Senior or Specialist Worker (Global Business Mobility)
- "allows you to come to or stay in the UK to do an eligible job at your employer's UK branch" https://www.gov.uk/senior-specialist-worker-visa
- Eligibility: "have worked for your employer outside the UK"; "You must be paid at least £52,500 or the 'going rate' for your job - whichever is higher"; "If you're earning £73,900 a year or more, there is no minimum time requirement" https://www.gov.uk/senior-specialist-worker-visa/eligibility (salary £136,364 base; 3 years with the employer). Occupation must be eligible (going rates: https://www.gov.uk/government/publications/global-business-mobility-going-rates-for-eligible-occupations).
- Why not Skilled Worker: that route sponsors a UK employment, which conflicts with D1/D2 (secondment keeps the Swiss employment).
- Decision time: "3 weeks, if you're outside the UK"; "You can apply for a visa up to 3 months before the day you are due to start work".
- Visa length: "whichever is shorter of: the time given on your certificate of sponsorship plus 14 days; 5 years" https://www.gov.uk/senior-specialist-worker-visa → CoS 6 Apr 2026 – 5 Apr 2028 gives a visa of 24 months + 14 days.
- End-to-end lead time if the UK subsidiary has no licence: sponsor licence "less than 8 weeks" → assign CoS → visa "3 weeks" from outside the UK → about 11 weeks; ETA for a pre-assignment visit "within a day … up to 3 working days".

### D12. Costs and company duties
| Item | Amount | Payer | Source |
|---|---|---|---|
| Visa (up to 3 years, outside UK) | £819 | applicant (employer may reimburse) | https://www.gov.uk/government/publications/visa-regulations-revised-table/home-office-immigration-and-nationality-fees-8-october-2026 |
| Immigration Health Surcharge | 2 × £1,035 + £517.50 = £2,587.50 (visa of 24 months + 14 days, rounded up to 30 months) | applicant (reimbursable, see below) | Home Office IHS caseworker guidance v10.0: "the IHS liability will include any additional period of immigration permission granted before or after the course of study or period of employment. The IHS portal will calculate the IHS liability to include these periods" and "The IHS is charged in 6-month periods … rounded up to the next 6-month period" https://www.gov.uk/government/publications/immigration-health-surcharge-caseworker-guidance/immigration-health-surcharge-caseworker-guidance-accessible ; "£1,035 per year" https://www.gov.uk/healthcare-immigration-application/how-much-pay ; law: IHS Order 2015 art. 4(6)(a) "6 months or less, the amount payable for that part is half of the specified annual amount" https://www.legislation.gov.uk/uksi/2015/792/article/4 . GOV.UK's "2 years = £2,070" style examples describe the permission length, not the job length. |
| Sponsor licence (if not held) | £1,682 medium/large; £611 small | sponsor | https://www.gov.uk/uk-visa-sponsorship-employers/apply-for-your-licence ("Most applications are dealt with in less than 8 weeks") |
| Certificate of Sponsorship | £525 | sponsor | https://www.gov.uk/uk-visa-sponsorship-employers/certificates-of-sponsorship |
| Immigration Skills Charge (2 years) | £1,320 + £660 + £660 = £2,640 medium/large; £480 + £240 + £240 = £960 small | sponsor | https://www.gov.uk/uk-visa-sponsorship-employers/immigration-skills-charge |
| **Total** | **£8,253.50** medium/large (default); £5,502.50 small | | |
- Sponsor size is an input (default medium/large; a small sponsor meets at least 2 of: turnover ≤ £15m, assets ≤ £7.5m, ≤ 50 employees, per the licence page).
- Swiss nationals are not covered by the EU ISC exemption ("this concession does not apply if the worker is a national of Iceland, Norway, Liechtenstein or Switzerland") https://www.gov.uk/government/publications/workers-and-temporary-workers-guidance-for-sponsors-part-2-sponsor-a-worker
- IHS is still charged (Convention Art. 19), but BSV states: "the convention (Art. 21 and 22 Annex 1) provides that this fee shall be reimbursed to persons who, under the convention, remain compulsorily insured under the Swiss health insurance scheme during their stay in the United Kingdom" https://backend.bsv.admin.ch/fileservice/sdweb-docs-prod-bsvmigch-files/files/2025/07/16/1cbc4e77-6b73-4dc6-a000-e0cc7df5a5ec.pdf
- Company duties: right to work check "before you employ them" https://www.gov.uk/check-job-applicant-right-to-work ; report changes within 10 working days (sponsor guidance part 3) https://www.gov.uk/government/publications/workers-and-temporary-workers-guidance-for-sponsors-part-3-sponsor-duties-and-compliance ; Swiss posting certificate via ALPS (D2).

### D13. Business visit before the assignment
- No visa for Swiss nationals; ETA required: "Citizens from the EU, Switzerland, Norway, Iceland or Liechtenstein (except Irish citizens) need an electronic travel authorisation (ETA) to travel to the UK without a visa" https://www.gov.uk/guidance/visiting-the-uk-as-an-eu-eea-or-swiss-citizen
- ETA: "costs £20" https://www.gov.uk/eta ; "decision by email within a day, but it can take up to 3 working days"; "lasts for 2 years or until your passport expires" https://www.gov.uk/eta/apply
- Permitted: meetings, conferences, site visits; no productive work: https://www.gov.uk/guidance/immigration-rules/immigration-rules-appendix-visitor-permitted-activities

### D14. Passport
- Passport required; Swiss national ID card only accepted with EUSS status, family permit, Frontier Worker permit or S2: https://www.gov.uk/uk-border-control/before-you-leave-for-the-uk ; "Your identity document should be valid for the whole of your stay."
- Visa issued as an eVisa: https://www.gov.uk/evisa

## E. Assumptions displayed in the tool
1. Secondment: remains employed by the Swiss company (D1).
2. Swiss posting certificate issued; not replacing another posted worker; ≤ 24 months (D2).
3. No BVG and no pillar 3a; insurance-premium deductions at the statutory maximum; NBU excluded (D3, D4). The employee's age is not used; the age 40 appears only in the ESTV-calculator reconciliation.
4. Swiss 2026 tariffs and the city multiplier of 119% carried into year 2 (D5).
5. UK 2026/27 rates both years; England rates (London) (D6).
6. Housing annual value ≤ rent; temporary-workplace relief not claimed (D8).
7. Relocation cash treated as taxable cash, not as reimbursement of qualifying costs (D8).
8. Swiss employer contributions (CHF 10,640.20/yr) excluded from the total (D9).
9. UK workplace pension auto-enrolment not applicable to the secondee (D9, TPR para 47).
10. Sponsor is medium/large and needs a licence (D12; input).
11. This is an exercise, not tax advice (brief).
