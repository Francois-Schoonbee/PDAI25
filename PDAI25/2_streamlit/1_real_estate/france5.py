"""
This is the fifth step of the Streamlit tutorial.
We will add a tab to display statistics.
"""

import pandas as pd
import streamlit as st

st.title("Real estate prices in France")

year = st.sidebar.selectbox(
    "Year to display:",
    [2019, 2020, 2021, 2022, 2023]
    )

department = st.sidebar.selectbox("Department to display:", [75, 92, 93, 94])

FILE = (
    f"https://files.data.gouv.fr/geo-dvf/latest/csv/{year}/"
    f"departements/{department}.csv.gz"
)
df = pd.read_csv(FILE, compression="gzip", low_memory=False)

median_price = df["valeur_fonciere"].median()
st.sidebar.write(f"Median price: {median_price:.0f} €")

# ADDITION: Create tabs

tab_stats, tab_table = st.tabs(["Stats", "Table"])

# ADDITION: We put everything we had under tab_table
# Note this is managed with the syntax of a context manager
with tab_table:

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

# ADDITION: We add a new tab for statistics

with tab_stats:
    st.header("Statistics")
    filtered_df = df[[
        "valeur_fonciere",
        "surface_reelle_bati",
        "nombre_pieces_principales"
        ]]
    filtered_df = filtered_df.dropna()
    st.write(filtered_df.describe().transpose().drop(["count", "std"], axis=1))

    st.header("Bar charts")

    # Add radio button to select between price and surface
    price_or_surface = st.radio("Price or surface", ["price", "surface"])

    if price_or_surface == "price":
        # Display a bar chart with average price per number of rooms
        bar_data = filtered_df[[
            "nombre_pieces_principales",
            "valeur_fonciere"
            ]].groupby("nombre_pieces_principales")\
            .median()\
            .reset_index()
        st.bar_chart(
            bar_data,
            x="nombre_pieces_principales",
            y="valeur_fonciere"
            )
    else:
        # Display a bar chart with average surface per number of rooms
        bar_data = filtered_df[[
            "nombre_pieces_principales",
            "surface_reelle_bati"
            ]].groupby("nombre_pieces_principales")\
            .median()\
            .reset_index()
        st.bar_chart(
            bar_data,
            x="nombre_pieces_principales",
            y="surface_reelle_bati"
            )
