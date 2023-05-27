"""
Streamlit App

python -m streamlit run app.py
"""

import asyncio

import streamlit as st

from sage.unpaywall import get_paper_info

if __name__ == "__main__":
    st.set_page_config(page_title="sage", page_icon="🎓", layout="wide")
    st.title("Sage")

    doi_input = st.text_input("DOI", "10.1038/s41586-021-03491-6")

    with st.spinner("Fetching paper info..."):
        paper_info = asyncio.run(get_paper_info(doi_input))

    st.header(paper_info["title"])
    st.markdown(f"[{paper_info['doi']}]({paper_info['doi_url']})")
    st.download_button("Download PDF", paper_info["best_oa_location"]["url_for_pdf"])

    with st.expander("Full info"):
        st.json(paper_info)
