"""tests.test_openalex.py"""

import pytest

from sage.openalex import find_similar_papers, get_openalex_work, get_paper_citations, get_paper_references


@pytest.mark.asyncio
async def test_get_openalex_work():
    """Test get_openalex_work()"""
    doi = "10.1038/s41586-021-03491-6"
    paper = await get_openalex_work(doi=doi)
    assert paper and paper != {}
    assert paper["id"] == "https://openalex.org/W3152312420"
    assert paper["doi"] == "https://doi.org/10.1038/s41586-021-03491-6"

    entity_id = "W3152312420"
    paper = await get_openalex_work(entity_id=entity_id)
    assert paper and paper != {}
    assert paper["id"] == "https://openalex.org/W3152312420"
    assert paper["doi"] == "https://doi.org/10.1038/s41586-021-03491-6"


@pytest.mark.asyncio
async def test_get_paper_citations():
    """Test get_paper_citations()"""
    doi = "10.1038/s41586-021-03491-6"
    citations = await get_paper_citations(doi=doi)
    assert len(citations) == 49

    entity_id = "W3152312420"
    citations = await get_paper_citations(entity_id=entity_id)
    assert len(citations) == 49


@pytest.mark.asyncio
async def test_get_paper_references():
    """Test get_paper_references()"""
    doi = "10.1038/s41586-021-03491-6"
    references = await get_paper_references(doi=doi)
    assert len(references) == 25

    entity_id = "W3152312420"
    references = await get_paper_references(entity_id=entity_id)
    assert len(references) == 25


@pytest.mark.asyncio
async def test_find_similar_papers():
    """Test find_similar_papers()"""
    doi = "10.7717/peerj.4375"
    papers = await find_similar_papers(doi)
    assert len(papers) == 35
