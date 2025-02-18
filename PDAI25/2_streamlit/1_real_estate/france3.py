"""
This is the third step of the Streamlit tutorial.
We will add a selectbox to choose the year.
"""

import pandas as pd
import streamlit as st

# ADDITION: Move this to the top
st.title("Real estate prices in France")

# ADDITION: Now we can select the year through a selectbox
year = st.selectbox("Year to display:", [2019, 2020, 2021, 2022, 2023])

# ADDITION: So now the file name depends on the year
FILE = (
    f"https://files.data.gouv.fr/geo-dvf/latest/csv/{year}/"
    "departements/75.csv.gz"
)
df = pd.read_csv(FILE, compression="gzip", low_memory=False)

st.header("Raw data")
st.write("Streamlit app to display real estate prices in **Paris**")

only_sales = st.checkbox("Exclude non-sale transactions")

if only_sales:
    df = df[df["nature_mutation"] == "Vente"]

st.dataframe(df)

st.write(f"Number of rows: {df.shape[0]}")
