import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

import textbausteine
import variables as var
import dics as dics

# --- Functions
def assign_dimensions(df):
    conditions = [
        (df.index >= var.f_q_technologie) & (df.index <= var.l_q_technologie),
        (df.index >= var.f_q_data) & (df.index <= var.l_q_data),
        (df.index >= var.f_q_organisation) & (df.index <= var.l_q_organisation),
        (df.index >= var.f_q_prozesse) & (df.index <= var.l_q_prozesse)
    ]
    values = ['Technologie',
              'Daten',
              'Organisation und Expertise',
              'Prozesse im Bezug auf KI'
              ]
    df['Gestaltungsdimension'] = np.select(conditions, values)
    return df
def calculate_sum_points(df):
    for i in range(var.number_Participants):
      df[[i]] = df[[i]].astype(str).astype(int)
    df['Punkte'] = df.sum(axis=1)
    return df
def calculate_average_points(df):
    for i in range(var.number_Participants):
        df = df.drop([i], axis=1)
    df['Punkte'] = df['Punkte'].div(var.number_Participants).round(1)
    df = df.rename({'Punkte': 'Durchschnitt Punkte'}, axis=1)
    return df
def transform_to_question_dimension_average_points_df(df):
    # st.write("----- Print 1 -----")
    # st.write(df) # --- PRINT1
    df = df.drop(columns=['ID', 'Startzeit', 'Fertigstellungszeit', 'E-Mail', 'Name'])
    df = df.replace(
        to_replace={'trifft nicht zu': '0', 'trifft eher nicht zu': '1', 'teils teils': '2', 'trifft eher zu': '3',
                    'trifft zu': '4', 'Ich kann keine Aussage treffen.': '0'})
    df = df.transpose()
    # st.write("----- Print 2 -----")
    # st.write(df)
    df = df.reset_index()
    df = df.rename({'index': 'Frage'}, axis=1)
    # st.write("----- Print 3 -----")
    # st.write(df)
    df = assign_dimensions(df)
    # st.write("----- Print 4 -----")
    # st.write(df)
    df.drop([0, 1], axis=0, inplace=True)
    # st.write("----- Print 5 -----")
    # st.write(df)
    df = calculate_sum_points(df)
    # st.write("----- Print 6 -----")
    # st.write(df)
    df = calculate_average_points(df)
    return df
def assign_levels(df):
    conditions = [
        ((df["Punkte Pro Dimension"] > 0) & (df["Punkte Pro Dimension"] <= var.upper_bound_tech_level1) & (df['Gestaltungsdimension'] == 'Technologie')),
        ((df["Punkte Pro Dimension"] > var.upper_bound_tech_level1) & (df["Punkte Pro Dimension"] <= var.upper_bound_tech_level2)) & (df['Gestaltungsdimension'] == 'Technologie'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_tech_level2) & (df["Punkte Pro Dimension"] <= var.upper_bound_tech_level3)) & (df['Gestaltungsdimension'] == 'Technologie'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_tech_level3) & (df["Punkte Pro Dimension"] <= var.upper_bound_tech_level4)) & (df['Gestaltungsdimension'] == 'Technologie'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_tech_level4) & (df["Punkte Pro Dimension"] <= var.upper_bound_tech_level5)) & (df['Gestaltungsdimension'] == 'Technologie'),

        ((df["Punkte Pro Dimension"] > 0) & (df["Punkte Pro Dimension"] <= var.upper_bound_data_level1) & (df['Gestaltungsdimension'] == 'Daten')),
        ((df["Punkte Pro Dimension"] > var.upper_bound_data_level1) & (df["Punkte Pro Dimension"] <= var.upper_bound_data_level2)) & (df['Gestaltungsdimension'] == 'Daten'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_data_level2) & (df["Punkte Pro Dimension"] <= var.upper_bound_data_level3)) & (df['Gestaltungsdimension'] == 'Daten'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_data_level3) & (df["Punkte Pro Dimension"] <= var.upper_bound_data_level4)) & (df['Gestaltungsdimension'] == 'Daten'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_data_level4) & (df["Punkte Pro Dimension"] <= var.upper_bound_data_level5)) & (df['Gestaltungsdimension'] == 'Daten'),

        ((df["Punkte Pro Dimension"] > 0) & (df["Punkte Pro Dimension"] <= var.upper_bound_orga_level1) & (df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI')),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level1) & (df["Punkte Pro Dimension"] <= var.upper_bound_orga_level2)) & (df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level2) & (df["Punkte Pro Dimension"] <= var.upper_bound_orga_level3)) & (df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level3) & (df["Punkte Pro Dimension"] <= var.upper_bound_orga_level4)) & (df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level4) & (df["Punkte Pro Dimension"] <= var.upper_bound_orga_level5)) & (df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI'),

        ((df["Punkte Pro Dimension"] > 0) & (df["Punkte Pro Dimension"] <= var.upper_bound_orga_level1) & (df['Gestaltungsdimension'] == 'Organisation und Expertise')),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level1) & (df["Punkte Pro Dimension"] <= var.upper_bound_orga_level2)) & (df['Gestaltungsdimension'] == 'Organisation und Expertise'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level2) & (df["Punkte Pro Dimension"] <= var.upper_bound_orga_level3)) & (df['Gestaltungsdimension'] == 'Organisation und Expertise'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level3) & (df["Punkte Pro Dimension"] <= var.upper_bound_orga_level4)) & (df['Gestaltungsdimension'] == 'Organisation und Expertise'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level4) & (df["Punkte Pro Dimension"] <= var.upper_bound_orga_level5)) & (df['Gestaltungsdimension'] == 'Organisation und Expertise')
    ]

    values = [1,2,3,4,5,
              1,2,3,4,5,
              1,2,3,4,5,
              1, 2, 3, 4, 5]

    df['Stufe'] = np.select(conditions, values)
    return df
