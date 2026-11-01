from fpdf import FPDF
import config

sections = [
    ("1. EMAIL",
     "Company email is for work. Short personal use is allowed during breaks. "
     "Email attachments can be at most 25 MB. Use OneDrive links for bigger files."),
    ("2. USB DRIVES",
     "USB drives are not allowed on company laptops. "
     "Use OneDrive to share files instead."),
    ("3. CLOUD STORAGE",
     "OneDrive is the only approved cloud storage. "
     "Personal accounts such as Dropbox or Google Drive must not be used for company files."),
    ("4. SCREEN LOCK",
     "Lock your screen every time you leave your desk. "
     "Laptops lock automatically after 5 minutes without activity."),
]

pdf = FPDF()
pdf.add_page()

pdf.set_font("Helvetica", style="B", size=16)
pdf.multi_cell(0, 10, "ACME CORP - ACCEPTABLE USE POLICY", new_x="LMARGIN", new_y="NEXT")

for heading, text in sections:
    pdf.ln(4)
    pdf.set_font("Helvetica", style="B", size=12)
    pdf.multi_cell(0, 8, heading, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")

output_path = config.DOCS_DIR / "it" / "acceptable_use_policy.pdf"
pdf.output(str(output_path))
print("Saved:", output_path)