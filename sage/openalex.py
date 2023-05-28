"""sage.openalex module"""

import asyncio
from json import JSONDecodeError
from typing import Any

import httpx
from aiolimiter import AsyncLimiter
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

EMAIL = "email@gmail.com"

openalex_limiter = AsyncLimiter(max_rate=10, time_period=1)


class OpenAlexError(Exception):
    """OpenAlex error"""


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=16),
    retry=retry_if_exception_type(JSONDecodeError)
)
async def openalex_get(url: str) -> dict:
    """
    Get the paper info from the OpenAlex API.
    :param url: URL to the OpenAlex API
    :return: Response JSON from the OpenAlex API
    """
    async with openalex_limiter:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params={"email": EMAIL})
            if response.status_code == 404:
                raise OpenAlexError("Paper not found")
            return response.json()


async def get_paper_citations(doi: str) -> list[str]:
    """
    Get the citations of the paper from the OpenAlex API.
    :param doi: DOI of the paper
    :return: List of citations of the paper
    """
    url = 'https://api.openalex.org/works/' + doi
    response = await openalex_get(url)
    return response.get("referenced_works", [])


async def get_paper_references(doi: str) -> list[dict]:
    """
    Get the references of the paper from the OpenAlex API.
    :param doi: DOI of the paper
    :return: List of references to the paper
    """
    url = 'https://api.openalex.org/works?filter=cites:' + doi
    response = await openalex_get(url)
    return response.get("results", [])


def calculate_similarity_score(paper1: list[str], paper2: list[str]) -> int:
    """
    Calculate the similarity score between two papers.
    :param paper1: List of citations of the first paper
    :param paper2: List of citations of the second paper
    :return: Similarity score between the two papers
    """
    return len(set(paper1) & set(paper2))


async def find_similar_papers(doi: str) -> list[tuple[Any, Any]]:
    """
    Find similar papers based on the references they share.
    """
    citations = await get_paper_citations(doi)

    async def fetch_and_score(citation):
        """
        Fetch the references of a paper and calculate the similarity score.
        :param citation:
        :return: Tuple of paper ID and similarity score
        """
        papers_to_compare = await get_paper_references(citation)

        return [
            (citation, calculate_similarity_score(citations, item['referenced_works']))
            for item in papers_to_compare
        ]

    # Create a list of tasks to run fetch_and_score for each citation concurrently
    tasks = [fetch_and_score(citation) for citation in citations]

    # Run all tasks concurrently and wait for them to complete
    results = await asyncio.gather(*tasks)

    # Flatten the list of results and sum the scores for each citation
    citation_scores = {}
    for result in results:
        for citation, score in result:
            citation_scores[citation] = citation_scores.get(citation, 0) + score

    # Sort by scores in descending order
    sorted_results = sorted(citation_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_results
