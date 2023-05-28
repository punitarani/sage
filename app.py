"""
Streamlit App

python -m streamlit run app.py
"""

import asyncio

import streamlit as st

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

    with st.spinner("Downloading paper..."):
        download_path = asyncio.run(download_paper(doi_input))

    with open(download_path, "rb") as f:
        download_data = f.read()
    st.download_button("Download PDF", data=download_data, file_name=f"{doi_input}.pdf")
