# Suede Buffalo LLC — Seller Carryback Deal Calculator & LOI Generator

A single-file web calculator for creative finance seller carryback deals. Runs entirely in the browser — no backend, no build step. Hosted on GitHub Pages.

**Live tool:** https://pharaohm33.github.io/loi-generator

---

## What It Does

Input your deal numbers and the calculator instantly outputs:

- Full capital stack (senior loan + seller carry + buyer cash)
- Closing cost waterfall and TAF/transactional funding sizing
- Cash back to buyer at close
- Year-by-year paydown grid with exit viability (sale & refi)
- Proforma NOI analysis with stabilization ramp and NOI growth
- One-click **Letter of Intent (LOI)** — formatted, copy-paste ready
- One-click **Buyer Presentation** — full deal summary with percentages

All inputs are URL-shareable (Share Calculator button encodes state into the URL).

---

## Input Sections

### A) Income & NOI
- **Direct NOI Override** — paste annual NOI from an OM to bypass rent-based calculation
- Gross monthly rent, other income, vacancy %, property management %
- Taxes, insurance, R&M (annual)
- **Market Cap Rate** — shows implied property value (click to copy)
- **Annual Appreciation %** — used for exit projections
- **% NOI Increase Per Year** — compounds NOI annually in exit grid
- **Proforma NOI + Stabilization Months** — models a NOI ramp from current → proforma, then growth

### B) Deal Pricing
- Purchase price, cash at closing, as-is value, ARV, rehab budget, rehab out-of-pocket

### C) Senior Loan (DSCR or Hard Money toggle)
- **DSCR mode:** loan sized as As-Is Value × LTV%
- **Hard Money mode:** binding constraint = min(As-Is LTV, LTC, ARV%) — shows which constraint is binding
- Rate, amortization, term, LTV, DSCR requirement, points, broker fee
- Hard Money adds: LTC%, ARV%, rehab completion timeline

### D) Seller Carry Note
- Interest rate, term (years)
- **5 payment modes:**

| Mode | Description |
|---|---|
| Deferred-Simple | Flat $/mo principal; interest accrues on declining balance → balloon |
| Interest-Only (IO) | Monthly interest payments; full principal at balloon |
| P&I (Amortizing) | Standard amortizing payment; balloon = remaining balance at term |
| Deferred-To-Exit | $0/mo; all principal + simple interest due at balloon |
| Deferred-Then-Pay | Deferral period ($0/mo, interest accrues), then IO payments; deferred interest rolls to balloon |
| IO + Deferred Simple | Monthly IO payments at sc_rate% + separate simple interest at sc_deferred_rate% accrues on full principal → balloon |

### E) Closing Costs & Fees
- 1st escrow fee (% of contract price)
- 2nd escrow fee (% of as-is value)
- Acquisition / Bird Dog fee (% of purchase price)
- Loan origination points (% of loan)
- Mortgage broker fee (% of loan)
- Earnest money deposit
- TAF fee % (transactional/acquisition funding)
- Buyer cash in, park-in-escrow toggle, rehab out-of-pocket

### F) Acquisition Correspondent
- Company name, phone, emails
- **Buyer Company** — if filled: LOI title becomes "LOI" (not "Non-Exclusive"), non-circumvent language removed, buyer company listed at bottom

---

## Output Panels

### Calculator Summary
Real-time display of every derived value: NOI, equity spread, capital stack, loan detail, seller carry note, closing costs, cash-back-to-buyer waterfall, cash flow, seller receipts, and proforma debt service.

### Exit Analysis
Year-by-year grid (through balloon + 3 years) showing:
- Property value (appreciation path)
- Seller owed (mode-aware: accounts for accruing interest, amortization, deferral, etc.)
- Cumulative cash flow (NOI-growth-adjusted)
- Sale exit surplus (no CF / with CF)
- Refi cash-out (no CF / with CF)
- Proforma Sale+CF column (when proforma NOI is set)

Viability badges show the first year each exit strategy turns positive, color-coded green (before balloon) or red (after balloon).

### LOI Generator
Produces a formatted Letter of Intent with bold section headers. Two variants:
- **Non-Exclusive LOI** (no buyer company): includes non-circumvent and non-exclusive clauses
- **LOI** (buyer company filled): clean deal terms only, lists buyer company at bottom

Handles all 5 payment modes with accurate language for each. 0% interest rate produces principal-only language with no interest references.

### Buyer Presentation
Full deal narrative with every dollar figure shown as a % of purchase price, including:
- Deal summary, as-is cap rate, implied valuation
- Financing structure with DSCR ratios and LTV%
- Cash-to-close waterfall
- Proforma NOI analysis (if set): ramp path, DSCR at stabilization, DSCR at balloon
- Current NOI exit projection (sale & refi, with/without held CF)
- Proforma exit projection (cap-rate implied value, sale & refi)
- Disclaimer that auto-adjusts based on which paths are active

---

## Admin Template

Click **★ Admin Template** to pre-fill Suede Buffalo LLC defaults:

| Field | Default |
|---|---|
| Company | Suede Buffalo LLC |
| Buyer Company | Don Ava Capital LLC |
| Appreciation | 3% |
| DSCR Requirement | 1.0x |
| Park Escrow | No |
| 1st Escrow Fee | 2% |
| 2nd Escrow Fee | 1.5% |
| TAF Fee | 2.5% |
| Acquisition Fee | 3% |
| Sr Rate | 7% |
| Sr Amort | 30 yr |
| Loan Points | 2% |
| Sr LTV | 75% |

---

## URL Sharing

**Share Calculator** encodes all inputs into the URL as query parameters. Send the link to a partner and they see the exact same numbers. Payment mode and loan type (DSCR/HM) are also encoded.

---

## Files

| File | Purpose |
|---|---|
| `index.html` | Entire web app — HTML, CSS, and JS in one file |
| `loi_generator.py` | Original Python CLI script (generates PDF LOI, predates web app) |

---

## Version History

See the [`versions/`](versions/) folder for full release notes.

| Version | Notes |
|---|---|
| v1.1 | Added IO + Deferred Simple payment mode (6th mode); LOI label renamed to "Monthly Payment Interest Rate" |
| v1.0 | Full web calculator: 5 seller carry modes, proforma NOI, DSCR/HM loan types, LOI generator with buyer toggle, buyer presentation with percentages, URL sharing, admin template |

---

*Internal use — Suede Buffalo LLC*
