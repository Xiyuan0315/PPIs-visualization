import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype
)
import functools


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy(deep=True)

    # # Try to convert datetimes into a standard format (datetime, no timezone)
    # for col in df.columns:
    #     if is_object_dtype(df[col]):
    #         try:
    #             df[col] = pd.to_datetime(df[col])
    #         except Exception:
    #             pass

    #     if is_datetime64_any_dtype(df[col]):
    #         df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df
@st.cache_data()
def keyword(df,keywords:list, intersect = False):
    df_list = []

    for key in keywords:
        # DNA damage
        df_sub = pd.DataFrame(columns = df.columns) # create header of Dataframe
        for i in df.index:
            if key.lower() in (str(df["GO_pathway1"][i]) + str(df["GO_pathway2"][i]) + str(df["NCBI_Summary1"][i]) + str(df["SGD_Description1"][i]) + str(df["SGD_Description2"][i])+ str(df["Uniprot_Function1"][i]) + str(df["Uniprot_Function1"][i]) + str(df["KEGG_pathway1"]) + str(df["KEGG_pathway2"])).lower():
                df_sub.loc[len(df_sub)] = df.loc[i].tolist() 
        df_list.append(df_sub)
    if intersect:
        df_sum = functools.reduce(lambda x, y: pd.merge(x, y, how='inner'), df_list)
    else:
        df_sum = pd.concat(df_list).drop_duplicates()
    
    return df_sum.reset_index(drop=True)

def format_str(text:str):
    term_list = text.split(',')
    result = []
    for i in range(len(term_list)):
        l = term_list[i].split()
        result.append(" ".join(l))
    return result

@st.cache_data 
def convert_df(df):
    return df.to_csv().encode('utf-8')


def get_pair_reverse(df):
    """
    Joint the first and the second columns as string
    """
    return df['gene2'].astype(str) + df['gene1']
def get_pair(df):
    """
    Joint the first and the second columns as string
    """
    return df['gene1'].astype(str) + df['gene2']

def get_biogrid(df_sum,df_cand):

    # Add joint pairs as pair into df_sum
    candidates = get_pair(df_cand)
    candidates_r = get_pair_reverse(df_cand)
    candidates = pd.concat([candidates,candidates_r])
    df_sum['pair'] = df_sum['Official.Symbol.Interactor.A'].astype(str) + df_sum['Official.Symbol.Interactor.B']
    # Filter the pairs of candidates from the DDR.xlsx
    candidates_info = df_sum[df_sum['pair'].isin(candidates)] 
    # Drop the jointed genes and save as excel file
    return candidates_info.drop(columns = ['pair'])

def get_biogrid_homo(df_sum,df_cand):

    # Add joint pairs as pair into df_sum
    candidates = df_cand['HOMO_gene_name1'].astype(str) + df_cand['HOMO_gene_name2'].astype(str)
    candidates_r = df_cand['HOMO_gene_name2'].astype(str) + df_cand['HOMO_gene_name1'].astype(str)
    candidates = pd.concat([candidates,candidates_r])
    df_sum['pair'] = df_sum['Official.Symbol.Interactor.A'].astype(str) + df_sum['Official.Symbol.Interactor.B']
    # Filter the pairs of candidates from the DDR.xlsx
    candidates_info = df_sum[df_sum['pair'].isin(candidates)] 
    # Drop the jointed genes and save as excel file
    return candidates_info.drop(columns = ['pair'])
    
def merge_df(df,df_cand):

    # Add joint pairs as pair into df_sum
    candidates = get_pair(df_cand)
    candidates_r = get_pair_reverse(df_cand)
    candidates = pd.concat([candidates,candidates_r], ignore_index=True)
    df['pair'] = df['gene1'].astype(str) + df['gene2']
    # Filter the pairs of candidates from the DDR.xlsx
    candidates_info = df[df['pair'].isin(candidates)] 
    # Drop the jointed genes and save as excel file
    return candidates_info.drop(columns = ['pair'])
