from os.path import exists

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

import dics as dics
import report_text_modules as rtm
import textbausteine
import variables as var
from category import CategoryName
from network.sharepoint_list_repository import download_list

# download_list(
#     list_name="form_results_list",
#     export_type="Excel",
#     dir_path="./form_results",
#     file_name="results.xlsx"
# )

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
    st.write("in calc points")
    st.write(df)
    print(df.dtypes)
    # for i in range(number_Participants):
    #     df[[i]] = df[[i]].astype(str).astype(int)
    df = df.astype({"Punkte": int})
    st.write(df)
    df['Punkte'] = df.sum(axis=1)
    print("ok")
    return df


def calculate_average_points(df):
    st.write("hier BEDUGEGE:")
    st.write(df)

    for i in range(number_Participants):
        df = df.drop([i], axis=1)
    df['Punkte'] = df['Punkte'].div(number_Participants).round(1)
    df = df.rename({'Punkte': 'Durchschnitt Punkte'}, axis=1)
    return df

def clean(df):
    # st.write("----- Print 1 -----")
    # st.write(df)
    df = df.drop(columns=['FileSystemObjectType', 'Id', 'ServerRedirectedEmbedUri', 'ServerRedirectedEmbedUrl', 'ID',
                          'ContentTypeId', 'Title', 'Modified', 'Created', 'AuthorId', 'EditorId',
                          'OData__UIVersionString', 'Attachments', 'GUID', 'ComplianceAssetId',
                          'field_0', 'field_2'])
    df = df.replace(
        to_replace={'trifft nicht zu': 0, 'trifft eher nicht zu': 1, 'trifft eher  nicht zu': 1,
                    'teils teils': 2, 'trifft eher zu': 3,
                    'trifft zu': 4, 'Ich kann keine Aussage treffen.': 0, '<NA>': 0})
    return df

def filter_with_password(df):
    df_result_search = pd.DataFrame()
    password_search = st.number_input("password")
    # st.write(password_search)
    # df = df.astype({'Password': 'Int64'})
    # print(df.dtypes)
    st.button("search")
    df_result_search = df[df['Password'] == (password_search)]
    df_result_search = df_result_search.drop(columns=['Password'])
    st.write("result:")
    df_result_search = df_result_search.rename(index={0: 'Punkte'})
    st.write(df_result_search)
    return df_result_search


def transform_to_question_dimension_average_points_df(df):
    df = df.transpose()
    #st.write("----- Print 2 -----")
    df.columns = ["Punkte"]
    #st.write(df)
    df = df.reset_index()
    # st.write("----- Print 3 -----")
    # st.write(df)
    df = df.drop(['index'], axis=1)
    df = assign_dimensions(df)
    # st.write("----- Print 4 -----")
    # st.write(df)
    # st.write("----- Print 5 -----")
    # st.write(df)
   # df = calculate_sum_points(df)
   #  st.write("----- Print 6 -----")
   #  df = calculate_average_points(df)
    return df


