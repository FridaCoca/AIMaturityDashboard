import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import variables as var

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

def assign_levels():
    data = {"Dimension": ['Daten', 'Organisation und Expertise', 'Prozesse', 'Technologie'], "Punkte": [260, 140, 80, 225]}
    df3 = pd.DataFrame(data)
    #st.write("--------- Print in assign Levels ------")
    #st.write(df3)
    # for col in df3.columns:
    #     print(col)
    conditions = [
        (df3["Punkte"] > 0) & (df3["Punkte"] <= var.upper_bound_tech_level1),
        (df3["Punkte"] > var.upper_bound_tech_level1) & (df3["Punkte"] <= var.upper_bound_tech_level2),
        (df3["Punkte"] > var.upper_bound_tech_level2) & (df3["Punkte"] <= var.upper_bound_tech_level3),
        (df3["Punkte"] > var.upper_bound_tech_level3) & (df3["Punkte"] <= var.upper_bound_tech_level4),
        (df3["Punkte"] > var.upper_bound_tech_level4) & (df3["Punkte"] <= var.upper_bound_tech_level5),
    ]
    values = ['1',
              '2',
              '3',
              '4',
              '5',
              ]
    df3['Stufe'] = np.select(conditions, values)
    df3 = df3.drop(columns=['Punkte'])

    #st.write("--------- Print in assign Levels 2 ------")
    #st.write(df3)
    return df3

def calculate_Punkte(df): #todo: fix SUM!
    cols_to_sum = [0, 1, 2, 3, 4]
    #st.write("----- Print in calculate Punkte -----")
    df['Punkte'] = df[cols_to_sum].astype(int).sum(axis=1, skipna=False)
    # df['Punkte'] = df['Punkte'].div(5).round(1)
    #st.write(df)
    return df

def transform_to_question_dimension_points_df(df):
    st.write("----- Print 1 -----")
    st.write(df) # --- PRINT1
    df = df.drop(columns=['ID', 'Startzeit', 'Fertigstellungszeit', 'E-Mail', 'Name'])
    df = df.replace(
        to_replace={'trifft nicht zu': '0', 'trifft eher nicht zu': '1', 'teils teils': '2', 'trifft eher zu': '3',
                    'trifft zu': '4', 'Ich kann keine Aussage treffen.': '0'})
    df = df.transpose()
    st.write("----- Print 2 -----")
    st.write(df)
    df = df.reset_index()
    df = df.rename({'index': 'Frage'}, axis=1)
    st.write("----- Print 3 -----")
    st.write(df)
    df = assign_dimensions(df)
    st.write("----- Print 4 -----")
    st.write(df)
    df.drop([0, 1], axis=0, inplace=True)
    #st.write("----- Print 5 -----")
    #st.write(df)
    df = calculate_Punkte(df)
    #st.write("----- Print 6 -----")
    #st.write(df)
    return df

def transform_to_dimension_level_df(df):
    df = df.groupby(['Gestaltungsdimension'])['Punkte'].sum()
    # st.write("----- Punkte nach Dimension -----")
    # st.write(groupBy_dimension_df)
    df = assign_levels()
    # df_dimensions_points = df_dimensions_points.set_index('Dimension')
    #st.write(df)
    return df

def transfor_to_dimension_drilldown_data(col_punkte_data):
    data_questions_points_dic = {
        0: 'Daten Hosting',
        1: 'Daten Hosting',
        2: 'Daten Hosting',
        3: 'Modelle und Werkzeuge',
        4: 'Modelle und Werkzeuge',
        5: 'Modelle und Werkzeuge',
        6: 'Modelle und Werkzeuge',
        7: 'Modelle und Werkzeuge',
        8: 'Data Warehouse Plattform',
        9: 'Data Warehouse Plattform',
        10: 'Data Warehouse Plattform',
        11: 'Data Warehouse Plattform',
        12: 'BI Infrastruktur',
        13: 'BI Infrastruktur',
        14: 'BI Infrastruktur',
    }
    data_cat_points_dic = {
        'Daten Hosting': 0,
        'Modelle und Werkzeuge': 0,
        'Data Warehouse Plattform': 0,
        'BI Infrastruktur': 0,
    }
    print(col_punkte_data)
    for i, p in enumerate(col_punkte_data):
        k = data_questions_points_dic[i]
        data_cat_points_dic[k] += p

    # todo Durchschnitt
    col_points_drilldown_data = data_cat_points_dic.values()
    punke_pro_kategorie_tech = list(data_cat_points_dic.keys())
    kategorien_tech = list(data_cat_points_dic.values())
    # print(kategorien)
    # df_lola = pd.DataFrame(prozesse_katerogie_punkte_dic) // WHY DOES IT NOT WORK
    # print(df_lola)

    # create empty data frame in pandas
    df_lola_tech = pd.DataFrame()
    df_lola_tech['Kat'] = punke_pro_kategorie_tech
    df_lola_tech['Punkte'] = kategorien_tech
    # st.write(df_lola_tech)
    return df_lola_tech

