"""sage.summarize module"""

from aiocache import cached

from sage.azure import text_analytics_client, async_text_analytics_client


def summarize_text_abstractive(text: str) -> str:
    """
    Summarize text using abstractive summarization.
    :param text: Text to summarize
    :return: Summarized text
    """
    poller = text_analytics_client.begin_abstractive_summary([text])
    abstractive_summary_results = poller.result()
    for result in abstractive_summary_results:
        if result.kind == "AbstractiveSummarization":
            return "\n".join([summary.text for summary in result.summaries])


def summarize_text_extractive(text: str) -> str:
    """
    Summarize text using extractive summarization.
    :param text: Text to summarize
    :return: Summarized text
    """
    poller = text_analytics_client.begin_extract_summary([text])
    extract_summary_results = poller.result()
    for result in extract_summary_results:
        if result.kind == "ExtractiveSummarization":
            return " ".join([sentence.text for sentence in result.sentences])


@cached()
async def summarize_text_abstractive_async(text: str) -> str:
    """
    Summarize text using abstractive summarization.
    :param text: Text to summarize
    :return: Summarized text
    """
    async with async_text_analytics_client:
        poller = await async_text_analytics_client.begin_abstractive_summary([text])
        abstractive_summary_results = await poller.result()

        async for result in abstractive_summary_results:
            return "\n".join([summary.text for summary in result.summaries])


@cached()
async def summarize_text_extractive_async(text: str) -> str:
    """
    Summarize text using extractive summarization.
    :param text: Text to summarize
    :return: Summarized text
    """
    async with async_text_analytics_client:
        poller = await async_text_analytics_client.begin_extract_summary([text])
        extract_summary_results = await poller.result()
        async for result in extract_summary_results:
            if result.kind == "ExtractiveSummarization":
                return " ".join([sentence.text for sentence in result.sentences])
