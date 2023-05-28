"""sage.summarize module"""

from aiocache import cached

from sage import DATA_DIR
from sage.azure import text_analytics_client, async_text_analytics_client
from sage.utils import safe_filename

SUMMARY_ABS_DIR = DATA_DIR.joinpath("summaries", "abs")
SUMMARY_EXT_DIR = DATA_DIR.joinpath("summaries", "ext")


def summarize_text_abstractive(text: str, doi: str = None) -> str:
    """
    Summarize text using abstractive summarization.
    :param text: Text to summarize
    :param doi: DOI of the paper
    :return: Summarized text
    """
    # Check if the summary is cached
    filepath = None
    if doi is not None:
        filepath = SUMMARY_ABS_DIR.joinpath(f"{safe_filename(doi)}.txt")
        if filepath.exists():
            return filepath.read_text()

    poller = text_analytics_client.begin_abstractive_summary([text])
    abstractive_summary_results = poller.result()
    for result in abstractive_summary_results:
        if result.kind == "AbstractiveSummarization":
            summary = "\n".join([summary.text for summary in result.summaries])
            # Cache the summary
            if filepath is not None:
                with open(filepath, "w") as f:
                    f.write(summary)
            return summary


def summarize_text_extractive(text: str, doi: str = None) -> str:
    """
    Summarize text using extractive summarization.
    :param text: Text to summarize
    :param doi: DOI of the paper
    :return: Summarized text
    """
    # Check if the summary is cached
    filepath = None
    if doi is not None:
        filepath = SUMMARY_EXT_DIR.joinpath(f"{safe_filename(doi)}.txt")
        if filepath.exists():
            return filepath.read_text()

    poller = text_analytics_client.begin_extract_summary([text])
    extract_summary_results = poller.result()
    for result in extract_summary_results:
        if result.kind == "ExtractiveSummarization":
            summary = " ".join([sentence.text for sentence in result.sentences])

            # Cache the summary
            if filepath is not None:
                with open(filepath, "w") as f:
                    f.write(summary)
            return summary


@cached()
async def summarize_text_abstractive_async(text: str, doi: str = None) -> str:
    """
    Summarize text using abs summarization.
    :param text: Text to summarize
    :param doi: DOI of the paper
    :return: Summarized text
    """
    # Check if the summary is cached
    filepath = None
    if doi is not None:
        filepath = SUMMARY_ABS_DIR.joinpath(f"{safe_filename(doi)}.txt")
        if filepath.exists():
            return filepath.read_text()

    async with async_text_analytics_client:
        poller = await async_text_analytics_client.begin_abstractive_summary([text])
        abstractive_summary_results = await poller.result()

        async for result in abstractive_summary_results:
            summary = "\n".join([summary.text for summary in result.summaries])

            # Cache the summary
            if filepath is not None:
                with open(filepath, "w") as f:
                    f.write(summary)
            return summary


@cached()
async def summarize_text_extractive_async(text: str, doi: str) -> str:
    """
    Summarize text using extractive summarization.
    :param text: Text to summarize
    :param doi: DOI of the paper
    :return: Summarized text
    """
    # Check if the summary is cached
    filepath = None
    if doi is not None:
        filepath = SUMMARY_EXT_DIR.joinpath(f"{safe_filename(doi)}.txt")
        if filepath.exists():
            return filepath.read_text()

    async with async_text_analytics_client:
        poller = await async_text_analytics_client.begin_extract_summary([text])
        extract_summary_results = await poller.result()
        async for result in extract_summary_results:
            if result.kind == "ExtractiveSummarization":
                summary = " ".join([sentence.text for sentence in result.sentences])

                # Cache the summary
                if filepath is not None:
                    with open(filepath, "w") as f:
                        f.write(summary)
                return summary
