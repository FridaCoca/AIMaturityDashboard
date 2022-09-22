import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px

import textbausteine
import variables as var
import dics as dics

import report_text_modules as rtm

# --- Functions
from block_statement import BlockStatement
from category import CategoryName


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


def assign_levels_in_dimension(df):
    conditions = [
        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_daten_hosting[1]) & (df['Kategorien'] == 'Daten Hosting')),
        ((df["Punkte"] > var.boundries_daten_hosting[1]) & (df["Punkte"] <= var.boundries_daten_hosting[2]) & (
                df['Kategorien'] == 'Daten Hosting')),
        ((df["Punkte"] > var.boundries_daten_hosting[2]) & (df["Punkte"] <= var.boundries_daten_hosting[3]) & (
                df['Kategorien'] == 'Daten Hosting')),
        ((df["Punkte"] > var.boundries_daten_hosting[3]) & (df["Punkte"] <= var.boundries_daten_hosting[4]) & (
                df['Kategorien'] == 'Daten Hosting')),
        ((df["Punkte"] > var.boundries_daten_hosting[4]) & (df["Punkte"] <= var.boundries_daten_hosting[5]) & (
                df['Kategorien'] == 'Daten Hosting')),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_modelle_und_werkzeuge[1]) & (
                df['Kategorien'] == 'Modelle und Werkzeuge')),
        ((df["Punkte"] > var.boundries_modelle_und_werkzeuge[1]) & (
                df["Punkte"] <= var.boundries_modelle_und_werkzeuge[2])) & (
                df['Kategorien'] == 'Modelle und Werkzeuge'),
        ((df["Punkte"] > var.boundries_modelle_und_werkzeuge[2]) & (
                df["Punkte"] <= var.boundries_modelle_und_werkzeuge[3])) & (
                df['Kategorien'] == 'Modelle und Werkzeuge'),
        ((df["Punkte"] > var.boundries_modelle_und_werkzeuge[3]) & (
                df["Punkte"] <= var.boundries_modelle_und_werkzeuge[4])) & (
                df['Kategorien'] == 'Modelle und Werkzeuge'),
        ((df["Punkte"] > var.boundries_modelle_und_werkzeuge[4]) & (
                df["Punkte"] <= var.boundries_modelle_und_werkzeuge[5])) & (
                df['Kategorien'] == 'Modelle und Werkzeuge'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_data_warehouse_plattform[1]) & (
                df['Kategorien'] == 'Data Warehouse Plattform')),
        ((df["Punkte"] > var.boundries_data_warehouse_plattform[1]) & (
                df["Punkte"] <= var.boundries_data_warehouse_plattform[2])) & (
                df['Kategorien'] == 'Data Warehouse Plattform'),
        ((df["Punkte"] > var.boundries_data_warehouse_plattform[2]) & (
                df["Punkte"] <= var.boundries_data_warehouse_plattform[3])) & (
                df['Kategorien'] == 'Data Warehouse Plattform'),
        ((df["Punkte"] > var.boundries_data_warehouse_plattform[3]) & (
                df["Punkte"] <= var.boundries_data_warehouse_plattform[4])) & (
                df['Kategorien'] == 'Data Warehouse Plattform'),
        ((df["Punkte"] > var.boundries_data_warehouse_plattform[4]) & (
                df["Punkte"] <= var.boundries_data_warehouse_plattform[5])) & (
                df['Kategorien'] == 'Data Warehouse Plattform'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[1]) & (
                df['Kategorien'] == 'BI Infrastruktur')),
        ((df["Punkte"] > var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[1]) & (
                df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[2])) & (
                df['Kategorien'] == 'BI Infrastruktur'),
        ((df["Punkte"] > var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[2]) & (
                df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[3])) & (
                df['Kategorien'] == 'BI Infrastruktur'),
        ((df["Punkte"] > var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[3]) & (
                df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[4])) & (
                df['Kategorien'] == 'BI Infrastruktur'),
        ((df["Punkte"] > var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[4]) & (
                df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[5])) & (
                df['Kategorien'] == 'BI Infrastruktur'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_data_driven_culture[1]) & (
                df['Kategorien'] == 'Data Driven Culture')),
        ((df["Punkte"] > var.boundries_data_driven_culture[1]) & (
                df["Punkte"] <= var.boundries_data_driven_culture[2]) & (
                 df['Kategorien'] == 'Data Driven Culture')),
        ((df["Punkte"] > var.boundries_data_driven_culture[2]) & (
                df["Punkte"] <= var.boundries_data_driven_culture[3]) & (
                 df['Kategorien'] == 'Data Driven Culture')),
        ((df["Punkte"] > var.boundries_data_driven_culture[3]) & (
                df["Punkte"] <= var.boundries_data_driven_culture[4]) & (
                 df['Kategorien'] == 'Data Driven Culture')),
        ((df["Punkte"] > var.boundries_data_driven_culture[4]) & (
                df["Punkte"] <= var.boundries_data_driven_culture[5]) & (
                 df['Kategorien'] == 'Data Driven Culture')),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_datenherkunft_und_haltung[1]) & (
                df['Kategorien'] == 'Modelle und Werkzeuge')),
        ((df["Punkte"] > var.boundries_datenherkunft_und_haltung[1]) & (
                df["Punkte"] <= var.boundries_datenherkunft_und_haltung[2])) & (
                df['Kategorien'] == 'Datenherkunft und -haltung'),
        ((df["Punkte"] > var.boundries_datenherkunft_und_haltung[2]) & (
                df["Punkte"] <= var.boundries_datenherkunft_und_haltung[3])) & (
                df['Kategorien'] == 'Datenherkunft und -haltung'),
        ((df["Punkte"] > var.boundries_datenherkunft_und_haltung[3]) & (
                df["Punkte"] <= var.boundries_datenherkunft_und_haltung[4])) & (
                df['Kategorien'] == 'Datenherkunft und -haltung'),
        ((df["Punkte"] > var.boundries_datenherkunft_und_haltung[4]) & (
                df["Punkte"] <= var.boundries_datenherkunft_und_haltung[5])) & (
                df['Kategorien'] == 'Datenherkunft und -haltung'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_datenqualität[1]) & (
                df['Kategorien'] == 'Datenqualität')),
        ((df["Punkte"] > var.boundries_datenqualität[1]) & (
                df["Punkte"] <= var.boundries_datenqualität[2])) & (
                df['Kategorien'] == 'Datenqualität'),
        ((df["Punkte"] > var.boundries_datenqualität[2]) & (
                df["Punkte"] <= var.boundries_datenqualität[3])) & (
                df['Kategorien'] == 'Datenqualität'),
        ((df["Punkte"] > var.boundries_datenqualität[3]) & (
                df["Punkte"] <= var.boundries_datenqualität[4])) & (
                df['Kategorien'] == 'Datenqualität'),
        ((df["Punkte"] > var.boundries_datenqualität[4]) & (
                df["Punkte"] <= var.boundries_datenqualität[5])) & (
                df['Kategorien'] == 'Datenqualität'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_datamonitoring_governance_und_policies[1]) & (
                df['Kategorien'] == 'Datamonitoring, -governance und -policies')),
        ((df["Punkte"] > var.boundries_datamonitoring_governance_und_policies[1]) & (
                df["Punkte"] <= var.boundries_datamonitoring_governance_und_policies[2])) & (
                df['Kategorien'] == 'Datamonitoring, -governance und -policies'),
        ((df["Punkte"] > var.boundries_datamonitoring_governance_und_policies[2]) & (
                df["Punkte"] <= var.boundries_datamonitoring_governance_und_policies[3])) & (
                df['Kategorien'] == 'Datamonitoring, -governance und -policies'),
        ((df["Punkte"] > var.boundries_datamonitoring_governance_und_policies[3]) & (
                df["Punkte"] <= var.boundries_datamonitoring_governance_und_policies[4])) & (
                df['Kategorien'] == 'Datamonitoring, -governance und -policies'),
        ((df["Punkte"] > var.boundries_datamonitoring_governance_und_policies[4]) & (
                df["Punkte"] <= var.boundries_datamonitoring_governance_und_policies[5])) & (
                df['Kategorien'] == 'Datamonitoring, -governance und -policies'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_rechtliche_grundlagen[1]) & (
                df['Kategorien'] == 'Rechtliche Grundlagen')),
        ((df["Punkte"] > var.boundries_rechtliche_grundlagen[1]) & (
                df["Punkte"] <= var.boundries_rechtliche_grundlagen[2])) & (
                df['Kategorien'] == 'Rechtliche Grundlagen'),
        ((df["Punkte"] > var.boundries_rechtliche_grundlagen[2]) & (
                df["Punkte"] <= var.boundries_rechtliche_grundlagen[3])) & (
                df['Kategorien'] == 'Rechtliche Grundlagen'),
        ((df["Punkte"] > var.boundries_rechtliche_grundlagen[3]) & (
                df["Punkte"] <= var.boundries_rechtliche_grundlagen[4])) & (
                df['Kategorien'] == 'Rechtliche Grundlagen'),
        ((df["Punkte"] > var.boundries_rechtliche_grundlagen[4]) & (
                df["Punkte"] <= var.boundries_rechtliche_grundlagen[5])) & (
                df['Kategorien'] == 'Rechtliche Grundlagen'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_bi_expertise[1]) & (
                df['Kategorien'] == 'BI Expertise')),
        ((df["Punkte"] > var.boundries_bi_expertise[1]) & (
                df["Punkte"] <= var.boundries_bi_expertise[2])) & (
                df['Kategorien'] == 'BI Expertise'),
        ((df["Punkte"] > var.boundries_bi_expertise[2]) & (
                df["Punkte"] <= var.boundries_bi_expertise[3])) & (
                df['Kategorien'] == 'BI Expertise'),
        ((df["Punkte"] > var.boundries_bi_expertise[3]) & (
                df["Punkte"] <= var.boundries_bi_expertise[4])) & (
                df['Kategorien'] == 'BI Expertise'),
        ((df["Punkte"] > var.boundries_bi_expertise[4]) & (
                df["Punkte"] <= var.boundries_bi_expertise[5])) & (
                df['Kategorien'] == 'BI Expertise'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_bestehende_ki_lösungen_im_unternehmen[1]) & (
                df['Kategorien'] == 'Bestehende KI Lösungen im Unternehmen')),
        ((df["Punkte"] > var.boundries_bestehende_ki_lösungen_im_unternehmen[1]) & (
                df["Punkte"] <= var.boundries_bestehende_ki_lösungen_im_unternehmen[2])) & (
                df['Kategorien'] == 'Bestehende KI Lösungen im Unternehmen'),
        ((df["Punkte"] > var.boundries_bestehende_ki_lösungen_im_unternehmen[2]) & (
                df["Punkte"] <= var.boundries_bestehende_ki_lösungen_im_unternehmen[3])) & (
                df['Kategorien'] == 'Bestehende KI Lösungen im Unternehmen'),
        ((df["Punkte"] > var.boundries_bestehende_ki_lösungen_im_unternehmen[3]) & (
                df["Punkte"] <= var.boundries_bestehende_ki_lösungen_im_unternehmen[4])) & (
                df['Kategorien'] == 'Bestehende KI Lösungen im Unternehmen'),
        ((df["Punkte"] > var.boundries_bestehende_ki_lösungen_im_unternehmen[4]) & (
                df["Punkte"] <= var.boundries_bestehende_ki_lösungen_im_unternehmen[5])) & (
                df['Kategorien'] == 'Bestehende KI Lösungen im Unternehmen'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_strategie[1]) & (
                df['Kategorien'] == 'Strategie')),
        ((df["Punkte"] > var.boundries_strategie[1]) & (
                df["Punkte"] <= var.boundries_strategie[2])) & (
                df['Kategorien'] == 'Strategie'),
        ((df["Punkte"] > var.boundries_strategie[2]) & (
                df["Punkte"] <= var.boundries_strategie[3])) & (
                df['Kategorien'] == 'Strategie'),
        ((df["Punkte"] > var.boundries_strategie[3]) & (
                df["Punkte"] <= var.boundries_strategie[4])) & (
                df['Kategorien'] == 'Strategie'),
        ((df["Punkte"] > var.boundries_strategie[4]) & (
                df["Punkte"] <= var.boundries_strategie[5])) & (
                df['Kategorien'] == 'Strategie'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_ki_best_practices[1]) & (
                df['Kategorien'] == 'KI Best Practices')),
        ((df["Punkte"] > var.boundries_ki_best_practices[1]) & (
                df["Punkte"] <= var.boundries_ki_best_practices[2])) & (
                df['Kategorien'] == 'KI Best Practices'),
        ((df["Punkte"] > var.boundries_ki_best_practices[2]) & (
                df["Punkte"] <= var.boundries_ki_best_practices[3])) & (
                df['Kategorien'] == 'KI Best Practices'),
        ((df["Punkte"] > var.boundries_ki_best_practices[3]) & (
                df["Punkte"] <= var.boundries_ki_best_practices[4])) & (
                df['Kategorien'] == 'KI Best Practices'),
        ((df["Punkte"] > var.boundries_ki_best_practices[4]) & (
                df["Punkte"] <= var.boundries_ki_best_practices[5])) & (
                df['Kategorien'] == 'KI Best Practices'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[1]) & (
                df['Kategorien'] == 'Prozess zur Identifikation von KI-Einsatzfeldern')),
        ((df["Punkte"] > var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[1]) & (
                df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[2])) & (
                df['Kategorien'] == 'Prozess zur Identifikation von KI-Einsatzfeldern'),
        ((df["Punkte"] > var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[2]) & (
                df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[3])) & (
                df['Kategorien'] == 'Prozess zur Identifikation von KI-Einsatzfeldern'),
        ((df["Punkte"] > var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[3]) & (
                df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[4])) & (
                df['Kategorien'] == 'Prozess zur Identifikation von KI-Einsatzfeldern'),
        ((df["Punkte"] > var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[4]) & (
                df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[5])) & (
                df['Kategorien'] == 'Prozess zur Identifikation von KI-Einsatzfeldern'),
    ]

    values = [1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5]

    df['Stufe'] = np.select(conditions, values)
    df = df.filter(['Kategorien', 'Stufe'], axis=1)
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


