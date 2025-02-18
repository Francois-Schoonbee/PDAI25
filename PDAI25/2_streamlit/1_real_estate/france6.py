"""
This is the sixth step of the Streamlit tutorial.
We will add a map to display the location of the transactions.
"""

import pandas as pd
import pydeck as pdk  # ADDITION: Import PyDeck (neccessary for the map)
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

# ADDITION: Create new tab for map

tab_stats, tab_table, tab_map = st.tabs(["Stats", "Table", "Map"])

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

# ADDITION: New tab for map
with tab_map:
    st.header("Map of all properties")
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=df["latitude"].mean(),
                longitude=df["longitude"].mean(),
                zoom=10,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position=["longitude", "latitude"],
                    get_color=[200, 30, 0, 160],
                    get_radius=50,
                ),
            ],
        )
    )