def assign_levels_in_dimension(df):
    conditions = [
        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_daten_hosting[1]) & (df['Kategorien'] == 'Daten Hosting')),
        ((df["Punkte"] > var.boundries_daten_hosting[1]) & (df["Punkte"] <= var.boundries_daten_hosting[2]) & (
                df['Kategorien'] == 'Daten Hosting')),
        ((df["Punkte"] > var.boundries_daten_hosting[2]) & (df["Punkte"] <= var.boundries_daten_hosting[3]) & (
                df['Kategorien'] == 'Daten Hosting')),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_modelle_und_werkzeuge[1]) & (
                df['Kategorien'] == 'Modelle und Werkzeuge')),
        ((df["Punkte"] > var.boundries_modelle_und_werkzeuge[1]) & (
                df["Punkte"] <= var.boundries_modelle_und_werkzeuge[2])) & (
                df['Kategorien'] == 'Modelle und Werkzeuge'),
        ((df["Punkte"] > var.boundries_modelle_und_werkzeuge[2]) & (
                df["Punkte"] <= var.boundries_modelle_und_werkzeuge[3])) & (
                df['Kategorien'] == 'Modelle und Werkzeuge'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_data_warehouse_plattform[1]) & (
                df['Kategorien'] == 'Data Warehouse Plattform')),
        ((df["Punkte"] > var.boundries_data_warehouse_plattform[1]) & (
                df["Punkte"] <= var.boundries_data_warehouse_plattform[2])) & (
                df['Kategorien'] == 'Data Warehouse Plattform'),
        ((df["Punkte"] > var.boundries_data_warehouse_plattform[2]) & (
                df["Punkte"] <= var.boundries_data_warehouse_plattform[3])) & (
                df['Kategorien'] == 'Data Warehouse Plattform'),


        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[1]) & (
                df['Kategorien'] == 'BI Infrastruktur')),
        ((df["Punkte"] > var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[1]) & (
                df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[2])) & (
                df['Kategorien'] == 'BI Infrastruktur'),
        ((df["Punkte"] > var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[2]) & (
                df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[3])) & (
                df['Kategorien'] == 'BI Infrastruktur'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_data_driven_culture[1]) & (
                df['Kategorien'] == 'Data Driven Culture')),
        ((df["Punkte"] > var.boundries_data_driven_culture[1]) & (
                df["Punkte"] <= var.boundries_data_driven_culture[2]) & (
                 df['Kategorien'] == 'Data Driven Culture')),
        ((df["Punkte"] > var.boundries_data_driven_culture[2]) & (
                df["Punkte"] <= var.boundries_data_driven_culture[3]) & (
                 df['Kategorien'] == 'Data Driven Culture')),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_datenherkunft_und_haltung[1]) & (
                df['Kategorien'] == 'Modelle und Werkzeuge')),
        ((df["Punkte"] > var.boundries_datenherkunft_und_haltung[1]) & (
                df["Punkte"] <= var.boundries_datenherkunft_und_haltung[2])) & (
                df['Kategorien'] == 'Datenherkunft und -haltung'),
        ((df["Punkte"] > var.boundries_datenherkunft_und_haltung[2]) & (
                df["Punkte"] <= var.boundries_datenherkunft_und_haltung[3])) & (
                df['Kategorien'] == 'Datenherkunft und -haltung'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_datenqualität[1]) & (
                df['Kategorien'] == 'Datenqualität')),
        ((df["Punkte"] > var.boundries_datenqualität[1]) & (
                df["Punkte"] <= var.boundries_datenqualität[2])) & (
                df['Kategorien'] == 'Datenqualität'),
        ((df["Punkte"] > var.boundries_datenqualität[2]) & (
                df["Punkte"] <= var.boundries_datenqualität[3])) & (
                df['Kategorien'] == 'Datenqualität'),


        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_datamonitoring_governance_und_policies[1]) & (
                df['Kategorien'] == 'Datamonitoring, -governance und -policies')),
        ((df["Punkte"] > var.boundries_datamonitoring_governance_und_policies[1]) & (
                df["Punkte"] <= var.boundries_datamonitoring_governance_und_policies[2])) & (
                df['Kategorien'] == 'Datamonitoring, -governance und -policies'),
        ((df["Punkte"] > var.boundries_datamonitoring_governance_und_policies[2]) & (
                df["Punkte"] <= var.boundries_datamonitoring_governance_und_policies[3])) & (
                df['Kategorien'] == 'Datamonitoring, -governance und -policies'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_rechtliche_grundlagen[1]) & (
                df['Kategorien'] == 'Rechtliche Grundlagen')),
        ((df["Punkte"] > var.boundries_rechtliche_grundlagen[1]) & (
                df["Punkte"] <= var.boundries_rechtliche_grundlagen[2])) & (
                df['Kategorien'] == 'Rechtliche Grundlagen'),
        ((df["Punkte"] > var.boundries_rechtliche_grundlagen[2]) & (
                df["Punkte"] <= var.boundries_rechtliche_grundlagen[3])) & (
                df['Kategorien'] == 'Rechtliche Grundlagen'),

        # ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_ki_vision[1]) & (
        #         df['Kategorien'] == 'KI-Vision')),
        # ((df["Punkte"] > var.boundries_ki_vision[1]) & (
        #         df["Punkte"] <= var.boundries_ki_vision[2])) & (
        #         df['Kategorien'] == 'KI-Vision'),
        # ((df["Punkte"] > var.boundries_ki_vision[2]) & (
        #         df["Punkte"] <= var.boundries_ki_vision[3])) & (
        #         df['Kategorien'] == 'KI-Vision'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_bi_expertise[1]) & (
                df['Kategorien'] == 'BI Expertise')),
        ((df["Punkte"] > var.boundries_bi_expertise[1]) & (
                df["Punkte"] <= var.boundries_bi_expertise[2])) & (
                df['Kategorien'] == 'BI Expertise'),
        ((df["Punkte"] > var.boundries_bi_expertise[2]) & (
                df["Punkte"] <= var.boundries_bi_expertise[3])) & (
                df['Kategorien'] == 'BI Expertise'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_bestehende_ki_lösungen_im_unternehmen[1]) & (
                df['Kategorien'] == 'Bestehende KI Lösungen im Unternehmen')),
        ((df["Punkte"] > var.boundries_bestehende_ki_lösungen_im_unternehmen[1]) & (
                df["Punkte"] <= var.boundries_bestehende_ki_lösungen_im_unternehmen[2])) & (
                df['Kategorien'] == 'Bestehende KI Lösungen im Unternehmen'),
        ((df["Punkte"] > var.boundries_bestehende_ki_lösungen_im_unternehmen[2]) & (
                df["Punkte"] <= var.boundries_bestehende_ki_lösungen_im_unternehmen[3])) & (
                df['Kategorien'] == 'Bestehende KI Lösungen im Unternehmen'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_strategie[1]) & (
                df['Kategorien'] == 'Strategie')),
        ((df["Punkte"] > var.boundries_strategie[1]) & (
                df["Punkte"] <= var.boundries_strategie[2])) & (
                df['Kategorien'] == 'Strategie'),
        ((df["Punkte"] > var.boundries_strategie[2]) & (
                df["Punkte"] <= var.boundries_strategie[3])) & (
                df['Kategorien'] == 'Strategie'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_ki_best_practices[1]) & (
                df['Kategorien'] == 'KI Best Practices')),
        ((df["Punkte"] > var.boundries_ki_best_practices[1]) & (
                df["Punkte"] <= var.boundries_ki_best_practices[2])) & (
                df['Kategorien'] == 'KI Best Practices'),
        ((df["Punkte"] > var.boundries_ki_best_practices[2]) & (
                df["Punkte"] <= var.boundries_ki_best_practices[3])) & (
                df['Kategorien'] == 'KI Best Practices'),

        ((df["Punkte"] > 0) & (df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[1]) & (
                df['Kategorien'] == 'Prozess zur Identifikation von KI-Einsatzfeldern')),
        ((df["Punkte"] > var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[1]) & (
                df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[2])) & (
                df['Kategorien'] == 'Prozess zur Identifikation von KI-Einsatzfeldern'),
        ((df["Punkte"] > var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[2]) & (
                df["Punkte"] <= var.boundries_prozess_zur_identifikation_von_ki_einsatzfeldern[3])) & (
                df['Kategorien'] == 'Prozess zur Identifikation von KI-Einsatzfeldern')
    ]

    values = [1, 2, 3,
              1, 2, 3,
              1, 2, 3,
              1, 2, 3,
              1, 2, 3,
              1, 2, 3,
              1, 2, 3,
              1, 2, 3,
              1, 2, 3,
              1, 2, 3,
              1, 2, 3,
              1, 2, 3,
              1, 2, 3,
              1, 2, 3]

    df['Stufe'] = np.select(conditions, values)
    df = df.filter(['Kategorien', 'Stufe'], axis=1)
    return df


