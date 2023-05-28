"""sage.unpaywall module"""

import tempfile
from pathlib import Path

import httpx
from aiocache import cached

EMAIL = "email@gmail.com"


@cached()
async def get_paper_info(doi: str) -> dict:
    """
    Get the paper info from the Unpaywall API.
    :param doi: DOI of the paper
    :return: Info of the paper
    """
    request_url = f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}"
    async with httpx.AsyncClient() as client:
        response = await client.get(request_url)
        if response.status_code == 200:
            return response.json()
    return {}


async def get_paper_url(doi: str) -> str | None:
    """
    Get the URL of the paper from the Unpaywall API.
    :param doi: DOI of the paper
    :return: URL of the paper or None if not found
    """
    data = await get_paper_info(doi)
    if "best_oa_location" in data:
        return data["best_oa_location"]["url_for_pdf"]
    return None


async def get_authors(doi: str) -> list[set[str]]:
    """
    Get the authors of the paper from the Unpaywall API.
    :param doi: DOI of the paper
    :return: List of authors of the paper
    """
    data = await get_paper_info(doi)
    return data.get("z_authors", [])


async def download_paper(doi: str) -> Path | None:
    """
    Download the paper from the Unpaywall API.
    :param doi: DOI of the paper
    :return: Path to the downloaded paper or None if not found

    The file is saved in a temporary directory and will be deleted when the program exits.
    """

    url = await get_paper_url(doi)
    if url is None:
        return None
    async with httpx.AsyncClient() as client:
        response = await client.get(url, follow_redirects=True)
        if response.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False) as f:
                f.write(response.content)
                return Path(f.name)
    return None
