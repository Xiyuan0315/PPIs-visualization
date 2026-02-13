import pandas as pd
import streamlit as st
from typing import Sequence
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import re


def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    # modify = st.checkbox("Add filters")

    # if not modify:
    #     return df

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
                if _max == _min:
                    right.write(f"Only value: {_min}")
                    continue
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
                    col_as_text = df[column].astype(str)
                    try:
                        df = df[col_as_text.str.contains(user_text_input, na=False, regex=True)]
                    except re.error:
                        df = df[col_as_text.str.contains(user_text_input, na=False, regex=False)]

    return df

@st.cache_data()
def keyword(
    df: pd.DataFrame,
    keywords: list,
    intersect: bool = False,
    search_columns: Sequence[str] | None = None,
):
    default_search_columns = [
        "GO_pathway1",
        "GO_pathway2",
        "NCBI_Summary1",
        "SGD_Description1",
        "SGD_Description2",
        "Uniprot_Function1",
        "Uniprot_Function2",
        "KEGG_pathway1",
        "KEGG_pathway2",
    ]
    if search_columns is None:
        search_columns = default_search_columns

    valid_keywords = [k.strip().lower() for k in keywords if k.strip()]
    if not valid_keywords:
        return df.reset_index(drop=True)

    available_columns = [c for c in search_columns if c in df.columns]
    if not available_columns:
        return df.iloc[0:0].copy()

    searchable = (
        df[available_columns]
        .fillna("")
        .astype(str)
        .agg(" ".join, axis=1)
        .str.lower()
    )

    if intersect:
        mask = pd.Series(True, index=df.index)
        for key in valid_keywords:
            mask = mask & searchable.str.contains(key, regex=False, na=False)
    else:
        mask = pd.Series(False, index=df.index)
        for key in valid_keywords:
            mask = mask | searchable.str.contains(key, regex=False, na=False)

    return df.loc[mask].reset_index(drop=True)

def format_str(text:str):
    result = []
    for term in text.split(','):
        normalized = " ".join(term.split())
        if normalized:
            result.append(normalized)
    return result

@st.cache_data 
def convert_df(df):
    return df.to_csv().encode('utf-8')

def make_arrow_compatible(df: pd.DataFrame) -> pd.DataFrame:
    """
    Streamlit uses PyArrow for dataframe transport. Mixed python types inside an
    object column (e.g. ints + bytes + strings) can fail Arrow conversion.
    Normalize only problematic object columns for display/editor operations.
    """
    safe_df = df.copy(deep=True)
    for col in safe_df.columns:
        if not is_object_dtype(safe_df[col]):
            continue
        series = safe_df[col]
        non_null = series[series.notna()]
        if non_null.empty:
            continue

        has_bytes = non_null.map(
            lambda v: isinstance(v, (bytes, bytearray, memoryview))
        ).any()
        if has_bytes:
            series = series.map(
                lambda v: v.decode("utf-8", errors="replace")
                if isinstance(v, (bytes, bytearray, memoryview))
                else v
            )
            safe_df[col] = series
            non_null = series[series.notna()]

        if non_null.map(type).nunique() > 1:
            safe_df[col] = series.map(lambda v: str(v) if pd.notna(v) else v)

    return safe_df

def get_pair_reverse(df):
    """
    Joint the first and the second columns as string
    """
    return df['gene2'].astype(str) + "|" + df['gene1'].astype(str)
def get_pair(df):
    """
    Joint the first and the second columns as string
    """
    return df['gene1'].astype(str) + "|" + df['gene2'].astype(str)

def get_biogrid(df_sum,df_cand):

    # Add joint pairs as pair into df_sum
    candidates = get_pair(df_cand)
    candidates_r = get_pair_reverse(df_cand)
    candidates = pd.concat([candidates,candidates_r], ignore_index=True)
    df_sum_pairs = df_sum.assign(
        pair=df_sum['Official.Symbol.Interactor.A'].astype(str) + "|" + df_sum['Official.Symbol.Interactor.B'].astype(str)
    )
    # Filter the pairs of candidates from the DDR.xlsx
    candidates_info = df_sum_pairs[df_sum_pairs['pair'].isin(candidates)] 
    # Drop the jointed genes and save as excel file
    return candidates_info.drop(columns = ['pair'])

def get_biogrid_homo(df_sum,df_cand):

    # Add joint pairs as pair into df_sum
    candidates = df_cand['HOMO_gene_name1'].astype(str) + "|" + df_cand['HOMO_gene_name2'].astype(str)
    candidates_r = df_cand['HOMO_gene_name2'].astype(str) + "|" + df_cand['HOMO_gene_name1'].astype(str)
    candidates = pd.concat([candidates,candidates_r], ignore_index=True)
    df_sum_pairs = df_sum.assign(
        pair=df_sum['Official.Symbol.Interactor.A'].astype(str) + "|" + df_sum['Official.Symbol.Interactor.B'].astype(str)
    )
    # Filter the pairs of candidates from the DDR.xlsx
    candidates_info = df_sum_pairs[df_sum_pairs['pair'].isin(candidates)] 
    # Drop the jointed genes and save as excel file
    return candidates_info.drop(columns = ['pair'])
    
def merge_df(df,df_cand):

    # Add joint pairs as pair into df_sum
    candidates = get_pair(df_cand)
    candidates_r = get_pair_reverse(df_cand)
    candidates = pd.concat([candidates,candidates_r], ignore_index=True)
    df_pairs = df.assign(pair=df['gene1'].astype(str) + "|" + df['gene2'].astype(str))
    candidates_info = df_pairs[df_pairs['pair'].isin(candidates)] 
    return candidates_info.drop(columns = ['pair'])
