"""
This is the third step (part b) of the Streamlit tutorial.
We will add a text input to filter by street name.
"""

import pandas as pd
import streamlit as st


st.title("Real estate prices in France")

year = st.selectbox("Year to display:", [2019, 2020, 2021, 2022, 2023])

FILE = (
    f"https://files.data.gouv.fr/geo-dvf/latest/csv/{year}/"
    "departements/75.csv.gz"
)
df = pd.read_csv(FILE, compression="gzip", low_memory=False)

st.header("Raw data")
st.write("Streamlit app to display real estate prices in **Paris**")

only_sales = st.checkbox("Exclude non-sale transactions")

street_name = st.text_input("Filter by street name", "")

if street_name:
    df.dropna(subset=["adresse_nom_voie"], inplace=True)
    df = df[df["adresse_nom_voie"].str.contains(street_name, case=False)]

if only_sales:
    df = df[df["nature_mutation"] == "Vente"]

st.dataframe(df)

st.write(f"Number of rows: {df.shape[0]}")
