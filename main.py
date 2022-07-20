import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

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
    cols_to_sum = [0, 1, 2, 3, 4]
    df['Punkte'] = df[cols_to_sum].astype(float).sum(axis=1, skipna=True)
    df['Punkte'] = df['Punkte'].div(5).round(1)
    return df

def transform_df(df):
    # st.write(df) # --- PRINT1
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
    # st.write(df) # --- PRINT2
    df = calculate_Punkte(df)
    # st.write(df) # --- PRINT3
    # df.drop([2,3], axis=1) #todo:WHY IS THIS NOT DROPPING?
    df = df.filter(['Frage', 'Gestaltungsdimension', 'Punkte'], axis=1)
    # st.write(df) # --- PRINT4
    # df2 = assign_levels(df2) #todo: fix 1st column
    return df

# --- Dataframes and Plots
df = pd.read_excel('survey.xlsx')
df = transform_df(df)

# Punkte nach Gestaltungsdimensionen
df_dimensions_points = df.groupby(['Gestaltungsdimension'])['Punkte'].sum()
#st.write(df_dimensions_points)

# Df for Spider
df_for_spider = df_dimensions_points.reset_index()
#st.write(df_for_spider)
col_punkte = df_for_spider['Punkte'].tolist()
#st.write(col_punkte)

# Punkte nach Unterkategorien
df_tech = df[df['Gestaltungsdimension'] == 'Technologie']
df_daten = df[df['Gestaltungsdimension'] == 'Daten']
df_orga = df[df['Gestaltungsdimension'] == 'Organisation und Expertise']
df_prozesse = df[df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI']

df_tech = df_tech.filter(['Frage', 'Punkte'], axis=1)
df_daten = df_daten.filter(['Frage', 'Punkte'], axis=1)
df_orga = df_orga.filter(['Frage', 'Punkte'], axis=1)
df_prozesse = df_prozesse.filter(['Frage', 'Punkte'], axis=1)

df_tech = df_tech.groupby(['Frage'])['Punkte'].sum()
df_daten = df_daten.groupby(['Frage'])['Punkte'].sum()
df_orga = df_orga.groupby(['Frage'])['Punkte'].sum()
df_prozesse = df_prozesse.groupby(['Frage'])['Punkte'].sum()
# st.write(df_orga)

#SpiderMap

df = pd.DataFrame(dict(
    r=col_punkte,
    theta=['Daten','Organisation und Expertise','Prozesse in Bezug auf KI',
           'Technologie']))
fig = px.line_polar(df, r='r', theta='theta', line_close=True)

# --- Mainpage ---
st.title(":bar_chart: Ergebnisse KI Reifegradermittlung")
st.text(body1)
st.write("ALTERNATIVE 1")
bar_chart_1 = px.bar(df_dimensions_points, orientation='h')
st.write(bar_chart_1)
st.write("ALTERNATIVE 2")
st.bar_chart(df_dimensions_points)
st.write("ALTERNATIV 3")
fig

st.header("Ihr Seid Ki Experten!")
st.text(body3)

st.header("Ergebnisse nach Gestaltungsdimensionen")
st.subheader("Technologie")
st.write(px.bar(df_tech, orientation='h'))
st.subheader("Daten")
st.write(px.bar(df_daten, orientation='h'))
st.subheader("Organisation")
st.write(px.bar(df_orga, orientation='h'))
st.subheader("Prozesse im Bezug auf KI")
st.write(px.bar(df_prozesse, orientation='h'))

st.header("Handlungsempfehlungen:")
st.text(body3)

