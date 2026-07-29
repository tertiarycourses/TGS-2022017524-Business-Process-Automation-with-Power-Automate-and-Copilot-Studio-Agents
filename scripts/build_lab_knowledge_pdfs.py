#!/usr/bin/env python3
from pathlib import Path
import shutil
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
OUT.mkdir(parents=True, exist_ok=True)

BLUE = colors.HexColor("#1769E0")
DARK = colors.HexColor("#10223B")
PALE = colors.HexColor("#EEF4FB")
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="DocTitle", parent=styles["Title"], fontName="Helvetica-Bold",
                          fontSize=23, leading=28, textColor=DARK, alignment=TA_CENTER, spaceAfter=18))
styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontName="Helvetica-Bold",
                          fontSize=15, leading=19, textColor=BLUE, spaceBefore=12, spaceAfter=7))
styles.add(ParagraphStyle(name="Body2", parent=styles["BodyText"], fontSize=10.5, leading=15,
                          textColor=DARK, spaceAfter=7))
styles.add(ParagraphStyle(name="Small", parent=styles["BodyText"], fontSize=8.5, leading=11,
                          textColor=colors.HexColor("#52647A")))
styles.add(ParagraphStyle(name="TableHeader", parent=styles["Body2"], fontName="Helvetica-Bold",
                          fontSize=10.5, leading=14, textColor=colors.white))

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BLUE)
    canvas.rect(0, A4[1] - 8*mm, A4[0], 8*mm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#52647A"))
    canvas.setFont("Helvetica", 8)
    canvas.drawString(18*mm, 10*mm, "Tertiary Infotech Academy · Classroom training resource")
    canvas.drawRightString(A4[0]-18*mm, 10*mm, f"Page {doc.page}")
    canvas.restoreState()

def build(name, title, subtitle, sections):
    path = OUT / name
    doc = SimpleDocTemplate(str(path), pagesize=A4, rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=18*mm, title=title, author="Tertiary Infotech Academy")
    story = [Spacer(1, 11*mm), Paragraph(title, styles["DocTitle"]),
             Paragraph(subtitle, styles["Body2"]), Spacer(1, 4*mm)]
    for heading, body in sections:
        story.append(Paragraph(heading, styles["Section"]))
        if isinstance(body, list):
            rows = [[Paragraph("Question / topic", styles["TableHeader"]),
                     Paragraph("Approved response", styles["TableHeader"])]]
            for left, right in body:
                rows.append([Paragraph(left, styles["Body2"]), Paragraph(right, styles["Body2"])])
            table = Table(rows, colWidths=[50*mm, 110*mm], repeatRows=1)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), BLUE), ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                ("BACKGROUND", (0,1), (-1,-1), PALE), ("GRID", (0,0), (-1,-1), .4, colors.HexColor("#A9BAD0")),
                ("VALIGN", (0,0), (-1,-1), "TOP"), ("LEFTPADDING", (0,0), (-1,-1), 7),
                ("RIGHTPADDING", (0,0), (-1,-1), 7), ("TOPPADDING", (0,0), (-1,-1), 6),
                ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ]))
            story.append(table)
        else:
            story.append(Paragraph(body, styles["Body2"]))
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    return path

build("IT Support FAQ.pdf", "IT Support FAQ", "Approved knowledge source for the Lab 5 IT Support Agent.", [
    ("Account and access", [
        ("How do I reset my password?", "Use the organisation's self-service password reset page. Verify the web address before entering credentials. If self-service fails, contact the service desk. Support staff will never ask for your password."),
        ("My MFA prompt did not arrive.", "Check network connectivity and the registered authenticator method. Do not approve an unexpected prompt. If the registered device is unavailable, contact the service desk for identity verification."),
        ("Can you give me an administrator password?", "No. Passwords, MFA codes, recovery keys and privileged credentials must never be requested, disclosed or repeated."),
    ]),
    ("Connectivity and devices", [
        ("VPN will not connect.", "Confirm normal internet access, restart the VPN client, verify system time and note the displayed error. If it continues, send the error and device asset number to the service desk."),
        ("I cannot join office Wi-Fi.", "Forget and reconnect to the approved corporate network. Do not use an unknown network with a similar name. Escalate certificate or account errors."),
        ("My laptop or phone is lost.", "Report it immediately to the service desk and your manager. Provide the asset number and last known location. Do not attempt unsafe recovery."),
    ]),
    ("Escalation", "Contact the IT service desk when identity verification, device replacement, security investigation, privileged access or an undocumented error is required. Include the time, device, steps tried and exact error, but never send credentials."),
])

