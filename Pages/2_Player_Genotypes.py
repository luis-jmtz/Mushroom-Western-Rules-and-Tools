import streamlit as st
import pandas as pd

# load data
size_speed = pd.read_csv(r"Data\Size_Speed_Genotype.tsv", sep="\t")
geno_traits =  pd.read_csv(r"Data\Genotype_Traits.tsv", sep="\t", escapechar='\\')

geno_traits["description"] = geno_traits["description"].str.replace(r'\\n', '\n', regex=True) #ensures new-line characters are read correclty

# Size List: Used for converting numerical size value to text

# defines the tabs that will be presented and used
tab_labels = []
for row in size_speed.itertuples():
    tab_labels.append(row.name)
tab_labels.pop(0)


tabs = st.tabs(tab_labels)


# Populates each tab
for i, tab in enumerate(tabs):
    with tab:
        geno_name = tab_labels[i]
        st.header(geno_name)
        # curr_geno_id = int(size_speed.loc[size_speed["name"] == geno_name].get("genotype_id")) # where the name column = the geno name, get the respective id and then cast it to an integer
        # st.write(curr_geno_id)

        st.write("### Core Traits")

        ss_row = size_speed[size_speed["genotype_id"] == i+1] # size, speed row

        st.write(ss_row)
        


        for index, row in geno_traits.iterrows():
            if row.isCore == 1 and row.genotype_id == i+1:
                st.write(row.description)

        st.write("### Secondary Traits")

        for index, row in geno_traits.iterrows():
            if row.isCore == 0 and row.genotype_id == i+1:
                st.write(row.description)
