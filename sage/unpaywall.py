"""sage.unpaywall module"""

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
    with httpx.Client() as client:
        response = client.get(request_url)
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
