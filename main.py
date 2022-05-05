import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

st.set_page_config(page_title="Ergebnisse KI Reifegradermittlung",
                   page_icon=":bar_chart:",
                   layout="wide")
# --- Import Dataframe ---
df = pd.read_excel('surveyResults.xlsx')

# --- Text variables ---
body1 = """Lieber Kunde, der erste Teil der Reifegradanalyse ist jetzt geschafft. Nach der Erhebung der Datenbasis wollen wir jetzt gemeinsam in die Analyse gehen. 
In der Gesamtbewertung haben sie 14/20 möglichen Punkten errreicht und werden so Als KI Experte eingestuft.
Ein KI Experte zeichnet sich dadurch aus, dass / ------------------------- Beschreibung KI Experte. ---------."""
body2 = """ Um auf Ihr Unternehmen auf die nächste Stufe in Richtung KI Experte zu heben, können Sie folgende
Maßnahmen ergreifen:"""

# --- Variables ---
technologie = ["Modelle und Werkzeuge: Befinden sich schon Datenanalysemodelle und / oder -Werkzeuge im Einsatz? ", "Datenhaltung und Hosting",
               "Data Warehouse Plattform", "Datenherkunft",
               "BI-Infrastruktur", "HolaLola"]
data = []

# --- Hilfsfunktionen
def assign_Dimension():
    conditions = [
        (df['index'] < 23),
        (df['index'] > 23) & (df['index'] < 48),
        (df['index'] > 48) & (df['index'] < 59),
        (df['index'] > 59) & (df['index'] <= 63)
    ]
    values = ['Technologie',
              'Daten',
              'Organisation und Expertise',
              'Prozesse im Bezug auf KI'
              ]
    df['Gestaltungsdimension'] = np.select(conditions, values)

# ---- Transform Dataframe ---
df = df.drop(columns=['ID','Startzeit', 'Fertigstellungszeit', 'E-Mail'])
df = df.replace(to_replace={'stimme überhaupt nicht zu':'0', 'stimme nicht zu':'1', 'stimme zu':'2', 'stimme voll und ganz zu':'4'})
df = df.transpose()
df = df.reset_index(level=0)
df = df.reset_index(level=0)

df = df.rename({'index':'Frage', 'level_0':'index'}, axis=1)
# df['Gestaltungsdimension'] = ''
str = "HolaLola"
# df.loc[df['Frage'] == str, 'Gestaltungsdimension'] = 'LOla'
# df.loc[df['Frage'], 'Gestaltungsdimension'] = assign_Dimension(df['Frage'])
assign_Dimension()
st.write(df)

def import_df1():
    df = pd.read_excel(
        io='surveyResults.xlsx',
        engine='openpyxl',
        sheet_name='Sheet2',
        skiprows=0,
        # usecols='E:BP',
        # nrows=2,

    )
    return df
def import_dfP():
    dfP = pd.read_excel(
        io='surveyResults.xlsx',
        engine='openpyxl',
        sheet_name='Sheet3',
        # skiprows= 1,
        # usecols='E:BP',
        # nrows=2,
    )
    return dfP


df = import_df1()
dfP = import_dfP()

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
# --- Debugging Dataframes ----
# st.write(df)
# st.dataframe(dfSelection)
# st.write(dfP)

# Points by Dimension [Bar Chart]
def plot_barchart():
    pointsByDimensions = (
        dfSelection.groupby(by=["Gestaltungsdimension"]).sum()[["Punkte"]]
    )
    figPointsDimension = px.bar(
        pointsByDimensions,
        x="Punkte",
        y=pointsByDimensions.index,
       # orientation="h",
        title="<b>Punkte nach Gestaltungsdimension </b>",
        color_discrete_sequence=["#0083B8"] * len(pointsByDimensions),
        template="plotly_white",
    )
    st.plotly_chart(figPointsDimension)
    DataFrame = df
    chart_data = pd.DataFrame()
    st.bar_chart(chart_data)


# --- Mainpage ---
st.title(":bar_chart: Ergebnisse KI Reifegradermittlung")
st.text(body1)
st.header("Ergebnisse nach Gestaltungsdimensionen")
plot_barchart()
st.header("Handlungsempfehlungen:")
st.text(body2)

