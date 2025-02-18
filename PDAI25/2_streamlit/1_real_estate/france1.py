"""
Base example for a streamlit app.
Simply display the raw data.
"""

import pandas as pd
import streamlit as st

FILE = (
    "https://files.data.gouv.fr/geo-dvf/latest/csv/2022/"
    "departements/75.csv.gz"
)
df = pd.read_csv(FILE, compression="gzip", low_memory=False)
st.title("Real estate prices in France")

st.header("Raw data")
st.write("Streamlit app to display real estate prices in **Paris**")

st.dataframe(df)
