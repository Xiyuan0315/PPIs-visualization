import streamlit as st
import pandas as pd
from setup import input_dir
from utils import merge_df,convert_df, filter_dataframe,make_arrow_compatible

@st.cache_data
def load_location_df() -> pd.DataFrame:
    return pd.read_pickle(input_dir / "YeastPair_Location.pkl")

def show_loc(df):
    st.write("Detailed location information of selected pairs")
    df_location = load_location_df()
    sel_location = merge_df(df=df_location, df_cand=df)
    sel_location = filter_dataframe(sel_location)
    st.dataframe(make_arrow_compatible(sel_location), width="stretch")

    csv = convert_df(sel_location.reset_index(drop = True))
    st.download_button(
    label="Download location file as CSV",
    data=csv,
    file_name='location.csv',
    mime="text/csv"
    )
