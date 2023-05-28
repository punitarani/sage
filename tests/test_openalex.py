"""tests.test_openalex.py"""

import pytest

from sage.openalex import find_similar_papers


@pytest.mark.asyncio
async def test_find_similar_papers():
    """Test find_similar_papers()"""
    doi = "W2741809807"
    papers = await find_similar_papers(doi)
    assert len(papers) == 35
