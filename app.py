"""
Streamlit App

python -m streamlit run app.py
"""

import asyncio
from functools import cache
from multiprocessing import Pool
from multiprocessing import cpu_count

import streamlit as st
import streamlit.components.v1 as components
from aiocache import cached

from sage.document import load_pdf_document, Document
from sage.openalex import find_similar_papers, get_openalex_work
from sage.summarize import summarize_text_abstractive
from sage.unpaywall import get_paper_info, download_paper, get_paper_authors
from sage.utils import safe_filename
from sage.viz import str_to_embeddings, visualize, add_multiple

paper_openalex_works = {}  # entity_id -> openalex_work
paper_infos = {}  # entity_id -> paper_info
paper_texts = {}  # doi -> text
paper_summaries = {}  # doi -> summary


@cached()
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


@cache
def summarize_worker(doi: str, text: str) -> tuple[str, str]:
    try:
        return doi, summarize_text_abstractive(doi=doi, text=text[:124999])
    except Exception as e:
        print(e)
        return doi, "error summarizing"


async def main():
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
        sim_paper_checkboxes[sim_paper_info["doi"]] = checkbox

    if st.button("Generate"):
        st.header("Selected papers")
        selected_papers = [
            sim_paper_doi
            for sim_paper_doi, checkbox in sim_paper_checkboxes.items()
            if checkbox
        ]

        with st.spinner("Downloading papers..."):
            coroutines = [download_paper(doi) for doi in [doi_input, *selected_papers]]
            downloaded_papers = await asyncio.gather(*coroutines)

        loaded_paper_texts_progress = st.progress(0)
        for i, downloaded_paper in enumerate(downloaded_papers):
            if downloaded_paper:
                # Update to use doi instead of filename
                paper_texts[downloaded_paper.stem] = load_pdf_document(downloaded_paper)
            loaded_paper_texts_progress.progress((i + 1) / len(downloaded_papers))

        with st.spinner("Analyzing papers..."):
            with Pool(cpu_count()) as p:
                sim_paper_summaries = p.starmap(summarize_worker, list(paper_texts.items()))

        paper_summaries.update({safe_filename(doi): summary for doi, summary in sim_paper_summaries})

        for i, (doi, summary) in enumerate(sim_paper_summaries):
            st.subheader(f"{doi} ({similar_papers[i][1]})")
            st.write(summary)

        st.header("Visualization")

        # Build the document objects
        docs = []
        for doi in [doi_input, *selected_papers]:
            openalex_work = await get_openalex_work(doi=doi)
            entity_id = openalex_work.get("id", None)

            try:
                if entity_id in paper_infos:
                    authors = await get_paper_authors(doi=doi)

                    docs.append(
                        Document(
                            name=safe_filename(doi),
                            title=paper_infos[entity_id]["title"],
                            url=paper_infos[entity_id]["doi_url"],
                            text=paper_texts[safe_filename(doi)],
                            summary=paper_summaries[safe_filename(doi)],
                            doi=doi,
                            date=paper_infos[entity_id]["published_date"],
                            authors=authors,
                        )
                    )
            except KeyError as e:
                print(e)

        add_multiple(docs)

        # Embed the documents
        embeddings = []
        with st.spinner("Embedding papers..."):
            for doc in docs:
                embeddings.append(str_to_embeddings(doc.text[:1000]))

        # Display the embeddings
        components.iframe(visualize(embeddings_vectors=embeddings, metadatas=docs), height=600)


if __name__ == "__main__":
    st.set_page_config(page_title="sage", page_icon="🎓", layout="wide")

    asyncio.run(main())
