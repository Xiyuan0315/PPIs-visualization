import streamlit as st
import pandas as pd
from utils import format_str,make_arrow_compatible
from setup import input_dir

@st.cache_data
def load_pathway_df() -> pd.DataFrame:
    go = pd.read_pickle(input_dir / "go.pkl")
    kegg = pd.read_pickle(input_dir / "kegg.pkl")
    return pd.concat([go, kegg], axis=0)

### Part3-GO, KEGG
def get_pathway():
    df = load_pathway_df()
    st.write("Genes involved in given pathways") 
    pathway_input = st.text_area("Input your intersted pathway: ","GO:0000006, sce04213")
    pathway_list = format_str(pathway_input) 
    
    col1, col2, col3 , col4, col5 = st.columns(5)

    with col1:
        pass
    with col2:
        pass
    with col4:
        pass
    with col5:
        check = st.button("Check!")
    with col3 :
        pass
    if check:  
        if len(pathway_input) !=0:
            st.dataframe(make_arrow_compatible(df[df['ID'].isin(pathway_list)]), width="stretch")