def transfor_to_dimension_drilldown_orga(col_punkte_orga):
    data_questions_points_dic = {
        0: 'BI Expertise',
        1: 'BI Expertise',
        2: 'BI Expertise',
        3: 'Bestehende KI Lösungen im Unternehmen',
        4: 'Bestehende KI Lösungen im Unternehmen',
        5: 'Bestehende KI Lösungen im Unternehmen',
        6: 'Strategie',
        7: 'Strategie',
        8: 'Strategie',
    }
    data_cat_points_dic = {
        'BI Expertise': 0,
        'Bestehende KI Lösungen im Unternehmen': 0,
        'Strategie': 0,
    }
    print(col_punkte_orga)
    for i, p in enumerate(col_punkte_orga):
        k = data_questions_points_dic[i]
        data_cat_points_dic[k] += p

    # todo Durchschnitt
    col_points_drilldown_data = data_cat_points_dic.values()
    punke_pro_kategorie_tech = list(data_cat_points_dic.keys())
    kategorien_tech = list(data_cat_points_dic.values())
    # print(kategorien)
    # df_lola = pd.DataFrame(prozesse_katerogie_punkte_dic) // WHY DOES IT NOT WORK
    # print(df_lola)

    # create empty data frame in pandas
    df_lola_tech = pd.DataFrame()
    df_lola_tech['Kat'] = punke_pro_kategorie_tech
    df_lola_tech['Punkte'] = kategorien_tech
    # st.write(df_lola_tech)
    df_lola_tech = df_lola_tech.set_index('Kat')
    return df_lola_tech

# --- Dataframes
df = pd.read_excel('survey.xlsx')
question_dimension_df = transform_to_question_dimension_points_df(df)
# st.write(question_dimension_df)

# Punkte nach Gestaltungsdimensionen
dimension_level_df = transform_to_dimension_level_df(question_dimension_df)

# Df for Spider
df_for_spider = dimension_level_df.reset_index()
# st.write(df_for_spider)
#col_punkte = df_for_spider['Stufe'].tolist()
col_punkte = [1,2,3,4]
# st.write(col_punkte)