# --- Maturity Analysis ---
total_points = dfSelection['Punkte'].sum()
def setup_radar():
    """
    Starts the radar charts
    :param var_number:
    """
    global COLORS, companies_array, ANGLES, fig, ax, var_number
    global BG_WHITE
    BG_WHITE = "#fbf9f4"
    global BLUE
    BLUE = "#2a475e"
    global GREY70
    GREY70 = "#b3b3b3"
    global GREY_LIGHT
    GREY_LIGHT = "#f2efe8"
    global COLORS
    COLORS = ["#FF5A5F", "#FFB400", "#007A87"]
    # The three species of penguins
    global companies_array
    companies_array = dfP["Unternehmen"].values.tolist()
    print("Unternehmen:", companies_array)

    # The angles at which the values of the numeric variables are placed
    ANGLES = [n / var_number * 2 * np.pi for n in range(var_number)]
    ANGLES += ANGLES[:1]
    # Padding used to customize the location of the tick labels
    X_VERTICAL_TICK_PADDING = 5
    X_HORIZONTAL_TICK_PADDING = 50
    # Angle values going from 0 to 2*pi
    global HANGLES
    HANGLES = np.linspace(0, 2 * np.pi)
    # Used for the equivalent of horizontal lines in cartesian coordinates plots
    # The last one is also used to add a fill which acts a background color.
    global H0
    H0 = np.zeros(len(HANGLES))
    global H1
    H1 = np.ones(len(HANGLES)) * 0.5
    global H2
    H2 = np.ones(len(HANGLES))

    # Initialize layout ----------------------------------------------
    fig = plt.figure(figsize=(4, 5))
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
    for idx, company_i in enumerate(companies_array):
        print(var_array)
        values = dfP.iloc[idx].values.tolist()[1:]
        print("val: ", values)
        values += values[:1]
        ax.plot(ANGLES, values, c=COLORS[idx % 3], linewidth=4, label=company_i)
        ax.scatter(ANGLES, values, s=160, c=COLORS[idx % 3], zorder=10)


var_array = dfP.columns.tolist()[1:]
var_number = len(var_array)
print("var_amount", var_number)
setup_radar()
plot_radar_data()
# fig

# Set values for the angular axis (x)
ax.set_xticks(ANGLES[:-1])
ax.set_xticklabels(var_array, size=14)

# Remove lines for radial axis (y)
ax.set_yticks([])
ax.yaxis.grid(False)
ax.xaxis.grid(False)

# Remove spines
ax.spines["start"].set_color("none")
ax.spines["polar"].set_color("none")

# # Add custom lines for radial axis (y) at 0, 0.5 and 1.
ax.plot(HANGLES, H0, ls=(0, (6, 6)), c=GREY70)
ax.plot(HANGLES, H1, ls=(0, (6, 6)), c=COLORS[2])
ax.plot(HANGLES, H2, ls=(0, (6, 6)), c=GREY70)

# # Now fill the area of the circle with radius 1.
# # This create the effect of gray background.
ax.fill(HANGLES, H2, GREY_LIGHT)

# # Custom guides for angular axis (x).
# # These four lines do not cross the y = 0 value, so they go from
# # the innermost circle, to the outermost circle with radius 1.
ax.plot([0, 0], [0, 1], lw=2, c=GREY70)
ax.plot([np.pi, np.pi], [0, 1], lw=2, c=GREY70)
ax.plot([np.pi / 2, np.pi / 2], [0, 1], lw=2, c=GREY70)
ax.plot([-np.pi / 2, -np.pi / 2], [0, 1], lw=2, c=GREY70)

# # Add levels -----------------------------------------------------
# # These labels indicate the values of the radial axis
PAD = 0.05
ax.text(-0.4, 0 + PAD, "Beginner", size=10, fontname="Roboto")
ax.text(-0.4, 0.5 + PAD, "Fortgeschritten", size=10, fontname="Roboto")
ax.text(-0.4, 1 + PAD, "Experte", size=10, fontname="Roboto")

# Create and add legends -----------------------------------------
# Legends are made from scratch.

# Iterate through species names and colors.
# These handles contain both markers and lines.
handles = [
    Line2D(
        [], [],
        c=color,
        lw=3,
        marker="o",
        markersize=8,
        label=variable
    )
    for variable, color in zip(companies_array, COLORS)
]

legend = ax.legend(
    handles=handles,
    loc=(1, 0),  # bottom-right
    labelspacing=1.5,  # add space between labels
    frameon=False  # don't put a frame
)

# Iterate through text elements and change their properties
for text in legend.get_texts():
    text.set_fontname("Roboto")  # Change default font
    text.set_fontsize(10)  # Change default font size

# Adjust tick label positions ------------------------------------
# XTICKS = ax.xaxis.get_major_ticks()
# for tick in XTICKS[0::2]:
#     tick.set_pad(X_VERTICAL_TICK_PADDING)
#
# for tick in XTICKS[1::2]:
#     tick.set_pad(X_HORIZONTAL_TICK_PADDING)

# Add title ------------------------------------------------------
fig.suptitle(
    "Reifegrad in den verschiedenen Gestaltungsdimensionen",
    x=0.1,
    y=1,
    ha="left",
    fontsize=15,
    fontname="Lobster Two",
    color=BLUE,
    weight="bold",
)
fig
