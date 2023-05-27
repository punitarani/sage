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


@pytest.mark.asyncio
async def test_get_authors():
    """Test get_authors()"""

    from sage.unpaywall import get_authors

    # Test with a valid DOI
    doi = "10.1038/s41586-021-03491-6"
    authors = await get_authors(doi)
    assert authors == [
        {"given": "Luca", "family": "Braga", "sequence": "first"},
        {"ORCID": "http://orcid.org/0000-0002-5056-845X", "given": "Hashim", "family": "Ali", "sequence": "additional",
         "authenticated-orcid": False},
        {"given": "Ilaria", "family": "Secco", "sequence": "additional"},
        {"given": "Elena", "family": "Chiavacci", "sequence": "additional"},
        {"ORCID": "http://orcid.org/0000-0001-6463-6997", "given": "Guilherme", "family": "Neves",
         "sequence": "additional", "authenticated-orcid": False},
        {"ORCID": "http://orcid.org/0000-0003-4597-5963", "given": "Daniel", "family": "Goldhill",
         "sequence": "additional", "authenticated-orcid": False},
        {"given": "Rebecca", "family": "Penn", "sequence": "additional"},
        {"ORCID": "http://orcid.org/0000-0002-1726-8033", "given": "Jose M.", "family": "Jimenez-Guardeño",
         "sequence": "additional", "authenticated-orcid": False},
        {"ORCID": "http://orcid.org/0000-0002-9023-0103", "given": "Ana M.", "family": "Ortega-Prieto",
         "sequence": "additional", "authenticated-orcid": False},
        {"given": "Rossana", "family": "Bussani", "sequence": "additional"},
        {"ORCID": "http://orcid.org/0000-0001-7609-6297", "given": "Antonio", "family": "Cannatà",
         "sequence": "additional", "authenticated-orcid": False},
        {"ORCID": "http://orcid.org/0000-0002-9001-5374", "given": "Giorgia", "family": "Rizzari",
         "sequence": "additional", "authenticated-orcid": False},
        {"ORCID": "http://orcid.org/0000-0003-3909-422X", "given": "Chiara", "family": "Collesi",
         "sequence": "additional", "authenticated-orcid": False},
        {"ORCID": "http://orcid.org/0000-0002-1147-1882", "given": "Edoardo", "family": "Schneider",
         "sequence": "additional", "authenticated-orcid": False},
        {"ORCID": "http://orcid.org/0000-0003-2872-6906", "given": "Daniele", "family": "Arosio",
         "sequence": "additional", "authenticated-orcid": False},
        {"given": "Ajay M.", "family": "Shah", "sequence": "additional"},
        {"ORCID": "http://orcid.org/0000-0002-3948-0895", "given": "Wendy S.", "family": "Barclay",
         "sequence": "additional", "authenticated-orcid": False},
        {"ORCID": "http://orcid.org/0000-0002-7699-2064", "given": "Michael H.", "family": "Malim",
         "sequence": "additional", "authenticated-orcid": False},
        {"given": "Juan", "family": "Burrone", "sequence": "additional"},
        {"ORCID": "http://orcid.org/0000-0003-2927-7225", "given": "Mauro", "family": "Giacca",
         "sequence": "additional", "authenticated-orcid": False},
    ]

    # Test with an invalid DOI
    doi = "10.1038/invalid-doi"
    authors = await get_authors(doi)
    assert authors == []


@pytest.mark.asyncio
async def test_download_paper():
    """Test download_paper()"""

    from sage.unpaywall import download_paper

    # Test with a valid DOI
    doi = "10.1038/s41586-021-03491-6"
    filename = await download_paper(doi)
    assert filename is not None
    assert filename.exists()

    # Test with an invalid DOI
    doi = "10.1038/invalid-doi"
    filename = await download_paper(doi)
    assert filename is None
