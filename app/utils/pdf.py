import re
from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

def generate_pdf(report_content: str, query: str) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1 * inch)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle", parent=styles["Title"], fontSize=20, spaceAfter=30, alignment=1
    )
    heading1_style = ParagraphStyle(
        "CustomHeading1",
        parent=styles["Heading1"],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=12,
    )
    heading2_style = ParagraphStyle(
        "CustomHeading2",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=16,
        spaceAfter=10,
    )

    content = []
    content.append(Paragraph("🔬 AI Research Report", title_style))
    content.append(Paragraph(f"<b>Query:</b> {query}", styles["Normal"]))
    content.append(
        Paragraph(
            f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles["Normal"],
        )
    )
    content.append(Spacer(1, 0.3 * inch))

    lines = report_content.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            content.append(Spacer(1, 0.1 * inch))
            continue
        processed_line = line
        processed_line = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", processed_line)
        processed_line = re.sub(
            r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", processed_line
        )
        processed_line = re.sub(
            r"(https?://[^\s<>" + r"{}" + r"|\^\[\]]+)",
            r"<link href=\"\1\">\1</link>",
            processed_line,
        )
        if line.startswith("# "):
            content.append(Paragraph(processed_line[2:], heading1_style))
        elif line.startswith("## "):
            content.append(Paragraph(processed_line[3:], heading2_style))
        elif line.startswith("### "):
            content.append(Paragraph(processed_line[4:], styles["Heading3"]))
        elif line.startswith("- ") or line.startswith("* "):
            bullet_text = processed_line[2:]
            content.append(Paragraph(f"• {bullet_text}", styles["Normal"]))
        else:
            if processed_line:
                content.append(Paragraph(processed_line, styles["Normal"]))
    doc.build(content)
    buffer.seek(0)
    return buffer
