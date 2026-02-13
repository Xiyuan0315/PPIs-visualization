import streamlit as st
from sum_display import filter_yeast
from homo_display import show_homo
from loc_display import show_loc
from pathway_display import get_pathway
from datetime import date
import pandas as pd
from setup import input_dir

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.write('<style>body { margin: 0; font-family: Arial, Helvetica, sans-serif;} .header{padding: 10px 16px; background: #555; color: #f1f1f1; position:fixed;top:0;} .sticky { position: fixed; top: 0; width: 100%;} </style><div class="header" id="myHeader">'+str(2)+'</div>', unsafe_allow_html=True)

@st.cache_data
def load_summary_pairs() -> pd.DataFrame:
    df = pd.read_pickle(input_dir / "summary.pkl")
    return df[["gene1", "gene2"]].copy()

def extract_gene_pairs(df: pd.DataFrame) -> pd.DataFrame | None:
    required_cols = {"gene1", "gene2"}
    if not required_cols.issubset(df.columns):
        st.error("Selected data must include 'gene1' and 'gene2' columns.")
        return None
    return df[["gene1", "gene2"]]


today = date.today()
st.title("PPI summary for yeast")
st.sidebar.image(f"{input_dir}/PPI.png", width="stretch")
page = st.sidebar.selectbox("Options", ("Yeast","Homo","Location","Pathway"))


if page == "Yeast":
    df = filter_yeast()
    st.session_state["filtered_df"] = df.copy()
    
elif page == "Pathway":
    get_pathway()
elif page == "Homo":
    df = st.session_state.get("filtered_df")
    if df is None:
        st.info("Using default summary pairs. Filter yeast pairs first to narrow the set.")
        df = load_summary_pairs()
    gene_pairs = extract_gene_pairs(df)
    if gene_pairs is not None:
        show_homo(gene_pairs)
else:
    df = st.session_state.get("filtered_df")
    if df is None:
        st.info("Using default summary pairs. Filter yeast pairs first to narrow the set.")
        df = load_summary_pairs()
    gene_pairs = extract_gene_pairs(df)
    if gene_pairs is not None:
        show_loc(gene_pairs)
st.sidebar.markdown(f"*:green[Edited by Xiyuan], modifyied on {today.strftime('%b %d, %Y')}*")
