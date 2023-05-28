"""
Streamlit App

python -m streamlit run app.py
"""

import asyncio

import streamlit as st

from sage.openalex import find_similar_papers, get_openalex_work
from sage.unpaywall import get_paper_info

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
        return sim_paper_info
    return None


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
        similar_paper_infos = await asyncio.gather(*coroutines)

    sim_paper_checkboxes = {}

    st.header("Similar papers")
    for i, sim_paper_info in enumerate(similar_paper_infos):
        # Get title of similar paper
        sim_paper_title = sim_paper_info.get("title", None)
        if not sim_paper_title:
            sim_paper_title = sim_paper_info.get("doi", None)

        sim_paper_score = similar_papers[i][1]

        # Display checkbox for each similar paper
        checkbox = st.checkbox(f"{sim_paper_title} ({sim_paper_score})")
        sim_paper_checkboxes[sim_paper_title] = checkbox

    if st.button("Generate"):
        st.header("Selected papers")
        for sim_paper_title, checkbox in sim_paper_checkboxes.items():
            if checkbox:
                st.write(sim_paper_title)


if __name__ == "__main__":
    st.set_page_config(page_title="sage", page_icon="🎓", layout="wide")

    asyncio.run(main())
