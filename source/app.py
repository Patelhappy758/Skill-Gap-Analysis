import os
from io import BytesIO
from typing import Optional

import streamlit as st

from parser_pipeline import extract_text_auto


st.set_page_config(page_title="Milestone 1: Upload & Parse", layout="wide")

st.title("Document Upload & Parsing")
st.caption("Milestone 1: Data ingestion, parsing, and cleaned preview")


def save_uploaded_file(uploaded_file) -> Optional[str]:
    if not uploaded_file:
        return None
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    dest_path = os.path.join(upload_dir, uploaded_file.name)
    with open(dest_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return dest_path


left, right = st.columns([1, 2])

with left:
    st.subheader("Upload Documents")
    uploaded = st.file_uploader(
        "Drag-and-drop or browse",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=False,
    )
    parse_btn = st.button("Parse")

with right:
    st.subheader("Document Preview")
    tabs = st.tabs(["Raw", "Cleaned"])  # content filled after parse


if parse_btn and uploaded is not None:
    saved_path = save_uploaded_file(uploaded)
    try:
        raw_text, cleaned_text = extract_text_auto(saved_path)
        with right:
            with tabs[0]:
                st.text_area("Raw Text", value=raw_text, height=500)
            with tabs[1]:
                st.text_area("Cleaned Text", value=cleaned_text, height=500)
    except Exception as e:
        st.error(f"Failed to parse: {e}")

st.divider()
st.caption("Tip: Try the sample files in the repository's source folder.")

