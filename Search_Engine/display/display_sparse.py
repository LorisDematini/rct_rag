import os
import streamlit as st
import matplotlib.pyplot as plt

from .highlight import highlight_text_sparse
from .display_utils import find_pdf_file, get_summary_data
from config import validate, show_section, download_label, title_graph, x_label, y_label, format_protocol, no_text_p, no_protocol_query, no_pdf_avail

summary_data = get_summary_data()

def display_scores_chart(results: list[dict]) -> None:
    """
    Display a bar chart of similarity scores for each study.

    Args:
        results (list of dict): Each dict contains "study_id" and "score".
    """
    study_ids = [r["study_id"] for r in results]
    scores = [r["score"] for r in results]
    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.bar(study_ids, scores, color='skyblue')
    ax.set(
        title= title_graph, 
        xlabel= x_label,
        ylabel= y_label,
        ylim=(0, max(scores) * 1.1)
    )
    # Rotate x labels if too many
    if len(study_ids) > 5:
        ax.set_xticks(range(len(study_ids)))
        ax.set_xticklabels(study_ids, rotation=45, ha='right')
    st.pyplot(fig)


def display_study_sections(
    sections: dict | None,
    query: str,
    cleaned_query: str | None = None,
    mode: str = "sparse",
) -> None:
    """
    Display detailed sections of a study with highlighted matches.

    Args:
        sections (dict or None): Sections and paragraphs keyed by section title.
        query (str): Original user query.
        cleaned_query (str, optional): Preprocessed query for highlighting.
        mode (str): Display mode; "sparse" applies highlighting.
    """
    if not isinstance(sections, dict):
        st.warning(format_protocol)
        return

    for title_sec, paragraphs in sections.items():
        if not paragraphs:
            continue
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"**{title_sec}**")
        with col2:
            for p in paragraphs if isinstance(paragraphs, list) else [paragraphs]:
                if not isinstance(p, str):
                    st.markdown(no_text_p)
                    continue
                if mode == "sparse":
                    # Highlight matching query terms
                    st.markdown(
                        highlight_text_sparse(p, query, cleaned_query),
                        unsafe_allow_html=True,
                    )


def display_sparse_results(
    results: list[dict],
    query: str,
    query_cleaned: str,
    top_terms_by_study: dict | None = None
) -> None:
    """
    Display the results of sparse TF-IDF search with highlights, scores, and downloads.

    Args:
        results (list of dict): Search results containing study_id, score, document.
        query (str): Original user query.
        query_cleaned (str): Preprocessed query.
        top_terms_by_study (dict, optional): Dict mapping study_id to list of top terms with scores.
    """
    if "validated_warning" not in st.session_state:
        st.session_state.validated_warning = False

    # Show the cleaned query as a warning, and wait for user confirmation
    if not st.session_state.validated_warning:
        st.warning(f"Processed query: `{query_cleaned}`")
        if not st.button(validate):
            st.stop()
    st.session_state.validated_warning = False

    st.subheader(f"{len(results)} / {len(summary_data)} protocols found")
    if not results:
        st.info(no_protocol_query)
        return

    display_scores_chart(results)

    for res in results:
        study_id = res["study_id"]
        score = res["score"]
        # Color coding score: green >0.2, orange >0.1, else red
        color = "green" if score > 0.2 else "orange" if score > 0.1 else "red"
        st.markdown(
            f"### {study_id} — Score: "
            f"<span style='color:{color}'><b>{score:.2f}</b></span>",
            unsafe_allow_html=True,
        )

        if top_terms_by_study and study_id in top_terms_by_study:
            top_terms = top_terms_by_study[study_id]
            terms = ", ".join(f"**{term}** (`{s:.2f}`)" for term, s in top_terms)
            st.markdown(f"**Important terms:** {terms}")

            pdf_path = find_pdf_file(study_id)
            if pdf_path:
                with open(pdf_path, "rb") as file:
                    st.download_button(
                        label=download_label,
                        data=file,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf",
                    )
            else:
                st.info(no_pdf_avail)

        with st.expander(show_section):
            display_study_sections(
                summary_data.get(study_id), query, query_cleaned, mode="sparse"
            )