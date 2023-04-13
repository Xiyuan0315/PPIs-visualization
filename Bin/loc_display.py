import streamlit as st
import pandas as pd
from setup import input_dir
from utils import merge_df,convert_df, filter_dataframe
def show_loc(df):
    st.write("Detailed location information of selected pairs")
    df_location = pd.read_pickle(input_dir / "YeastPair_Location.pkl")
    sel_location = merge_df(df=df_location, df_cand=df)
    sel_location = filter_dataframe(sel_location)
    st.dataframe(sel_location)

    csv = convert_df(sel_location.reset_index(drop = True))
    st.download_button(
    label="Download location file as CSV",
    data=csv,
    file_name='location.csv',
    mime="text/csv"
    )
