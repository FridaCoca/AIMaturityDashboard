import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Results Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")

df = pd.read_excel(
    io='surveyResults.xlsx',
    engine='openpyxl',
    sheet_name='Sheet2',
    skiprows=0,
    # usecols='E:BP',
    # nrows=2,
)

dfP = pd.read_excel(
    io='surveyResults.xlsx',
    engine='openpyxl',
    sheet_name='Sheet3',
    # skiprows= 1,
    # usecols='E:BP',
    # nrows=2,
)

# --- Sidebar ---
st.sidebar.header("Bitte hier auswählen:")

strIdentifingColumn = "Unternehmen"
company = st.sidebar.multiselect(
    "Unternehmen auswählen:",
    options=df[strIdentifingColumn].unique(),
    # default=df[strIdentifingColumn].unique
)

strIdentifingColumn = "Gestaltungsdimension"
dimension = st.sidebar.multiselect(
    "Unternehmen auswählen:",
    options=df[strIdentifingColumn].unique(),
    # default=df[strIdentifingColumn].unique
)

dfSelection = df.query(
    "Unternehmen == @company & Gestaltungsdimension == @dimension"
)

st.write(df)
st.dataframe(dfSelection)
st.write(dfP)

# --- Mainpage ---
st.title(":bar_chart: Reifegrad Dashboard")
st.markdown("##")

# --- Maturity Analysis ---
total_points = dfSelection['Punkte'].sum()

# Points by Dimension [Bar Chart]
pointsByDimensions = (
    dfSelection.groupby(by=["Gestaltungsdimension"]).sum()[["Punkte"]]
)
figPointsDimension = px.bar(
    pointsByDimensions,
    x="Punkte",
    y=pointsByDimensions.index,
    orientation="h",
    title="<b>Punkte nach Gestaltungsdimension </b>",
    color_discrete_sequence=["#0083B8"] * len(pointsByDimensions),
    template="plotly_white",
)

st.plotly_chart(figPointsDimension)


def setup_radar():
    """
    Starts the radar charts
    :param var_number:
    """
    global COLORS, companiesArray, ANGLES, fig, ax, var_number
    BG_WHITE = "#fbf9f4"
    BLUE = "#2a475e"
    GREY70 = "#b3b3b3"
    GREY_LIGHT = "#f2efe8"
    COLORS = ["#FF5A5F", "#FFB400", "#007A87"]
    # The three species of penguins
    companiesArray = dfP["Unternehmen"].values.tolist()
    print("Unternehmen:", companiesArray)

    # The angles at which the values of the numeric variables are placed
    ANGLES = [n / var_number * 2 * np.pi for n in range(var_number)]
    ANGLES += ANGLES[:1]
    # Padding used to customize the location of the tick labels
    X_VERTICAL_TICK_PADDING = 5
    X_HORIZONTAL_TICK_PADDING = 50
    # Angle values going from 0 to 2*pi
    HANGLES = np.linspace(0, 2 * np.pi)
    # Used for the equivalent of horizontal lines in cartesian coordinates plots
    # The last one is also used to add a fill which acts a background color.
    H0 = np.zeros(len(HANGLES))
    H1 = np.ones(len(HANGLES)) * 0.5
    H2 = np.ones(len(HANGLES))
    # Initialize layout ----------------------------------------------
    fig = plt.figure(figsize=(20, 20))
    ax = fig.add_subplot(111, polar=True)
    fig.patch.set_facecolor(BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    # Rotate the "" 0 degrees on top.
    # There it where the first variable, avg_bill_length, will go.
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    # Setting lower limit to negative value reduces overlap
    # for values that are 0 (the minimums)
    ax.set_ylim(-0.1, 1.05)


def plot_radar_data():
    global var_array
    # Plot lines and dots --------------------------------------------
    for idx, variable in enumerate(var_array):
        values = dfP.iloc[idx].values.tolist()[1:]
        values += values[:1]
        ax.plot(ANGLES, values, c=COLORS[idx], linewidth=4, label=variable)
        ax.scatter(ANGLES, values, s=160, c=COLORS[idx], zorder=10)


var_array = dfP.columns.tolist()[1:]
var_number = len(var_array)
print("var_amount", var_number)
setup_radar()
plot_radar_data()
fig
