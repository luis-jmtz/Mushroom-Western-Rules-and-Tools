import streamlit as st
import pandas as pd

# load data
size_speed = pd.read_csv(r"Data\Size_Speed_Genotype.tsv", sep="\t")
geno_traits =  pd.read_csv(r"Data\Genotype_Traits.tsv", sep="\t")

# defines the tabs that will be presented and used
tab_labels = []
for row in size_speed.itertuples():
    tab_labels.append(row.name)
tab_labels.pop(0)

# intializes a string that the other functions will modify
display_text = ""


def get_geno_values(geno_id):
    pass


tabs = st.tabs(tab_labels)


# Populates each tab
for i, tab in enumerate(tabs):
    with tab:
        geno_name = tab_labels[i]
        st.write(geno_name)
        curr_geno_id = int(size_speed.loc[size_speed["name"] == geno_name].get("genotype_id")) # where the name column = the geno name, get the respective id and then cast it to an integer
        st.write(curr_geno_id)
        get_geno_values(curr_geno_id)