def assign_levels(df):
    conditions = [
        ((df["Punkte Pro Dimension"] > 0) & (df["Punkte Pro Dimension"] <= var.upper_bound_tech_level1) & (
                df['Gestaltungsdimension'] == 'Technologie')),
        ((df["Punkte Pro Dimension"] > var.upper_bound_tech_level1) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_tech_level2)) & (
                df['Gestaltungsdimension'] == 'Technologie'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_tech_level2) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_tech_level3)) & (
                df['Gestaltungsdimension'] == 'Technologie'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_tech_level3) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_tech_level4)) & (
                df['Gestaltungsdimension'] == 'Technologie'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_tech_level4) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_tech_level5)) & (
                df['Gestaltungsdimension'] == 'Technologie'),

        ((df["Punkte Pro Dimension"] > 0) & (df["Punkte Pro Dimension"] <= var.upper_bound_data_level1) & (
                df['Gestaltungsdimension'] == 'Daten')),
        ((df["Punkte Pro Dimension"] > var.upper_bound_data_level1) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_data_level2)) & (
                df['Gestaltungsdimension'] == 'Daten'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_data_level2) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_data_level3)) & (
                df['Gestaltungsdimension'] == 'Daten'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_data_level3) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_data_level4)) & (
                df['Gestaltungsdimension'] == 'Daten'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_data_level4) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_data_level5)) & (
                df['Gestaltungsdimension'] == 'Daten'),

        ((df["Punkte Pro Dimension"] > 0) & (df["Punkte Pro Dimension"] <= var.upper_bound_orga_level1) & (
                df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI')),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level1) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_orga_level2)) & (
                df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level2) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_orga_level3)) & (
                df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level3) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_orga_level4)) & (
                df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level4) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_orga_level5)) & (
                df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI'),

        ((df["Punkte Pro Dimension"] > 0) & (df["Punkte Pro Dimension"] <= var.upper_bound_orga_level1) & (
                df['Gestaltungsdimension'] == 'Organisation und Expertise')),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level1) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_orga_level2)) & (
                df['Gestaltungsdimension'] == 'Organisation und Expertise'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level2) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_orga_level3)) & (
                df['Gestaltungsdimension'] == 'Organisation und Expertise'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level3) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_orga_level4)) & (
                df['Gestaltungsdimension'] == 'Organisation und Expertise'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level4) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_orga_level5)) & (
                df['Gestaltungsdimension'] == 'Organisation und Expertise')
    ]

    values = [1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5,
              1, 2, 3, 4, 5]

    df['Stufe'] = np.select(conditions, values)
    return df


