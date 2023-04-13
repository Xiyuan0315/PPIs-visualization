import pandas as pd
from setup import input_dir
from utils import convert_df,merge_df,filter_dataframe,get_biogrid_homo
import streamlit as st

def show_homo(df: pd.DataFrame):

    st.write("homologous genes of selected list")
    df_homo = pd.read_pickle(input_dir / "summary_homo.pkl")
    sel_homo = merge_df(df=df_homo, df_cand=df)

    sel_homo = filter_dataframe(sel_homo)
    st.dataframe(sel_homo.reset_index(drop = True))

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
    biogrid_total = pd.read_pickle(input_dir / "BioGRID_homo.pkl")
    biogrid_selected = get_biogrid_homo(df_sum = biogrid_total,df_cand=sel_homo)
    check = st.checkbox("Show")
    if check:
        st.write(biogrid_selected.reset_index(drop=True))
