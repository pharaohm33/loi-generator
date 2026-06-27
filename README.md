# Seller Carryback LOI Generator — Suede Buffalo LLC

Automatically calculates deal terms and generates a formatted Non-Exclusive LOI PDF for seller-carryback creative finance deals.

## Features

- **Principal-Only mode** — monthly principal-reduction payments; interest accrues on declining balance and is paid at balloon (Deferred-Simple)
- **Interest-Only mode** — monthly interest-only payments; full principal due at balloon
- Prints a calculator summary to the terminal — **screenshot this for deal documentation**
- Outputs a professionally formatted PDF LOI matching the Suede Buffalo LLC template

## Requirements

```
pip install reportlab openpyxl
```

## Usage

1. Open `loi_generator.py` and edit the `DEAL` dictionary at the top:

```python
DEAL = {
    "property_address": "123 Main St, Salt Lake City, UT 84101",
    "num_units":        24,
    "purchase_price":   4_500_000,
    "cash_at_closing":  2_000_000,
    "interest_rate":    0.08,       # 8% annual simple interest
    "term_years":       10,
    "payment_mode":     "principal_only",   # or "interest_only"
    "monthly_principal": 15_000,    # only used in principal_only mode
    ...
}
```

2. Run:

```bash
python3 loi_generator.py
```

3. **Screenshot the terminal calculator output** — this documents how the offer was generated.

4. The PDF LOI is saved in the current directory with the filename:
   `LOI_<address>_<mode>_<date>.pdf`

## Payment Modes

| Mode | Monthly Payment | Balloon |
|------|----------------|---------|
| `principal_only` | Fixed $ principal reduction; interest accrues | Remaining principal + all accrued interest |
| `interest_only`  | Carry × rate ÷ 12 | Full carry principal |

## LOI Structure

**Page 1 — Deal Terms - Seller Summary**
- Property & purchase price
- Seller receives breakdown
- Seller carry note details & narrative
- Seller protection / senior equity interest
- Timeline

**Page 2 — Non-Circumvent & Signature**
- Non-circumvent clause
- Non-exclusive nature clause
- Seller signature lines
- Acquisition Correspondent contact info

## License

Internal use — Suede Buffalo LLC
