from setup import input_dir
import pandas as pd
import streamlit as st
from utils import keyword,format_str,get_biogrid,convert_df,filter_dataframe,make_arrow_compatible

@st.cache_data
def load_summary_df() -> pd.DataFrame:
    return pd.read_pickle(input_dir / "summary.pkl")


@st.cache_data
def load_biogrid_df() -> pd.DataFrame:
    return pd.read_pickle(input_dir / "BioGRID.pkl")


def filter_yeast():
    ### part1 summary and filtering
    st.markdown("We annnotate 1504 predicted PPIs in yeast by RossetaFold with three databases: *NCBI, Uniprot,SGD* and two pahtway enrichment databases: *KEGG* and *GO*.")
    df = load_summary_df()
    text_input = st.sidebar.text_area("Enter keywords 👇(ex. DNA damage, GO:0006412)")
    intersect = st.sidebar.checkbox("Intersection")
    keyword_list = format_str(text_input)
    

    if len(text_input) !=0:
        if intersect:
            df = keyword(df,keyword_list,intersect=True) 
        else:
            df = keyword(df,keyword_list)
    
    mode = st.selectbox('Selet the mode',('Filtering','Editing'))
    if mode == 'Filtering':
        df = filter_dataframe(df)
        st.dataframe(make_arrow_compatible(df), width="stretch")
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
    else:
        edited_df = st.data_editor(make_arrow_compatible(df), num_rows='dynamic')
        col1, col2, col3 , col4, col5 = st.columns(5)

        with col1:
            finish_editing = st.button('Finish editing')
        with col2:
            pass
        with col3 :
            pass
        with col4:
            pass
        with col5:
            exit_editing = st.button('Quit without saving')
        if finish_editing:
            edited_df.to_pickle(input_dir / 'summary.pkl')
            load_summary_df.clear()
        else:pass
        if exit_editing:
            pass
        df = load_summary_df()




    ### Part2, biogrid
    st.markdown('----')
    st.header("Related Literatures from Biogrid")
    biogrid_total = load_biogrid_df()
    biogrid_selected = get_biogrid(df_sum = biogrid_total,df_cand=df)
    check = st.checkbox("Show")
    if check:
        st.dataframe(make_arrow_compatible(biogrid_selected.reset_index(drop=True)), width="stretch")


    return df