def transform_to_dimension_level_df(df):
    df = df.groupby('Gestaltungsdimension').sum()
    df = df.reset_index().rename({'Punkte': 'Punkte Pro Dimension'}, axis=1)
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

        ((df["Punkte Pro Dimension"] > 0) & (df["Punkte Pro Dimension"] <= var.upper_bound_data_level1) & (
                df['Gestaltungsdimension'] == 'Daten')),
        ((df["Punkte Pro Dimension"] > var.upper_bound_data_level1) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_data_level2)) & (
                df['Gestaltungsdimension'] == 'Daten'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_data_level2) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_data_level3)) & (
                df['Gestaltungsdimension'] == 'Daten'),

        ((df["Punkte Pro Dimension"] > 0) & (df["Punkte Pro Dimension"] <= var.upper_bound_processes_level1) & (
                df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI')),
        ((df["Punkte Pro Dimension"] > var.upper_bound_processes_level1) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_processes_level2)) & (
                df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_processes_level2) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_processes_level3)) & (
                df['Gestaltungsdimension'] == 'Prozesse im Bezug auf KI'),

        ((df["Punkte Pro Dimension"] > 0) & (df["Punkte Pro Dimension"] <= var.upper_bound_orga_level1) & (
                df['Gestaltungsdimension'] == 'Organisation und Expertise')),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level1) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_orga_level2)) & (
                df['Gestaltungsdimension'] == 'Organisation und Expertise'),
        ((df["Punkte Pro Dimension"] > var.upper_bound_orga_level2) & (
                df["Punkte Pro Dimension"] <= var.upper_bound_orga_level3)) & (
                df['Gestaltungsdimension'] == 'Organisation und Expertise')
    ]

    values = [1, 2, 3,
              1, 2, 3,
              1, 2, 3,
              1, 2, 3]

    df['Stufe'] = np.select(conditions, values)
    return df


