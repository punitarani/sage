"""tests.test_summarize.py"""

import pytest

from sage.document import load_pdf_document
from sage.summarize import summarize_text_abstractive, summarize_text_extractive
from . import DATA_DIR


@pytest.mark.asyncio
async def test_summarize_text_abstractive():
    """
    Test summarize_text_abstractive()
    """
    text = load_pdf_document(DATA_DIR.joinpath("ijms-23-12644.pdf"))
    summary = await summarize_text_abstractive(text)
    assert len(summary) > 0


@pytest.mark.asyncio
async def test_summarize_text_extractive():
    """
    Test summarize_text_extractive()
    """
    text = load_pdf_document(DATA_DIR.joinpath("ijms-23-12644.pdf"))
    summary = await summarize_text_extractive(text)
    assert len(summary) > 0
