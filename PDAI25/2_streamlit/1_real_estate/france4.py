"""
This is the third step of the Streamlit tutorial.
We will add a selectbox to choose the year.
"""

import pandas as pd
import streamlit as st

st.title("Real estate prices in France")

# ADDITION: Let's move year selection to a sidebar
year = st.sidebar.selectbox(
    "Year to display:",
    [2019, 2020, 2021, 2022, 2023]
)

# ADDITION: Since we have a sidebar, why not add the department selection?
department = st.sidebar.selectbox("Department to display:", [75, 92, 93, 94])

# ADDITION: Make the file name depend on the year and department
FILE = (
    f"https://files.data.gouv.fr/geo-dvf/latest/csv/{year}/"
    f"departements/{department}.csv.gz"
)
df = pd.read_csv(FILE, compression="gzip", low_memory=False)

# ADDITION: Why not add the median price of the department to this sidebar?
median_price = df["valeur_fonciere"].median()
st.sidebar.write(f"Median price: {median_price:.0f} €")


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