def transform_to_dimension_drilldown(main_df, questions_points_dic, cat_points_dic, dimension):
    df_kat = main_df[main_df['Gestaltungsdimension'] == dimension]
    df_kat = df_kat.filter(['Frage', 'Durchschnitt Punkte'], axis=1)
    col_punkte_kat = df_kat['Durchschnitt Punkte'].tolist()

    for i, p in enumerate(col_punkte_kat):
        k = questions_points_dic[i]
        cat_points_dic[k] += p

    points_by_subkat = list(cat_points_dic.keys())
    subkats = list(cat_points_dic.values())

    points_by_subkat_df = pd.DataFrame()
    points_by_subkat_df['Kategorien'] = points_by_subkat
    points_by_subkat_df['Punkte'] = subkats
    points_by_subkat_df = assign_levels_in_dimension(points_by_subkat_df)
    return points_by_subkat_df


def create_List(main_df, dimension):
    df_kat = main_df[main_df['Gestaltungsdimension'] == dimension]
    df_kat = df_kat.filter(['Frage', 'Durchschnitt Punkte'], axis=1)
    col_frage_punkte = df_kat['Durchschnitt Punkte'].tolist()
    return col_frage_punkte


# def create_text(col_frage_punkte: [], kategorie : rtm.Text_Kategorie):
#     text = ""
#     i = 0
#     for x in kategorie.statements:
#         if col_frage_punkte[i] >= 2:
#             text += (x.get_text(2))
#         i += 1
#     return text
#
#
def get_category_points(category_name: CategoryName):
    return data_drilldown_df.loc[data_drilldown_df.Kategorien == category_name.value, 'Stufe'].tolist()[0]


