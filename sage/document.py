"""sage.document module"""

import re
from pathlib import Path

import unicodedata
from langchain.document_loaders import PyMuPDFLoader


def load_pdf_document(filepath: Path) -> str:
    """
    Load a PDF document.
    :param filepath: Path to the PDF file
    :return: List of Document objects
    """
    loader = PyMuPDFLoader(str(filepath))
    doc = loader.load()
    text = "\n".join([page.page_content for page in doc])
    return format_text(text)


def format_text(text: str) -> str:
    """
    Format the text to a standardized form.
    :param: text: Text to format
    :return: Formatted text
    """
    # Normalize the text to Unicode NFC form
    normalized_text = unicodedata.normalize("NFC", text)

    # Remove non-printable characters
    printable_text = re.sub(r"[^\x20-\x7E]", "", normalized_text)

    # Standardize whitespace
    standardized_whitespace = re.sub(r"\s+", " ", printable_text).strip()

    return standardized_whitespace