build("HR Policies.pdf", "HR Policies", "Fictional classroom policy source for the Lab 6 HR Support Agent.", [
    ("Leave policy", [
        ("Annual leave", "Submit dates, leave type and reason through the approved leave process. Approval depends on eligibility, balance and operational needs. The employee must wait for manager approval before making commitments."),
        ("Medical leave", "Notify the manager promptly and provide documentation only through approved HR channels. Medical information is confidential and must not be shared beyond authorised personnel."),
        ("Compassionate or unpaid leave", "Contact the manager and HR because eligibility and supporting information depend on circumstances. The agent must not promise approval."),
    ]),
    ("Working arrangements", [
        ("Flexible work request", "Discuss the proposed arrangement with the manager and submit it through the approved HR process. Business needs, role requirements and policy determine the decision."),
        ("Conduct and respectful workplace", "Employees must act respectfully and report harassment, discrimination, retaliation or safety concerns through the published HR or ethics channel."),
    ]),
    ("Expenses and personal data", [
        ("Expense claims", "Submit itemised receipts, business purpose and cost centre within 30 days through the approved expense system. Manager approval is required."),
        ("Employee data", "Access only the personal data required for an authorised duty. Never use the HR agent to request another employee's leave, medical, performance or payroll information."),
    ]),
    ("Escalation", "HR and the employee's manager make final decisions. Escalate unclear eligibility, policy exceptions, disputes, sensitive personal matters and any request not answered by the approved source."),
])

build("Finance Knowledge Base.pdf", "Finance Knowledge Base", "Educational knowledge source for the Lab 9 Finance Information Agent.", [
    ("Market basics", [
        ("Market order", "An instruction to trade promptly at the best available price. Execution is prioritised, but the final price is not guaranteed."),
        ("Limit order", "An instruction to trade only at a specified price or better. Price is controlled, but execution is not guaranteed."),
        ("Bid, ask and spread", "The bid is the highest current buying price; the ask is the lowest current selling price. Their difference is the spread."),
    ]),
    ("Candles and timeframes", [
        ("OHLC candle", "A candle summarises open, high, low and close for one interval. Volume, when available, indicates activity but does not prove direction."),
        ("1-minute, 15-minute and 1-hour views", "Short intervals show rapid changes and more noise; longer intervals provide broader context. Different timeframes can point in different directions."),
        ("Volatility", "Volatility describes the magnitude of price variation. Higher volatility increases uncertainty and potential loss as well as potential gain."),
    ]),
    ("News and interpretation", "News can affect expectations, but headlines may be incomplete, delayed or already reflected in price. Check time, publisher, relevance and corroboration. Separate observed data from interpretation."),
    ("Risk boundary", "The agent provides general education only. It must not predict guaranteed returns, choose investments for a person, or issue personalised buy or sell instructions. Users should consider independent professional advice and their own objectives and risk tolerance."),
])

travel_policy = build("Travel Expense Policy.pdf", "Travel Expense Policy", "Fictional approved policy source for the Lab 11 Expense Claim Agent.", [
    ("Required claim information", [
        ("Business purpose", "Every claim must identify a clear work-related purpose. Personal entertainment and personal travel are not reimbursable."),
        ("Receipt", "An itemised receipt is required when the total claim amount is above SGD 50. Missing receipts require human review and may require a declaration."),
        ("Submission deadline", "Claims should be submitted within 30 calendar days of the expense. Older claims require human review."),
    ]),
    ("Category limits", [
        ("Local transport", "Taxi, private-hire and public transport are limited to SGD 80 per day for approved business travel."),
        ("Meals", "Business-travel meals are limited to SGD 60 per person per day. Alcohol and personal entertainment are not reimbursable."),
        ("Hotel", "Accommodation is limited to SGD 300 per room per night unless a documented exception is approved."),
        ("Airfare", "Air travel requires documented pre-approval. Economy class is the default unless the approved travel standard states otherwise."),
    ]),
    ("Decision meanings", [
        ("ELIGIBLE_FOR_APPROVAL", "The supplied facts fit the published thresholds. A manager still makes the final approval."),
        ("MORE_INFORMATION_REQUIRED", "Required evidence or a required fact is missing."),
        ("OUTSIDE_POLICY", "The supplied facts exceed a published limit or describe a non-reimbursable category."),
        ("HUMAN_REVIEW", "The claim is ambiguous, late, exceptional, unsupported or outside the agent's authority."),
    ]),
    ("Human decision boundary", "The Expense Claim Agent and its flows provide policy guidance and routing recommendations only. They must not promise reimbursement, create evidence, override a limit, or treat an AI recommendation as the final approval. The authorised manager or expense team makes the final decision."),
])
travel_policy_asset = (
    ROOT
    / "labs/Day 2/Lab 11 - Travel Expense Agent and Agent Flow/assets"
    / "Travel Expense Policy.pdf"
)
travel_policy_asset.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(travel_policy, travel_policy_asset)

print("\n".join(str(p) for p in sorted(OUT.glob("*.pdf"))))
