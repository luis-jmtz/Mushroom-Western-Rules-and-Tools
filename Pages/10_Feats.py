import streamlit as st

from pathlib import Path

file_path = Path(r"Data\Feats_Text.md")
contents = file_path.read_text()
st.markdown(contents, unsafe_allow_html=True)
