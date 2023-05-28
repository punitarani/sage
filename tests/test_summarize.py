"""tests.test_summarize.py"""

import pytest

from sage.document import load_pdf_document
from sage.summarize import (
    summarize_text_abstractive,
    summarize_text_extractive,
    summarize_text_abstractive_async,
    summarize_text_extractive_async
)
from . import DATA_DIR


def test_summarize_text_abstractive():
    """
    Test summarize_text_abstractive()
    """
    text = load_pdf_document(DATA_DIR.joinpath("ijms-23-12644.pdf"))
    summary = summarize_text_abstractive(text[:1000])
    assert len(summary) > 0


def test_summarize_text_extractive():
    """
    Test summarize_text_extractive()
    """
    text = load_pdf_document(DATA_DIR.joinpath("ijms-23-12644.pdf"))
    summary = summarize_text_extractive(text[:1000])
    assert len(summary) > 0


@pytest.mark.asyncio
async def test_summarize_text_abstractive_async():
    """
    Test summarize_text_abstractive_async()
    """
    text = load_pdf_document(DATA_DIR.joinpath("ijms-23-12644.pdf"))
    summary = await summarize_text_abstractive_async(text[:1000])
    assert len(summary) > 0


@pytest.mark.asyncio
async def test_summarize_text_extractive_async():
    """
    Test summarize_text_extractive_async()
    """
    text = load_pdf_document(DATA_DIR.joinpath("ijms-23-12644.pdf"))

    summary = await summarize_text_extractive_async(text[:1000])
    assert len(summary) > 0
