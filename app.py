"""
Streamlit App

python -m streamlit run app.py
"""

import asyncio

import streamlit as st

from sage.document import load_pdf_document
from sage.openalex import find_similar_papers
from sage.summarize import summarize_text_abstractive
from sage.unpaywall import get_paper_info, download_paper

if __name__ == "__main__":
    st.set_page_config(page_title="sage", page_icon="🎓", layout="wide")
    st.title("Sage")

    doi_input = st.text_input("DOI", "10.1038/s41586-021-03491-6")

    with st.spinner("Fetching paper info..."):
        paper_info = asyncio.run(get_paper_info(doi_input))

    if not paper_info:
        st.error("Invalid DOI")
        st.stop()

    st.header(paper_info["title"])
    st.markdown(f"[{paper_info['doi']}]({paper_info['doi_url']})")

    with st.expander("Full info"):
        st.json(paper_info)

    with st.spinner("Finding similar papers..."):
        similar_papers = asyncio.run(find_similar_papers(doi_input))

    with st.expander("Similar papers"):
        for paper in similar_papers:
            st.write(f"{paper[0]} - {paper[1]}")

    with st.spinner("Downloading paper..."):
        download_path = asyncio.run(download_paper(doi_input))

    with open(download_path, "rb") as f:
        download_data = f.read()
    st.download_button("Download PDF", data=download_data, file_name=f"{doi_input}.pdf")

    with st.spinner("Summarizing paper..."):
        text = load_pdf_document(download_path)
        summary = asyncio.run(summarize_text_abstractive(text))

    st.header("Summary")
    st.write(summary)