def transform_to_dimension_drilldown(main_df, questions_points_dic, cat_points_dic, dimension):
    df_kat = main_df[main_df['Gestaltungsdimension'] == dimension]
    df_kat = df_kat.filter(['Frage', 'Punkte'], axis=1)
    col_punkte_kat = df_kat['Punkte'].tolist()

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
    df_kat = df_kat.filter(['Frage', 'Punkte'], axis=1)
    col_frage_punkte = df_kat['Punkte'].tolist()
    return col_frage_punkte


# def create_text(col_frage_punkte: [], kategorie : rtm.Text_Kategorie):
#     text = ""
#     i = 0
#     for x in kategorie.statements:
#         if col_frage_punkte[i] >= 2:
#             text += (x.get_text(2))
#         i += 1
#     return text


def get_category_points(category_name: CategoryName):
    return data_drilldown_df.loc[data_drilldown_df.Kategorien == category_name.value, 'Stufe'].tolist()[0]


file = "form_results/results.xlsx"

# # --- dataframes and spidermap for dimension-Level-representation
#if not exists(file):
    # st.title(":bar_chart: Ergebnisse KI Reifegradermittlung")
    # st.markdown(textbausteine.intro_ohne_file)

df = pd.read_excel(file)

# number_Participants = len(df.index)
number_Participants = 1

df = clean(df)
# df = filter_with_password(df)


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


# --- points_dimension_lists for the paragraph
points_orga_list = create_List(df, 'Organisation und Expertise')
points_data_list = create_List(df, 'Daten')
points_tech_list = create_List(df, 'Vision, Strategie und Expertise')
points_tech_list = create_List(df, 'Technologie')
points_processes_list = create_List(df, 'Organisation und Expertise')
st.write('---------------------')
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

# Binary
print(rtm.binaryCategory.get_statement_result([1, 2, 3, 4, 5, 6, 7]))

# Block
statement_category_name = rtm.blockCategory.statements[0].category_name
category_points = get_category_points(statement_category_name)
print(category_points)
print(rtm.blockCategory.get_statement_result([category_points]))

