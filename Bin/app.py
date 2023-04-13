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

today = date.today()
st.title("PPI summary for yeast")
st.sidebar.image(f"{input_dir}/PPI.png",use_column_width=True)
page = st.sidebar.selectbox("Options", ("Yeast","Homo","Location","Pathway"))


if page == "Yeast":
    df = filter_yeast()
    df.to_pickle("filtered.pkl")
    
elif page == "Pathway":
    get_pathway()
elif page == "Homo":
    df = pd.read_pickle('filtered.pkl')
    show_homo(df[['gene1','gene2']])
else:
    df = pd.read_pickle('filtered.pkl')
    show_loc(df[['gene1','gene2']])
st.sidebar.markdown(f"*:green[Edited by Xiyuan], modifyied on {today.strftime('%b %d, %Y')}*")
