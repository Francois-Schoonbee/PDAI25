"""
This is the fifth step of the Streamlit tutorial.
We will add a tab to display statistics.
(This shows an alternative way of dealing with tabs)
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

# Create tabs

tab_stats, tab_table = st.tabs(["Stats", "Table"])

# ADDITION: We put everything we had under tab_table
# Now this is managed by referencing the tab_table object

tab_table.header("Raw data")
tab_table.write("Streamlit app to display real estate prices in **Paris**")
tab_table.write("[... The content is ommitted in this example ...]")

# Here should be the code we had before
# This is ommitted just for ease of understanding
# ...

# ADDITION: We add a new tab for statistics, also by referencing the object

tab_stats.header("Statistics")
tab_stats.write("[... The content is ommitted in this example ...]")