# --- dataframes and spidermap for dimension-Level-representation
df = pd.read_excel('survey.xlsx')
df = transform_to_question_dimension_average_points_df(df)
dimension_level_df = transform_to_dimension_level_df(df)
bar_chart_dimension_level_df = px.bar(dimension_level_df, x='Gestaltungsdimension', y='Stufe')
spider_dimension_level = spidermap(dimension_level_df)

# --- dataframes for dimension drilldown
tech_drilldown_df = transform_to_dimension_drilldown(df, dics.questions_points_tech, dics.cat_points_tech,
                                                     'Technologie')
data_drilldown_df = transform_to_dimension_drilldown(df, dics.questions_points_data, dics.cat_points_data, 'Daten')
processes_drilldown_df = transform_to_dimension_drilldown(df, dics.questions_points_processes,
                                                          dics.cat_points_processes, 'Prozesse im Bezug auf KI')
orga_drilldown_df = transform_to_dimension_drilldown(df, dics.questions_points_orga, dics.cat_points_orga,
                                                     'Organisation und Expertise')
st.write(data_drilldown_df)
# create_text2()

# --- points_dimension_lists for the paragraph
points_orga_list = create_List(df, 'Organisation und Expertise')
points_data_list = create_List(df, 'Daten')
points_tech_list = create_List(df, 'Vision, Strategie und Expertise')
points_tech_list = create_List(df, 'Technologie')
points_processes_list = create_List(df, 'Organisation und Expertise')
st.write('---------------------')
st.write(points_orga_list)
# text_Orga = create_text(points_orga_list, rtm.test_kategorie)
# st.write(text_Orga)
st.write('---------------------')

