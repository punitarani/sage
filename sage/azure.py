"""sage.azure module"""

import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.textanalytics.aio import TextAnalyticsClient as AsyncTextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

AZURE_LANGUAGE_ENDPOINT = os.environ["AZURE_LANGUAGE_ENDPOINT"]
AZURE_LANGUAGE_KEY = os.environ["AZURE_LANGUAGE_KEY"]

assert AZURE_LANGUAGE_ENDPOINT, "AZURE_LANGUAGE_ENDPOINT environment variable not set"
assert AZURE_LANGUAGE_KEY, "AZURE_LANGUAGE_KEY environment variable not set"

text_analytics_client = TextAnalyticsClient(
    endpoint=AZURE_LANGUAGE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_LANGUAGE_KEY),
)

async_text_analytics_client = AsyncTextAnalyticsClient(
    endpoint=AZURE_LANGUAGE_ENDPOINT,
    credential=AzureKeyCredential(AZURE_LANGUAGE_KEY),
)
