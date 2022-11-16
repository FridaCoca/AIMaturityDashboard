# --- Variables ---

# indices for questions to assign dimension
f_q_technologie = 0
l_q_technologie = 14
f_q_data = 15
l_q_data = 34
f_q_organisation = 35
l_q_organisation = 46
f_q_prozesse = 47
l_q_prozesse = 54

number_questions_tech = 15
number_questions_data = 20
number_questions_orga = 12
number_questions_processes = 8

# upper and lower bounds to assign level
max_points_tech = number_questions_tech*4
upper_bound_tech_level1 = max_points_tech/3
upper_bound_tech_level2 = (max_points_tech/3)*2
upper_bound_tech_level3 = max_points_tech

max_points_data = number_questions_data*4
upper_bound_data_level1 = max_points_data/3
upper_bound_data_level2 = (max_points_data/3)*2
upper_bound_data_level3 = max_points_data

max_points_orga = number_questions_orga*4
upper_bound_orga_level1 = max_points_orga/3
upper_bound_orga_level2 = (max_points_orga/3)*2
upper_bound_orga_level3 = max_points_orga

max_points_precesses = number_questions_processes*4
upper_bound_processes_level1 = max_points_precesses/3
upper_bound_processes_level2 = (max_points_precesses/3)*2
upper_bound_processes_level3 = max_points_precesses

# boundries to assign level IN dimension
boundries_daten_hosting = [12, 4, 8, 12]
boundries_modelle_und_werkzeuge	= [20, 7, 14, 20]
boundries_data_warehouse_plattform = [16, 5.3, 10.6, 16]
boundries_bi_infrastruktur = [12, 4, 8, 12]

boundries_data_driven_culture = [16, 5.3, 10.6, 16]
boundries_datenherkunft_und_haltung = [12, 4, 8, 12]
boundries_datenqualität = [20, 7, 14, 20]
boundries_datamonitoring_governance_und_policies = [16, 5.3, 10.6, 16]
boundries_rechtliche_grundlagen = [16, 5.3, 10.6, 16]

boundries_ki_vision = [12, 4, 8, 12]
boundries_bi_expertise = [12, 4, 8, 12]
boundries_bestehende_ki_lösungen_im_unternehmen = [12, 4, 8, 12]
boundries_strategie = [12, 4, 8, 12]

boundries_ki_best_practices = [4, 1, 3, 4]
boundries_prozess_zur_identifikation_von_ki_einsatzfeldern = [16, 5.3, 10.6, 16]
boundries_ki_use_cases = [12, 4, 8, 12]