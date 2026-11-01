from docx import Document
import config

# Each section is a pair: (heading, text)
sections = [
    ("1. HEALTH INSURANCE",
     "All full-time employees get health insurance from their first day. "
     "The company pays 80 percent of the cost. The insurance also covers "
     "your partner and children."),
    ("2. GYM ALLOWANCE",
     "Employees receive a gym allowance of 40 US dollars per month. "
     "Submit your gym receipt through the HR portal to claim it."),
    ("3. LEARNING BUDGET",
     "Every employee has a learning budget of 1,000 US dollars per year "
     "for courses, books and conferences. Unused budget does not carry over."),
    ("4. REMOTE WORK",
     "Employees may work from home up to 2 days per week, with manager "
     "approval. New employees get a one-time home office allowance of "
     "300 US dollars."),
    ("5. REFERRAL BONUS",
     "If you refer a friend who is hired, you receive a bonus of "
     "2,000 US dollars after they complete 3 months at Acme Corp."),
]

doc = Document()
doc.add_heading("ACME CORP - EMPLOYEE BENEFITS", level=1)
doc.add_paragraph("Version 1.0 - Applies to all full-time employees")

for heading, text in sections:
    doc.add_heading(heading, level=2)
    doc.add_paragraph(text)

output_path = config.DOCS_DIR / "hr" / "benefits_policy.docx"
doc.save(output_path)
print("Saved:", output_path)