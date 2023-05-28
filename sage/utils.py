"""sage.utils.py"""


def safe_filename(doi: str) -> str:
    """
    Creates a safe filename from a DOI, replacing characters that are not allowed in filenames.
    :param doi: DOI of the paper
    :return: Safe filename
    """
    return ''.join(c if c.isalnum() else '_' for c in doi)
