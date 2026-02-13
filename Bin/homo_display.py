import pandas as pd
from setup import input_dir
from utils import (
    convert_df,
    merge_df,
    filter_dataframe,
    get_biogrid_homo,
    make_arrow_compatible,
    keyword,
    format_str,
)
import streamlit as st

@st.cache_data
def load_homo_summary() -> pd.DataFrame:
    return pd.read_pickle(input_dir / "summary_homo.pkl")


@st.cache_data
def load_homo_biogrid() -> pd.DataFrame:
    return pd.read_pickle(input_dir / "Biogrid_homo.pkl")


def show_homo(df: pd.DataFrame):

    st.write("homologous genes of selected list")
    df_homo = load_homo_summary()
    sel_homo = merge_df(df=df_homo, df_cand=df)
    text_input = st.sidebar.text_area(
        "Enter keywords 👇(ex. DNA damage, GO:0006412)",
        key="homo_keyword_input",
    )
    intersect = st.sidebar.checkbox("Intersection", key="homo_intersection")
    keyword_list = format_str(text_input)

    if len(text_input) != 0:
        homo_search_columns = (
            "SGD_description1",
            "SGD_description2",
            "Alias_symbols1",
            "Alias_symbols2",
            "Alliance_description1",
            "Alliance_description2",
            "NCBI_summary1",
            "NCBI_summary2",
            "PathCard_pathway1",
            "PathCard_pathway2",
            "KEGG_pathway1",
            "KEGG_pathway2",
            "Reactome_pathway1",
            "Reactome_pathway2",
            "Uniprot_function1",
            "Uniprot_function2",
            "GDC_disease1",
            "GDC_disease2",
            "Pubmed_id1",
            "Pubmed_id2",
        )
        sel_homo = keyword(
            sel_homo,
            keyword_list,
            intersect=intersect,
            search_columns=homo_search_columns,
        )

    sel_homo = filter_dataframe(sel_homo)
    st.dataframe(make_arrow_compatible(sel_homo.reset_index(drop = True)), width="stretch")

    csv = convert_df(sel_homo.reset_index(drop = True))

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
        file_name='homo.csv',
        mime="text/csv"
        )


    st.markdown('----')
    st.header("Related Literatures from Biogrid")
    biogrid_total = load_homo_biogrid()
    biogrid_selected = get_biogrid_homo(df_sum = biogrid_total,df_cand=sel_homo)
    check = st.checkbox("Show")
    if check:
        st.dataframe(make_arrow_compatible(biogrid_selected.reset_index(drop=True)), width="stretch")
