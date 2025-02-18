"""
This is the second step of the Streamlit tutorial.
We will add basic interactivity through a checkbox
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

# ADDITION: Add checkbox to filter only sales
only_sales = st.checkbox("Exclude non-sale transactions")

# ADDITION: Retrieve the value of the checkbox and act accordingly
if only_sales:
    df = df[df["nature_mutation"] == "Vente"]

st.dataframe(df)

# ADDITION: Add some info (to better perceive the change)
st.write(f"Number of rows: {df.shape[0]}")
