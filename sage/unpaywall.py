"""sage.unpaywall module"""

import httpx

EMAIL = "email@gmail.com"


async def get_paper_url(doi: str) -> str | None:
    """
    Get the URL of the paper from the Unpaywall API.
    :param doi: DOI of the paper
    :return: URL of the paper or None if not found
    """

    request_url = f"https://api.unpaywall.org/v2/{doi}?email={EMAIL}"
    async with httpx.AsyncClient() as client:
        response = await client.get(request_url)
        if response.status_code == 200:
            data = response.json()
            if "best_oa_location" in data:
                return data["best_oa_location"]["url_for_pdf"]
    return None