def transform_to_dimension_level_df(df):
    df = df.groupby(['Gestaltungsdimension'])['Durchschnitt Punkte'].sum()
    df = df.reset_index().rename({'Durchschnitt Punkte': 'Punkte Pro Dimension'}, axis=1)
    df = assign_levels(df)
    df = df.drop(['Punkte Pro Dimension'], axis=1)
    return df
def spidermap(df):
    col_punkte = df['Stufe'].tolist()
    df = pd.DataFrame(dict(
        r=col_punkte,
        theta=['Daten', 'Organisation und Expertise', 'Prozesse in Bezug auf Ki', 'Technologie']))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    return fig
def transform_to_dimension_drilldown(main_df, questions_points_dic, cat_points_dic):
    df_kat = main_df[main_df['Gestaltungsdimension'] == 'Technologie']
    df_kat = df_kat.filter(['Frage', 'Durchschnitt Punkte'], axis=1)
    col_punkte_kat = df_kat['Durchschnitt Punkte'].tolist()
    questions_points_dic
    cat_points_dic

    for i, p in enumerate(col_punkte_kat):
        k = questions_points_dic[i]
        cat_points_dic[k] += p

    points_by_subkat = list(cat_points_dic.keys())
    subkats = list(cat_points_dic.values())

    points_by_subkat_df = pd.DataFrame()
    points_by_subkat_df['Kategorien'] = points_by_subkat
    points_by_subkat_df['Punkte'] = subkats

    bar_chart_dimension_level_df = px.bar(points_by_subkat_df, x='Kategorien', y='Punkte')

    st.write(bar_chart_dimension_level_df)
    return points_by_subkat_df

# --- Dataframes and Spidermap for Dimension Level
df = pd.read_excel('survey.xlsx')
df = transform_to_question_dimension_average_points_df(df)
dimension_level_df = transform_to_dimension_level_df(df)
st.write('----- dimension_level_df -----')
bar_chart_dimension_level_df = px.bar(dimension_level_df, x ='Gestaltungsdimension', y = 'Stufe')
spider_dimension_level = spidermap(dimension_level_df)

# ----------------
st.write(bar_chart_dimension_level_df)
spider_dimension_level
transform_to_dimension_drilldown(df, dics.questions_points_tech, dics.cat_points_tech)


# --- Layout ---

st.title(":bar_chart: Ergebnisse KI Reifegradermittlung")
st.markdown(textbausteine.intro)
# st.write("ALTERNATIVE 1")
# bar_chart_1 = px.bar(dimension_level_df)
# st.write(bar_chart_1)
# st.write("ALTERNATIVE 2")
# st.bar_chart(dimension_level_df)
# st.write("ALTERNATIV 3")

st.header("KI-Reife über die 4 Dimensionen")
st.markdown(textbausteine.four_dimensions_intro)


st.header("KI-Reife innerhalb der Dimensionen ")
st.markdown(textbausteine.each_dimension_intro)
# st.subheader("Technologie")
# st.write(px.bar(df_tech, orientation='h'))
# st.subheader("Daten")
# st.write(px.bar(df_daten, orientation='h'))
# st.subheader("Organisation")
# st.write(px.bar(df_orga, orientation='h'))
st.subheader("Technologie")
st.markdown(textbausteine.tech_intro)
# st.write(px.bar(df_prozesse, orientation='h'))
# st.write(df_prozesse)
# st.write("----------------------------------------")
# st.write(df_lola_tech)
df_lola_tech = df_lola_tech.set_index('Kat')
st.write(px.bar(df_lola_tech))
st.markdown(textbausteine.tech_level1)

st.subheader("Daten")
st.markdown(textbausteine.description_daten)
df_data_drilldown = df_data_drilldown.set_index('Kat')
st.write(px.bar(df_data_drilldown))
st.markdown(textbausteine.description_daten_level1)

st.subheader("Prozesse im Bezug auf KI")
# st.write(px.bar(df_prozesse, orientation='h'))
# st.write(df_prozesse)
# st.write("----------------------------------------")
df_lola = df_lola.set_index('Kategorie')
# st.write(df_lola)
st.write(px.bar(df_lola))

st.subheader("Organisation und Expertise")
st.write(px.bar(df_orga_drilldown))



st.header("Handlungsempfehlungen:")
st.markdown(textbausteine.handlungsempf)


