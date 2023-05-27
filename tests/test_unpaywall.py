"""tests.test_unpaywall.py"""

import pytest


@pytest.mark.asyncio
async def test_get_paper_info():
    """Test get_paper_info()"""

    from sage.unpaywall import get_paper_info

    # Test with a valid DOI
    doi = "10.1038/s41586-021-03491-6"
    info = await get_paper_info(doi)
    assert info["doi"] == doi

    # Test with an invalid DOI
    doi = "10.1038/invalid-doi"
    info = await get_paper_info(doi)
    assert info == {}


@pytest.mark.asyncio
async def test_get_paper_url():
    """Test get_paper_url()"""

    from sage.unpaywall import get_paper_url

    # Test with a valid DOI
    doi = "10.1038/s41586-021-03491-6"
    url = await get_paper_url(doi)
    assert url == "https://www.nature.com/articles/s41586-021-03491-6.pdf"

    # Test with an invalid DOI
    doi = "10.1038/invalid-doi"
    url = await get_paper_url(doi)
    assert url is None
