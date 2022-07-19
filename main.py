import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

class SpiderRadar:
    def create_and_plot_radar(self):
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
            fig = plt.figure(figsize=(5, 6))
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

        dfP = pd.read_excel(
            io='surveyResults.xlsx',
            engine='openpyxl',
            sheet_name='Sheet3'
        )

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
        return fig

st.set_page_config(page_title="Ergebnisse KI Reifegradermittlung",
                   page_icon=":bar_chart:",
                   layout="wide")

# --- Variables ---
body1 = """Hallo Kunde, der erste Teil der Reifegradanalyse ist jetzt geschafft. Nach der Erhebung der Datenbasis wollen wir jetzt gemeinsam in die Analyse gehen. 
In der Gesamtbewertung haben sie 14/20 möglichen Punkten errreicht und werden so Als KI Experte eingestuft.
Ein KI Experte zeichnet sich dadurch aus, dass / ------------------------- Beschreibung KI Experte. ---------."""
body2 = """ Um auf Ihr Unternehmen auf die nächste Stufe in Richtung KI Experte zu heben, können Sie folgende
Maßnahmen ergreifen:"""
body3 = """Hallo. Ich bin ein kleiner Blindtext. Und zwar schon so lange ich denken kann.
 Es war nicht leicht zu verstehen, was es bedeutet, ein blinder Text zu sein: Man ergibt keinen Sinn. Wirklich keinen Sinn.
 Man wird zusammenhangslos eingeschoben und rumgedreht – und oftmals gar nicht erst gelesen. Aber bin ich allein deshalb ein schlechterer Text als andere?
 Na gut, ich werde nie in den Bestsellerlisten stehen. Aber andere Texte schaffen das auch nicht. Und darum stört es mich nicht besonders blind zu sein.
 Und sollten Sie diese Zeilen noch immer lesen, so habe ich als kleiner Blindtext etwas geschafft, wovon all die richtigen und wichtigen Texte meist nur
 träumen."""

f_q_technologie = 2
l_q_technologie = 16
f_q_data = 17
l_q_data = 33
f_q_organisation = 34
l_q_organisation = 41
f_q_prozesse = 42
l_q_prozesse = 46

upper_bound_tech_level1 = 12
upper_bound_tech_level2 = 24
upper_bound_tech_level3 = 36
upper_bound_tech_level4 = 48
upper_bound_tech_level5 = 60

upper_bound_data_level1 = 13
upper_bound_data_level2 = 26
upper_bound_data_level3 = 38
upper_bound_data_level4 = 51
upper_bound_data_level5 = 64

upper_bound_orga_level1 = 6
upper_bound_orga_level2 = 13
upper_bound_orga_level3 = 19
upper_bound_orga_level4 = 26
upper_bound_orga_level5 = 32

upper_bound_procecess_level1 = 5
upper_bound_orga_level2 = 10
upper_bound_orga_level3 = 14
upper_bound_orga_level4 = 19
upper_bound_orga_level5 = 24

# --- Functions
def assign_dimensions(df):
    conditions = [
        (df['index'] >= f_q_technologie) & (df['index'] <= l_q_technologie),
        (df['index'] >= f_q_data) & (df['index'] <= l_q_data),
        (df['index'] >= f_q_organisation) & (df['index'] <= l_q_organisation),
        (df['index'] >= f_q_prozesse) & (df['index'] <= l_q_prozesse)
    ]
    values = ['Technologie',
              'Daten',
              'Organisation und Expertise',
              'Prozesse im Bezug auf KI'
              ]
    df['Gestaltungsdimension'] = np.select(conditions, values)
    return df
def assign_levels(df3):
    conditions = [
        (df3['Punkte'] > 0) & (df3['Punkte'] <= upper_bound_tech_level1),
        (df3['Punkte'] > upper_bound_tech_level1) & (df3['Punkte'] <= upper_bound_tech_level2),
        (df3['Punkte'] > upper_bound_tech_level2) & (df3['Punkte'] <= upper_bound_tech_level3),
        (df3['Punkte'] > upper_bound_tech_level3) & (df3['Punkte'] <= upper_bound_tech_level4),
        (df3['Punkte'] > upper_bound_tech_level4) & (df3['Punkte'] <= upper_bound_tech_level5),
    ]
    values = ['Level 1',
              'Level 2',
              'Level 3',
              'Level 4',
              'Level 5',
              ]
    df3['Stufe'] = np.select(conditions, values)
    return df3
def calculate_Punkte(df):
    cols_to_sum = [0,1,2,3,4]
    df['Punkte'] = df[cols_to_sum].astype(float).sum(axis=1, skipna=True)
    df['Punkte'] = df['Punkte'].div(5).round(1)
    return df
def transform_df(df):
    st.write(df)
    df = df.drop(columns=['ID', 'Startzeit', 'Fertigstellungszeit', 'E-Mail', 'Name'])
    df = df.replace(
        to_replace={'trifft nicht zu': '0', 'trifft eher nicht zu': '1', 'teils teils': '2', 'trifft eher zu': '3',
                    'trifft zu': '4', 'Ich kann keine Aussage treffen.': '0'})
    df = df.transpose()
    df = df.reset_index(level=0)
    df = df.reset_index(level=0)
    df = df.rename({'index': 'Frage', 'level_0': 'index'}, axis=1)
    df = assign_dimensions(df)
    df.drop([0, 1], axis=0, inplace=True)
    st.write(df)
    df = calculate_Punkte(df)
    st.write(df)
    df2 = df.groupby(['Gestaltungsdimension'])['Punkte'].sum()
    st.bar_chart(df2)
    st.write(df2)
    d = {'Gestaltungsdimension': ['Daten', 'Organisation und Expertise', 'Prozesse im Bezug auf KI', 'Technologie'],
         'Punkte': [52, 28, 16, 45]}
    df3 = pd.DataFrame(data=d)
    st.write(df3)
    df3 = assign_levels(df3)
    st.write(df3)
    return df3
def drill_down():
    # First, let's set up the multi index with 2 levels:
    # city and store. We will create an empty frame with some
    # column data (fruits) and pass in the multi index as index.
    # Index names are set for accessing later

    multi_index = pd.MultiIndex.from_product([
        ['city_1', 'city_2'],
        ['store_1', 'store_2', 'store_3'],
    ])
    df = pd.DataFrame(columns=['apples', 'oranges'], index=multi_index)
    df.index.set_names(['city', 'store'], inplace=True)

    # Now let's make some selectboxes for drilling up/down

    levels = [
        st.selectbox('Level 1', ['All'] + [i for i in df.index.get_level_values(0).unique()]),
        st.selectbox('Level 2', ['All'] + [i for i in df.index.get_level_values(1).unique()])
    ]

    # We need to use slice(None) if the user selects 'All'.
    # The specified level with 'All' will take all values in that level.

    for idx, level in enumerate(levels):
        if level == 'All':
            levels[idx] = slice(None)

    # Make a cross section with the level values and pass in the index names.

    st.dataframe(
        df.xs(
            (levels[0], levels[1]),
            level=['city', 'store']
        )
    )
# --- Transform Dataframe

#df3 = transform_df(df)
#st.write(df3)
df = pd.read_excel('survey.xlsx')
transform_df(df)
drill_down()

# --- Mainpage ---
st.title(":bar_chart: Ergebnisse KI Reifegradermittlung")
st.text(body1)
st.header("Ihr Seid Ki Experten!")
st.text(body3)
st.header("Ergebnisse nach Gestaltungsdimensionen")
st.header("Handlungsempfehlungen:")
st.text(body3)


