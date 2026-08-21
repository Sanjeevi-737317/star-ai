import logging
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

logger = logging.getLogger(__name__)


def generate_po_pdf(po: dict, vendor: dict, rfq: dict, items: list[dict], output_path: str) -> str:
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    title = ParagraphStyle("Title", parent=styles["Heading1"], fontSize=18, textColor=colors.HexColor("#1a237e"), spaceAfter=12)
    heading = ParagraphStyle("Heading", parent=styles["Heading2"], fontSize=12, textColor=colors.HexColor("#283593"), spaceAfter=6)
    normal = ParagraphStyle("NormalCustom", parent=styles["Normal"], fontSize=10, leading=14)

    story.append(Paragraph("STAR AI - Purchase Order", title))
    story.append(Spacer(1, 6))
    story.append(Paragraph(f"PO Number: {po.get('po_number')}", normal))
    story.append(Paragraph(f"Date: {datetime.utcnow().strftime('%Y-%m-%d')}", normal))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Vendor Details", heading))
    story.append(Paragraph(f"Name: {vendor.get('name')}", normal))
    story.append(Paragraph(f"Email: {vendor.get('email', '-')}", normal))
    story.append(Spacer(1, 12))

    story.append(Paragraph("RFQ Details", heading))
    story.append(Paragraph(f"RFQ Number: {rfq.get('rfq_number')}", normal))
    story.append(Paragraph(f"Title: {rfq.get('title')}", normal))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Items", heading))
    table_data = [["Item", "Qty", "Unit Price", "Discount", "Total"]]
    for item in items:
        table_data.append([
            str(item.get("name", "")),
            str(item.get("quantity", 0)),
            f"{item.get('unit_price', 0.0):.2f}",
            f"{item.get('discount', 0.0):.2f}",
            f"{(item.get('quantity', 0) * (item.get('unit_price', 0.0) - item.get('discount', 0.0))):.2f}",
        ])
    table = Table(table_data, colWidths=[2.2 * inch, 0.9 * inch, 1.1 * inch, 1.1 * inch, 1.1 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a237e")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f5f5f5")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(table)
    story.append(Spacer(1, 12))

    story.append(Paragraph(f"Subtotal: {po.get('subtotal', 0.0):.2f}", normal))
    story.append(Paragraph(f"Tax: {po.get('tax', 0.0):.2f}", normal))
    story.append(Paragraph(f"Total Amount: {po.get('total_amount', 0.0):.2f}", normal))
    story.append(Spacer(1, 12))
    story.append(Paragraph("Terms and conditions apply as per STAR AI policy.", normal))

    doc.build(story)
    return output_path
