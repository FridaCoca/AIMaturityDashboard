import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Results Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")

df = pd.read_excel(
    io='surveyResults.xlsx',
    engine='openpyxl',
    sheet_name='Sheet1',
    skiprows=0,
    usecols='E:BP',
    #nrows=2,
)

#---- SIDEBAR ----
strIdentifingColumn = "Unternehmen"
st.sidebar.header("Bitte hier auswählen:")
company = st.sidebar.multiselect(
    "Unternehmen auswählen:",
    options=df[strIdentifingColumn].unique(),
    #default=df[strIdentifingColumn].unique,
)

df_selection = df.query(
    "Unternehmen == @company"
)

#st.write(df)
st.dataframe(df_selection)
