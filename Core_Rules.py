import streamlit as st

st.title("Mushroom Western Core Rules")


rules_text = r"Data\Core_Rules.md"

with open(rules_text, 'r', encoding='utf-8') as f:
        # Read the entire contents into a single string variable
        rules_string = f.read()

st.markdown(rules_string)