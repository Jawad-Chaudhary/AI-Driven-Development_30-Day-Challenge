
import pypdf

def extract_text_from_pdf(file_obj) -> str:
    """
    Extracts text from a PDF file object.

    Args:
        file_obj: A file-like object (e.g., from st.file_uploader) of a PDF file.

    Returns:
        A string containing all extracted text from the PDF.
    """
    try:
        reader = pypdf.PdfReader(file_obj)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

