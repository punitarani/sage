"""
Streamlit App

python -m streamlit run app.py
"""

import asyncio

import streamlit as st

from sage.document import load_pdf_document
from sage.openalex import find_similar_papers, get_openalex_work
from sage.summarize import summarize_text_abstractive
from sage.unpaywall import get_paper_info, download_paper

paper_openalex_works = {}
paper_infos = {}


async def get_paper_data(paper):
    sim_entity_id = paper[0]
    sim_score = paper[1]

    sim_openalex_work = await get_openalex_work(entity_id=sim_entity_id)
    paper_openalex_works[sim_entity_id] = sim_openalex_work

    sim_doi = sim_openalex_work.get("doi", None)
    if sim_doi:
        sim_paper_info = await get_paper_info(doi=sim_doi)
        paper_infos[sim_entity_id] = sim_paper_info

        sim_paper_title = sim_paper_info.get("title", None)
        if not sim_paper_title:
            sim_paper_title = sim_paper_info.get("doi", None)

        return f"{sim_paper_title} ({sim_score})"


async def main():
    """main function"""
    st.title("Sage")

    doi_input = st.text_input("DOI", "10.1038/s41586-021-03491-6")

    with st.spinner("Fetching paper info..."):
        paper_info = await get_paper_info(doi_input)

    if not paper_info:
        st.error("Invalid DOI")
        st.stop()

    st.header(paper_info["title"])
    st.markdown(f"[{paper_info['doi']}]({paper_info['doi_url']})")

    with st.expander("Full info"):
        st.json(paper_info)

    with st.spinner("Finding similar papers..."):
        similar_papers = await find_similar_papers(doi_input)

    with st.spinner("Loading similar papers..."):
        coroutines = [get_paper_data(paper) for paper in similar_papers]
        similar_paper_titles = await asyncio.gather(*coroutines)

    with st.expander("Similar papers"):
        for title in similar_paper_titles:
            st.write(title)

    with st.spinner("Downloading paper..."):
        download_path = await download_paper(doi_input)

    with open(download_path, "rb") as f:
        download_data = f.read()
    st.download_button("Download PDF", data=download_data, file_name=f"{doi_input}.pdf")

    with st.spinner("Summarizing paper..."):
        text = load_pdf_document(download_path)
        summary = await summarize_text_abstractive(text)

    st.header("Summary")
    st.write(summary)


if __name__ == "__main__":
    st.set_page_config(page_title="sage", page_icon="🎓", layout="wide")

    asyncio.run(main())