# Punkte nach Unterkategorien
df_tech = question_dimension_df[question_dimension_df['Gestaltungsdimension'] == 'Technologie']
df_daten = question_dimension_df[question_dimension_df['Gestaltungsdimension'] == 'Daten']
df_orga = question_dimension_df[question_dimension_df['Gestaltungsdimension'] == 'Organisation und Expertise']
df_prozesse = question_dimension_df[question_dimension_df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI']

df_tech = df_tech.filter(['Frage', 'Punkte'], axis=1)
df_daten = df_daten.filter(['Frage', 'Punkte'], axis=1)
df_orga = df_orga.filter(['Frage', 'Punkte'], axis=1)
df_prozesse = df_prozesse.filter(['Frage', 'Punkte'], axis=1)

df_tech = df_tech.groupby(['Frage'])['Punkte'].sum()
df_daten = df_daten.groupby(['Frage'])['Punkte'].sum()
df_orga = df_orga.groupby(['Frage'])['Punkte'].sum()
df_prozesse = df_prozesse.groupby(['Frage'])['Punkte'].sum()
# st.write(df_orga)

# Punkte auf mittlerer Hierarchieebene
df_tech_for_mittlerer_Hierarchieebene = df_tech.reset_index()
df_daten_for_mittlerer_Hierarchieebene = df_daten.reset_index()
df_orga_for_mittlerer_Hierarchieebene = df_orga.reset_index()
df_prozesse_for_mittlerer_Hierarchieebene = df_prozesse.reset_index()
# st.write(df_prozesse_for_mittlerer_Hierarchieebene)
col_punkte_data = df_tech_for_mittlerer_Hierarchieebene['Punkte'].tolist()
col_punkte_daten = df_daten_for_mittlerer_Hierarchieebene['Punkte'].tolist()
col_punkte_orga = df_orga_for_mittlerer_Hierarchieebene['Punkte'].tolist()
col_punkte_prozesse = df_prozesse_for_mittlerer_Hierarchieebene['Punkte'].tolist()
# print(col_punkte_tech)


#Df auf mittlerer HE
prozesse_frage_punkte_dic = {
    0: 'KI Best Practices',
    1: 'Prozess zur Identifikation von KI-Einsatzfeldern',
    2: 'Prozess zur Identifikation von KI-Einsatzfeldern',
    3: 'Prozess zur Identifikation von KI-Einsatzfeldern',
    4: 'Prozess zur Identifikation von KI-Einsatzfeldern',
}
prozesse_katerogie_punkte_dic = {
    'KI Best Practices': 0,
    'Prozess zur Identifikation von KI-Einsatzfeldern': 0
}
#print(prozesse_frage_punkte_dic[0])

for i, p in enumerate(col_punkte_prozesse):
    k = prozesse_frage_punkte_dic[i]
    prozesse_katerogie_punkte_dic[k] += p

# print(prozesse_katerogie_punkte_dic)

# todo Durchschnitt

col_punkte_prozesse_mittlere_Hierarchieebene = prozesse_katerogie_punkte_dic.values()
print(prozesse_katerogie_punkte_dic)
punke_pro_kategorie = list(prozesse_katerogie_punkte_dic.keys())
kategorien = list(prozesse_katerogie_punkte_dic.values())
# print(kategorien)
# df_lola = pd.DataFrame(prozesse_katerogie_punkte_dic) // WHY DOES IT NOT WORK
# print(df_lola)

# create empty data frame in pandas
df_lola = pd.DataFrame()
df_lola['Kategorie'] = punke_pro_kategorie
df_lola['Punkte'] = kategorien
#st.write(df_lola)

#Df auf mittlerer HE
technologie_frage_punkte_dic = {
    0: 'Daten Hosting',
    1: 'Daten Hosting',
    2: 'Daten Hosting',
    3: 'Modelle und Werkzeuge',
    4: 'Modelle und Werkzeuge',
    5: 'Modelle und Werkzeuge',
    6: 'Modelle und Werkzeuge',
    7: 'Modelle und Werkzeuge',
    8: 'Data Warehouse Plattform',
    9: 'Data Warehouse Plattform',
    10: 'Data Warehouse Plattform',
    11: 'Data Warehouse Plattform',
    12: 'BI Infrastruktur',
    13: 'BI Infrastruktur',
    14: 'BI Infrastruktur',
}
technologie_katerogie_punkte_dic = {
    'Daten Hosting': 0,
    'Modelle und Werkzeuge': 0,
    'Data Warehouse Plattform':0,
    'BI Infrastruktur':0,
}
#print(prozesse_frage_punkte_dic[0])
print(col_punkte_data)
for i, p in enumerate(col_punkte_data):
    k = technologie_frage_punkte_dic[i]
    technologie_katerogie_punkte_dic[k] += p

# print(prozesse_katerogie_punkte_dic)

# todo Durchschnitt

col_punkte_technologie_mittlere_Hierarchieebene = technologie_katerogie_punkte_dic.values()
#print(prozesse_katerogie_punkte_dic)
punke_pro_kategorie_tech = list(technologie_katerogie_punkte_dic.keys())
kategorien_tech = list(technologie_katerogie_punkte_dic.values())
# print(kategorien)
# df_lola = pd.DataFrame(prozesse_katerogie_punkte_dic) // WHY DOES IT NOT WORK
# print(df_lola)

# create empty data frame in pandas
df_lola_tech = pd.DataFrame()
df_lola_tech['Kat'] = punke_pro_kategorie_tech
df_lola_tech['Punkte'] = kategorien_tech
# st.write(df_lola_tech)

# SpiderMap
df = pd.DataFrame(dict(
    r=col_punkte,
    theta=['Daten', 'Organisation und Expertise', 'Prozesse in Bezug auf KI',
           'Technologie']))
fig = px.line_polar(df, r='r', theta='theta', line_close=True)
# Dataframes to plot
df_data_drilldown = transfor_to_dimension_drilldown_data(col_punkte_data)
df_orga_drilldown = transfor_to_dimension_drilldown_orga(col_punkte_orga)
# --- Layout ---
intro = """ Herzlichen Glückwunsch zum Abschluss Ihrer KI-Reifeprüfung!
Diese Seite führt Sie durch die Interpretation Ihrer Bewertungsergebnisse und schließt mit konkretten next Steps ab. """

four_dimensions_intro = """Hier sehen Sie einen Überblick über den Reifegrad Ihres Unternehmens über die 4 verschiedenen Dimensionen, die vom KI-Reifetool bewertet werden. """
each_dimension_intro = """Wir wollen nun einen detaillierten Einblick in jede Dimension gewinnen.  """
tech_intro = """ Um das volle Potenzial von KI zu erschöpfen, ist eine gute IT-Infrastruktur und –Technologie unumgänglich. Insbesondere geht es hier um kritische Hardware-und Softwareentscheidungen. """
tech_level1 = """ Ihr aktueller Reifegrad ist Level 1: Dies zeichnet sich vor allem dadurch aus,dass sich Daten in unterschiedlichen Blöcken befinden, die an mehreren Orten im gesamtenUnternehmen in Tabellenkalkulationen, E-Mails und in dezentralen Datenbanken gespeichertsind. Der Organisation fehlen noch die Softwaretools und die Rechenleistung, die für dieeffiziente Durchführung von KI-Projekten erforderlich sind. """
description_daten = """KI lebt von den Daten, die ihr zur Verfügung gestellt werden und nehmen so eine entscheidende Rolle in der Entwicklung von KI ein. Im Vordergrund steht hierbei nicht nur die Verfügbarkeit von Daten, sondern auch deren Qualität. Eine gut definierte Dateninfrastruktur, die den Zugriff auf Daten und die Gewinnung von Kennzahlen aus Daten erleichtert, ist also eine zentrale Voraussetzung für effiziente KI.  """
description_daten_level1 = """Im Bereich Daten befindet sich ihr Unternehmen aktuell auf Reifegrad Level 1: Das Unternehmen hat das Potenzial von Daten noch nicht erkannt. In Folge liegen die Daten nicht zentralisiert vor. Ein umfassendes Verständnis der wichtigsten Datenbestände ist nicht möglich und eine umfangreiche Datenanalyse nicht durchführbar. Es werden   keine Daten aus den Kernprozessen gesammelt und es fehlt das notwendige Know-how, um eine Datenbereinigung durchzuführen. Das Unternehmen verfügt über keinen Prozess zur Gewährleistung der Datenqualität und ist sich der Notwendigkeit einer langfristigen Datenpflege nicht bewusst. """
body2 = """ Um auf Ihr Unternehmen auf die nächste Stufe in Richtung KI Experte zu heben, können Sie folgendeMaßnahmen ergreifen:"""
handlungsempf = """Im Folgenden finden sie Handlungsempfehlungen, um an den konkreten Entwicklungsfeldern Ihres Unternehmens zu arbeiten.

Im Bereich Technologie sollte als nächster Schritt vor allem das Daten Hosting verbessert werden.  

Im Bereich Daten sollte in naher Zukunft vor allem das Datenmonitoring durchleuchtet und verbessert werden. """

st.title(":bar_chart: Ergebnisse KI Reifegradermittlung")
st.markdown(intro)
# st.write("ALTERNATIVE 1")
# bar_chart_1 = px.bar(dimension_level_df)
# st.write(bar_chart_1)
# st.write("ALTERNATIVE 2")
# st.bar_chart(dimension_level_df)
# st.write("ALTERNATIV 3")

st.header("KI-Reife über die 4 Dimensionen")
st.markdown(four_dimensions_intro)
fig

st.header("KI-Reife innerhalb der Dimensionen ")
st.markdown(each_dimension_intro)
# st.subheader("Technologie")
# st.write(px.bar(df_tech, orientation='h'))
# st.subheader("Daten")
# st.write(px.bar(df_daten, orientation='h'))
# st.subheader("Organisation")
# st.write(px.bar(df_orga, orientation='h'))
st.subheader("Technologie")
st.markdown(tech_intro)
# st.write(px.bar(df_prozesse, orientation='h'))
# st.write(df_prozesse)
# st.write("----------------------------------------")
# st.write(df_lola_tech)
df_lola_tech = df_lola_tech.set_index('Kat')
st.write(px.bar(df_lola_tech))
st.markdown(tech_level1)

st.subheader("Daten")
st.markdown(description_daten)
df_data_drilldown = df_data_drilldown.set_index('Kat')
st.write(px.bar(df_data_drilldown))
st.markdown(description_daten_level1)

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
st.markdown(handlungsempf)


