import streamlit as st
from pathlib import Path

folder_path = Path(r"Data\Player_Classes")
class_names = [f.stem for f in folder_path.glob("*.md")]
class_data = [f.read_text() for f in folder_path.glob("*.md")]


st.markdown("<h1 style='text-align: center;'>Player Classes</h1>", unsafe_allow_html=True)


tabs = st.tabs(class_names)

for i, tab in enumerate(tabs):
    with tab:
        st.markdown(class_data[i])