# --- Layout ---
st.title(":bar_chart: Ergebnisse KI Reifegradermittlung")
st.markdown(textbausteine.intro)

st.header("KI-Reife über die 4 Dimensionen")
st.markdown(textbausteine.four_dimensions_intro)
spider_dimension_level

st.header("KI-Reife innerhalb der Dimensionen ")
st.markdown(textbausteine.each_dimension_intro)

st.subheader("Technologie")
st.markdown(textbausteine.tech_description)
st.write(px.bar(tech_drilldown_df, x='Kategorien', y='Stufe'))
st.markdown(textbausteine.tech_level1)

st.subheader("Daten")
st.markdown(textbausteine.daten_description)
st.write(px.bar(data_drilldown_df, x='Kategorien', y='Stufe'))
st.markdown(textbausteine.description_daten_level1)

st.subheader("Organisation und Expertise")
st.markdown(textbausteine.orga_description)
st.write(px.bar(orga_drilldown_df, x='Kategorien', y='Stufe'))

st.subheader("Prozesse im Bezug auf KI")
st.markdown(textbausteine.processes_description)
st.write(px.bar(processes_drilldown_df, x='Kategorien', y='Stufe'))

st.header("Handlungsempfehlungen:")
st.markdown(textbausteine.handlungsempf)

# Binary
print(rtm.binaryCategory.get_statement_result([1, 2, 3, 4, 5, 6, 7]))

# Block
statement_category_name = rtm.blockCategory.statements[0].category_name
category_points = get_category_points(statement_category_name)
print(category_points)
print(rtm.blockCategory.get_statement_result([category_points]))
