from pypdf import PdfReader
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image

def extract_text_from_pdf(file_object):
    """
    Extracts text from a PDF file, with OCR fallback for scanned documents.

    Args:
        file_object: A file-like object representing the PDF file.

    Returns:
        A string containing the extracted text.
    """
    # Try extracting text with pypdf
    file_object.seek(0)
    reader = PdfReader(file_object)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""

    # If text is short, assume it's a scanned PDF and use OCR
    if len(text.strip()) < 100:
        file_object.seek(0)
        try:
            images = convert_from_bytes(file_object.read())
            ocr_text = ""
            for image in images:
                ocr_text += pytesseract.image_to_string(image)
            text = ocr_text
        except Exception as e:
            print(f"OCR extraction failed: {e}")
            # Return whatever was extracted by pypdf, or an empty string
            return text

    return text
