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
    skiprows=2,
    usecols='E:BP',
    nrows=2,
)
print(df)


daten = Path(__file__).parents[1] / 'surveyResults.xlsx'
print(daten)
st.write(df)
