"""tests.test_document.py"""

from sage.document import load_pdf_document

from . import DATA_DIR


def test_load_pdf_document():
    data = load_pdf_document(DATA_DIR.joinpath("ijms-23-12644.pdf"))
    assert len(data) == 95835
