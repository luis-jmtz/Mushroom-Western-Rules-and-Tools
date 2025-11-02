import streamlit as st
import pandas as pd


# load data
size_speed = pd.read_csv(r"Data\Size_Speed_Genotype.tsv", sep="\t")
geno_traits =  pd.read_csv(r"Data\Genotype_Traits.tsv", sep="\t", escapechar='\\')
sizes = pd.read_csv(r"Data\size_list.csv", header=None).iloc[0].tolist() # loads in the sizes which is single line csv

geno_traits["description"] = geno_traits["description"].str.replace(r'\\n', '\n', regex=True) #ensures new-line characters are read correclty

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

        geno_size = ss_row["size"].iloc[0]
        geno_speed = str(ss_row["speed"].iloc[0])

        st.write("Size: "+ sizes[geno_size])
        st.write("Speed: " + geno_speed)


        for index, row in geno_traits.iterrows():
            if row.isCore == 1 and row.genotype_id == i+1:
                st.write(row.description)

        st.write("### Secondary Traits")

        for index, row in geno_traits.iterrows():
            if row.isCore == 0 and row.genotype_id == i+1:
                st.write(row.description)
