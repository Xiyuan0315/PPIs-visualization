from setup import input_dir
import pandas as pd
import streamlit as st
from utils import keyword,format_str,get_biogrid,convert_df,filter_dataframe

def filter_yeast():
    ### part1 summary and filtering
    st.markdown("We annnotate 1504 predicted PPIs in yeast by RossetaFold with three databases: *NCBI, Uniprot,SGD* and two pahtway enrichment databases: *KEGG* and *GO*.")
    df = pd.read_pickle(input_dir / "summary.pkl")
    text_input = st.sidebar.text_area("Enter keywords 👇(ex. DNA damage, GO:0006412)")
    intersect = st.sidebar.checkbox("Intersection")
    keyword_list = format_str(text_input)
    

    if len(text_input) !=0:
        if intersect:
            df = keyword(df,keyword_list,intersect=True) 
        else:
            df = keyword(df,keyword_list)
    
    # df = pd.util.hash_pandas_object(df)
    df = filter_dataframe(df)
    st.write(df)
    csv = convert_df(df.reset_index(drop = True))
    col1, col2, col3 , col4, col5 = st.columns(5)
    with col1:
        pass
    with col2:
        pass
    with col3 :
        pass
    with col4:
        pass
    with col5:
        st.download_button(
        label="Download",
        data=csv,
        file_name='summary.csv',
        mime="text/csv"
    )



    ### Part2, biogrid
    st.markdown('----')
    st.header("Related Literatures from Biogrid")
    biogrid_total = pd.read_pickle(input_dir / "BioGRID.pkl")
    biogrid_selected = get_biogrid(df_sum = biogrid_total,df_cand=df)
    check = st.checkbox("Show")
    if check:
        st.write(biogrid_selected.reset_index(drop=True))


    return df

