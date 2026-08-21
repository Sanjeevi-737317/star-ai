import logging
import os

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_path: str) -> str:
    try:
        from pypdf import PdfReader
        reader = PdfReader(file_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception:
        logger.exception("PDF extraction failed")
        return ""


def extract_text_from_excel(file_path: str) -> str:
    try:
        import openpyxl
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        lines = []
        for sheet in workbook.worksheets:
            for row in sheet.iter_rows(values_only=True):
                line = " | ".join(str(cell) for cell in row if cell is not None)
                if line.strip():
                    lines.append(line)
        return "\n".join(lines)
    except Exception:
        logger.exception("Excel extraction failed")
        return ""


def extract_text_from_image(file_path: str) -> str:
    try:
        from PIL import Image
        import pytesseract
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)
    except Exception:
        logger.exception("Image OCR failed")
        return ""


def extract_text(file_path: str) -> str:
    lower = file_path.lower()
    if lower.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    if lower.endswith((".xlsx", ".xls")):
        return extract_text_from_excel(file_path)
    if lower.endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp")):
        return extract_text_from_image(file_path)
    raise ValueError(f"Unsupported file type: {file_path}")
