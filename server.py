"""FastpAPI Server"""

from fastapi import FastAPI

from sage import DATA_DIR
from sage.document import load_pdf_document
from sage.openalex import find_similar_papers, get_openalex_work
from sage.summarize import summarize_text_abstractive_async, summarize_text_extractive_async
from sage.unpaywall import get_paper_info, get_paper_url, get_paper_authors

app = FastAPI()


@app.get("/")
async def load_pdf_document_handler(name: str):
    """
    Load a PDF document from the data directory.
    :param name: Name of the PDF file without the extension
    :return: Text of the PDF document
    """
    filepath = DATA_DIR.joinpath(f"{name}.pdf")
    if filepath.exists():
        return load_pdf_document(filepath)
    return None


@app.get("/similar-papers")
async def find_similar_papers_handler(doi: str) -> list[tuple[str, int]]:
    """
    Find similar papers using OpenAlex.
    :param doi: DOI of the paper
    :return: List of similar papers (Entity ID, Similarity Score)
    """
    return await find_similar_papers(doi)


@app.get("/paper-info")
async def get_paper_info_handler(doi: str) -> dict:
    """
    Get the paper info from the Unpaywall API.
    :param doi: DOI of the paper
    :return: Unpaywall Info of the paper
    """
    return await get_paper_info(doi)


@app.get("/paper-url")
async def get_paper_url_handler(doi: str) -> str | None:
    """
    Get the URL of the paper from the Unpaywall API.
    :param doi: DOI of the paper
    :return: URL of the paper or None if not found
    """
    return await get_paper_url(doi)


@app.get("/paper-authors")
async def get_paper_authors_handler(doi: str) -> list[set[str]]:
    """
    Get the authors of the paper from the Unpaywall API.
    :param doi: DOI of the paper
    :return: List of authors of the paper
    """
    return await get_paper_authors(doi)


@app.get("/openalex-work")
async def get_openalex_work_handler(doi: str) -> dict:
    """
    Get the OpenAlex work from the OpenAlex API.
    :param doi: DOI of the paper
    :return: OpenAlex work
    """
    return await get_openalex_work(doi)


@app.get("/summarize-abstractive")
async def summarize_text_abstractive_handler(text: str, doi: str = None) -> str:
    """
    Summarize text using abstractive summarization.
    :param text: Text to summarize
    :param doi: DOI of the paper
    :return: Summary of the text
    """
    return await summarize_text_abstractive_async(doi=doi, text=text)


@app.get("/summarize-extractive")
async def summarize_text_extractive_handler(text: str, doi: str = None) -> str:
    """
    Summarize text using extractive summarization.
    :param text: Text to summarize
    :param doi: DOI of the paper
    :return: Summary of the text
    """
    return await summarize_text_extractive_async(doi=doi, text=text)
