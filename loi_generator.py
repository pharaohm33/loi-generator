#!/usr/bin/env python3
"""
Seller Carryback LOI Generator
Suede Buffalo LLC

Supports two payment modes:
  - principal_only  : Monthly principal-reduction payments; interest accrues on declining
                      balance (simple) and is paid at balloon (Deferred-Simple)
  - interest_only   : Monthly interest-only payments; full principal due at balloon (IO)

Usage:
    python loi_generator.py
    or edit DEAL below and run.

A calculator summary is printed to screen before the PDF is written.
Screenshot the terminal output to document how the offer was generated.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                HRFlowable, Table, TableStyle)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import date
import math

# ─────────────────────────────────────────────────────────────────────────────
#  DEAL INPUTS  ← edit these for each offer
# ─────────────────────────────────────────────────────────────────────────────
DEAL = {
    # Property
    "property_address":   "600 N 600 E, North Logan, UT 84321",
    "num_units":          159,

    # Pricing
    "purchase_price":     37_000_000,
    "cash_at_closing":    17_300_000,   # 1st-escrow / seller down-payment / cash to seller

    # Seller carry note terms
    "interest_rate":      0.08,         # annual simple interest
    "term_years":         17,           # balloon year

    # Payment mode: "principal_only"  OR  "interest_only"
    "payment_mode":       "principal_only",

    # --- principal_only mode ---
    "monthly_principal":  30_000,       # $ per month principal reduction

    # Acquisition Correspondent
    "ac_name":            "Suede Buffalo LLC",
    "ac_email1":          "suedebuffalofficial@gmail.com",
    "ac_email2":          "montanoemmanuel@gmail.com",
    "ac_phone":           "520 633 6437",

    # Date shown on document (None = today)
    "doc_date":           None,
}
# ─────────────────────────────────────────────────────────────────────────────


def fmt(n, decimals=0):
    """Format number as dollar string."""
    if decimals == 0:
        return f"${n:,.0f}"
    return f"${n:,.{decimals}f}"


def pct(r):
    return f"{r*100:.2f}%"


def calculate_principal_only(deal):
    """
    Deferred-Simple: fixed monthly principal reduction.
    Interest accrues each month on the CURRENT (declining) balance at simple rate.
    All accrued interest + remaining principal paid at balloon.
    Returns results dict.
    """
    carry       = deal["purchase_price"] - deal["cash_at_closing"]
    rate_mo     = deal["interest_rate"] / 12
    months      = deal["term_years"] * 12
    pmt         = deal["monthly_principal"]

    balance     = carry
    total_interest = 0.0

    for _ in range(months):
        interest_this_month = balance * rate_mo
        total_interest += interest_this_month
        balance -= pmt
        if balance < 0:
            balance = 0

    remaining_principal = max(balance, 0)
    balloon = remaining_principal + total_interest
    total_principal_paid = carry - remaining_principal
    total_receipts = deal["cash_at_closing"] + total_principal_paid + balloon

    return {
        "carry":                  carry,
        "monthly_payment":        pmt,
        "payment_description":    f"{fmt(pmt)}/month (principal reduction only; interest accrues)",
        "total_principal_paid":   total_principal_paid,
        "remaining_principal":    remaining_principal,
        "total_accrued_interest": total_interest,
        "balloon":                balloon,
        "total_receipts":         total_receipts,
        "financing_income":       total_receipts - deal["purchase_price"],
    }


def calculate_interest_only(deal):
    """
    Interest-Only: monthly payment = carry × annual_rate / 12.
    Principal balance never reduces; full principal due at balloon.
    Returns results dict.
    """
    carry      = deal["purchase_price"] - deal["cash_at_closing"]
    rate_mo    = deal["interest_rate"] / 12
    months     = deal["term_years"] * 12
    pmt        = carry * rate_mo

    total_interest  = pmt * months
    balloon         = carry                           # principal only at end
    total_receipts  = deal["cash_at_closing"] + total_interest + balloon

    return {
        "carry":                  carry,
        "monthly_payment":        pmt,
        "payment_description":    f"{fmt(pmt, 2)}/month (interest only)",
        "total_principal_paid":   0,
        "remaining_principal":    carry,
        "total_accrued_interest": total_interest,
        "balloon":                balloon,
        "total_receipts":         total_receipts,
        "financing_income":       total_receipts - deal["purchase_price"],
    }


def run_calculator(deal):
    if deal["payment_mode"] == "principal_only":
        r = calculate_principal_only(deal)
    else:
        r = calculate_interest_only(deal)
    r["mode"]  = deal["payment_mode"]
    r["deal"]  = deal
    return r


def print_calculator(r):
    """Print the calculator summary to terminal. SCREENSHOT THIS OUTPUT."""
    d = r["deal"]
    sep = "─" * 66

    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║     SELLER CARRYBACK DEAL CALCULATOR  —  Suede Buffalo LLC      ║")
    print("║         ★  SCREENSHOT THIS OUTPUT  — Offer Documentation  ★     ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()
    print(f"  Property    : {d['property_address']} ({d['num_units']} Units)")
    print(f"  Date        : {d.get('doc_date') or date.today().strftime('%B %d, %Y')}")
    print(sep)
    print(f"  Payment Mode: {'PRINCIPAL-ONLY (interest accrues to balloon)' if r['mode'] == 'principal_only' else 'INTEREST-ONLY (principal paid at balloon)'}")
    print()
    print("  A. DEAL STRUCTURE")
    print(f"     Purchase Price          : {fmt(d['purchase_price'])}")
    print(f"     Cash at Closing         : {fmt(d['cash_at_closing'])}")
    print(f"     Seller Carryback Note   : {fmt(r['carry'])}")
    print(f"     Interest Rate           : {pct(d['interest_rate'])} simple interest")
    print(f"     Term                    : {d['term_years']} Years ({d['term_years']*12} months)")
    print()
    print("  B. SELLER CARRY NOTE")
    print(f"     Monthly Payment         : {r['payment_description']}")

    if r["mode"] == "principal_only":
        print(f"     Total Principal Paid    : {fmt(r['total_principal_paid'])}")
        print(f"     Remaining Principal     : {fmt(r['remaining_principal'])}")
        print(f"     Total Accrued Interest  : {fmt(r['total_accrued_interest'])}")
    else:
        print(f"     Total Interest Paid     : {fmt(r['total_accrued_interest'])}")
        print(f"     Balloon (principal)     : {fmt(r['balloon'])}")

    print(f"     Balloon Payment Yr {d['term_years']:2d}   : ~{fmt(r['balloon'])}")
    print()
    print("  C. TOTAL SELLER RECEIPTS")
    print(f"     Cash at Closing         : {fmt(d['cash_at_closing'])}")
    if r["mode"] == "principal_only":
        print(f"     + Monthly Principal Pmts: {fmt(r['total_principal_paid'])}")
    else:
        print(f"     + Monthly Interest Pmts : {fmt(r['total_accrued_interest'])}")
    print(f"     + Balloon Payment       : {fmt(r['balloon'])}")
    print(f"     ═══════════════════════════════════════")
    print(f"     TOTAL RECEIPTS          : ~{fmt(r['total_receipts'])}")
    print(f"     (Includes {fmt(r['financing_income'])} in seller financing income)")
    print()
    print(sep)
    print("  ★ Screenshot complete — use as LOI calculation documentation.")
    print()


def build_loi_pdf(r, output_path):
    d  = r["deal"]
    doc_date = d.get("doc_date") or date.today().strftime("%B %d, %Y")
    filename = output_path

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=1.1*inch,
        rightMargin=1.1*inch,
        topMargin=1*inch,
        bottomMargin=1*inch,
    )

    styles = getSampleStyleSheet()

    def s(name, **kwargs):
        base = styles[name]
        return ParagraphStyle(name + "_custom", parent=base, **kwargs)

    title_style   = s("Normal", fontSize=12, fontName="Helvetica-Bold",
                      alignment=TA_CENTER, spaceAfter=2)
    subtitle_style= s("Normal", fontSize=12, fontName="Helvetica-Bold",
                      alignment=TA_CENTER, spaceAfter=14)
    bold_label    = s("Normal", fontSize=11, fontName="Helvetica-Bold",
                      spaceAfter=4)
    body          = s("Normal", fontSize=11, fontName="Helvetica",
                      spaceAfter=4, leading=15)
    body_indent   = s("Normal", fontSize=11, fontName="Helvetica",
                      spaceAfter=4, leading=15, leftIndent=14)
    section_hdr   = s("Normal", fontSize=11, fontName="Helvetica-Bold",
                      spaceAfter=5, spaceBefore=10)
    underline_body= s("Normal", fontSize=11, fontName="Helvetica",
                      spaceAfter=4, leading=15)
    small         = s("Normal", fontSize=10, fontName="Helvetica", spaceAfter=3)

    carry  = r["carry"]
    mode   = r["mode"]
    years  = d["term_years"]
    months = years * 12

    # ── Build interest/payment description paragraphs ──
    if mode == "principal_only":
        pmt_label = f"Monthly Principal-Reduction Payments:"
        pmt_line  = f"Months 1–{months}: {fmt(d['monthly_principal'])}/month"
        note_lines = [
            f"Total Monthly Principal Payments Over {years} Years: "
            f"{fmt(r['total_principal_paid'])}",
            f"Balloon Payment at Year {years}: Approximately {fmt(r['balloon'])}",
            f"Total Seller Receipts Over {years} Years: Approximately "
            f"{fmt(r['total_receipts'])}",
        ]
        narrative = [
            f"The seller receives {fmt(d['cash_at_closing'])} at closing and carries back "
            f"{fmt(carry)}.",

            f"During the {years}-year term, buyer will make monthly principal-reduction "
            f"payments totaling approximately {fmt(r['total_principal_paid'])}. These "
            f"payments reduce the seller carry balance.",

            f"Interest accrues separately at {pct(d['interest_rate'])} simple interest on "
            f"the declining principal balance and is paid at the end of the term with the "
            f"remaining principal balance.",

            f"At the end of year {years}, buyer will pay the remaining principal balance "
            f"plus accrued interest through a balloon payment of approximately "
            f"{fmt(r['balloon'])}.",

            f"Total seller receipts are approximately {fmt(r['total_receipts'])}, which "
            f"includes the full {fmt(d['purchase_price'])} purchase price plus approximately "
            f"{fmt(r['financing_income'])} in seller financing income.",
        ]
    else:
        pmt_label = f"Monthly Interest-Only Payments:"
        pmt_line  = f"Months 1–{months}: {fmt(r['monthly_payment'], 2)}/month"
        note_lines = [
            f"Total Interest Paid Over {years} Years: "
            f"{fmt(r['total_accrued_interest'])}",
            f"Balloon Payment at Year {years}: {fmt(r['balloon'])} (principal)",
            f"Total Seller Receipts Over {years} Years: Approximately "
            f"{fmt(r['total_receipts'])}",
        ]
        narrative = [
            f"The seller receives {fmt(d['cash_at_closing'])} at closing and carries back "
            f"{fmt(carry)}.",

            f"During the {years}-year term, buyer will make monthly interest-only payments "
            f"of {fmt(r['monthly_payment'], 2)}, totaling approximately "
            f"{fmt(r['total_accrued_interest'])} in interest.",

            f"Interest is calculated at {pct(d['interest_rate'])} simple interest on the "
            f"outstanding principal balance of {fmt(carry)}.",

            f"At the end of year {years}, buyer will pay the full principal balance of "
            f"{fmt(carry)} through a balloon payment.",

            f"Total seller receipts are approximately {fmt(r['total_receipts'])}, which "
            f"includes the full {fmt(d['purchase_price'])} purchase price plus approximately "
            f"{fmt(r['financing_income'])} in seller financing income.",
        ]

    story = []

    # ── Page 1 ────────────────────────────────────────────────────────────────
    story.append(Paragraph("Non-Exclusive LOI", title_style))
    story.append(Paragraph("Deal Terms - Seller Summary", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black))
    story.append(Spacer(1, 10))

    prop_str = f"{d['property_address']} - {d['num_units']} Units"
    story.append(Paragraph(f"<b>Property</b>: {prop_str}", body))
    story.append(Paragraph(f"<b>Purchase Price</b>: {fmt(d['purchase_price'])}", body))
    story.append(Spacer(1, 8))

    story.append(Paragraph("SELLER RECEIVES:", section_hdr))
    story.append(Paragraph(f"Cash at Closing: {fmt(d['cash_at_closing'])}", body_indent))
    story.append(Paragraph(f"Seller Carryback Note: {fmt(carry)}", body_indent))
    story.append(Paragraph(f"Interest Rate: {pct(d['interest_rate'])} simple interest", body_indent))
    story.append(Paragraph(f"Term: {years} Years", body_indent))
    story.append(Spacer(1, 8))

    story.append(Paragraph("SELLER CARRY NOTE", section_hdr))
    story.append(Paragraph(pmt_label, body))
    story.append(Paragraph(pmt_line, body_indent))
    for line in note_lines:
        story.append(Paragraph(line, body_indent))
    story.append(Spacer(1, 8))

    for para in narrative:
        story.append(Paragraph(para, body))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 6))
    story.append(Paragraph("SELLER PROTECTION BY SENIOR EQUITY INTEREST", section_hdr))
    story.append(Paragraph(
        "Your position is documented as a Senior Equity Interest, giving you first-priority "
        "claim to all cash flow and proceeds from operations, refinance, or sale — ahead "
        "of all buyer equity. If the buyer defaults on the note, the operating agreement "
        "allows you to take over the buyer’s interest in the property without foreclosure.",
        body))

    story.append(Spacer(1, 8))
    story.append(Paragraph("TIMELINE:", section_hdr))
    story.append(Paragraph(
        "Closing: Within 45-90 days of signed purchase and sales agreement.", body))

    # ── Page 2 ────────────────────────────────────────────────────────────────
    from reportlab.platypus import PageBreak
    story.append(PageBreak())

    story.append(Paragraph("Non-Circumvent", section_hdr))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "The Acquisition Correspondent will bring the buyer to closing on the property. "
        "Upon signing, Seller agrees not to circumvent the Acquisition Correspondent. "
        "In the event of circumvention, Seller shall pay the Acquisition Correspondent "
        "a penalty equal to 1% of the total purchase price.", body))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "Circumvention is defined as Seller closing on the subject property listed in "
        "this LOI with a buyer introduced by the Acquisition Correspondent, without "
        "ensuring that the Acquisition Correspondent is compensated by either party.", body))
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        "<u>The Acquisition Correspondent’s fee is currently payable by the buyer.</u> "
        "If the Acquisition Correspondent is unable to secure payment from the buyer, "
        "Seller agrees to coordinate a mutually agreed-upon payment with the Acquisition "
        "Correspondent prior to closing. If it becomes apparent that the Acquisition "
        "Correspondent is not on track to be paid before closing, it is the Acquisition "
        "Correspondent’s duty to disclose this to Seller, and Seller’s duty to "
        "respond to such communication in a timely manner.", body))

    story.append(Spacer(1, 12))
    story.append(Paragraph("Non-Exclusive Nature:", section_hdr))
    story.append(Paragraph(
        "Seller may entertain other offers until final purchase and sales agreement is "
        "in place with end buyer. At point of signing purchase and sales agreement, "
        "seller may not entertain other offers and honor the closing timeline set in "
        "purchase and sales agreement.", body))

    story.append(Spacer(1, 20))
    story.append(Paragraph("Seller Signature", body))
    story.append(Spacer(1, 24))
    story.append(HRFlowable(width=3.5*inch, thickness=0.5, color=colors.black,
                             hAlign="LEFT"))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Seller Name (Print)", body))
    story.append(Spacer(1, 24))
    story.append(HRFlowable(width=3.5*inch, thickness=0.5, color=colors.black,
                             hAlign="LEFT"))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Date", body))
    story.append(Spacer(1, 24))
    story.append(HRFlowable(width=3.5*inch, thickness=0.5, color=colors.black,
                             hAlign="LEFT"))

    story.append(Spacer(1, 20))
    story.append(Paragraph(f"<b>Acquisition Correspondent</b>:", body))
    story.append(Paragraph(d["ac_name"], body_indent))
    story.append(Paragraph("Contact:", body_indent))
    story.append(Paragraph(f"Email:", small))
    story.append(Paragraph(f"    {d['ac_email1']}", small))
    story.append(Paragraph(f"    {d['ac_email2']}", small))
    story.append(Paragraph(f"Phone:", small))
    story.append(Paragraph(f"    {d['ac_phone']}", small))

    doc.build(story)
    print(f"\n  ✓ LOI saved to: {output_path}\n")


def main():
    r = run_calculator(DEAL)

    # ── Print calculator (screenshot this) ──
    print_calculator(r)

    # ── Build output filename ──
    addr_slug = DEAL["property_address"].replace(",", "").replace(" ", "_")[:40]
    mode_slug = "PrincipalOnly" if DEAL["payment_mode"] == "principal_only" else "InterestOnly"
    today     = date.today().strftime("%Y-%m-%d")
    out_path  = f"LOI_{addr_slug}_{mode_slug}_{today}.pdf"

    build_loi_pdf(r, out_path)


if __name__ == "__main__":
    main()
