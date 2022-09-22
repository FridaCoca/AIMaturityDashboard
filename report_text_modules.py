from enum import Enum


class Statement_Version2:
    def __init__(self, question_number, text1, text2):
        self.question_number = question_number
        self.text1 = text1
        self.text2 = text2

    def get_text(self, option):
        if option == 1:
            return self.text1
        else:
            return self.text2


class Statement_Version1:
    def __init__(self, text1, text2, text3):
        self.text1 = text1
        self.text2 = text2
        self.text3 = text3

    def get_text(self, level):
        if level == 1 or level == 2:
            return self.text1
        if level == 3:
            return self.text2
        else:
            return self.text3


class Text_Kategorie:
    def __init__(self, statements):
        self.statements = statements


test_kategorie = Text_Kategorie(
    [
        Statement_Version2(1, 'Das Unternehmen hat ein KI-Budget festgelegt.',
                           'Es herrscht noch Unklarheit darüber, wie hoch das KI-Budget ist.'),
        Statement_Version2(2, 'Das Unternehmen hat eine KI-Strategie festgelegt.',
                           'Das Unternehmen hat keine KI-Strategie festgelegt.'),
        Statement_Version2(3,
                           'Um den Fortschritt bezüglich des Erreichens der KI-Vision zu tracken, hat das Unternehmen Indikatoren (KPIs) definiert.',
                           'Dem Unternehmen fehlen noch Indikatoren, um den Fortschritt bezüglich des Erreichens der KI-Vision zu tracken.'),
        Statement_Version2(4, 'Im Unternehmen liegt eine ausformulierte KI-Vision vor. ',
                           'Das Unternehmen hat noch keine KI-Vision formuliert.'),
        Statement_Version2(5,
                           'Innerhalb des Unternehmens herrscht Konzes darüber, welchen Einfluss KI auf das Umfeld, in dem das Unternehmen tätig ist, haben wird. ',
                           'Innerhalb des Unternehmens herrscht Unklarheit darüber, welchen Einfluss KI auf das Umfeld, in dem das Unternehmen tätig ist, haben wird. '),
        Statement_Version2(6,
                           'Sowohl Management als auch Mitarbeiter, die in den KI-Aktivitäten involviert sind, haben das gleiche Verständnis der KI- Vision',
                           'Management und Mitarbeiter, die in den KI-Aktivitäten involviert sind, haben nicht das gleiche Verständnis der KI- Vision. '),
        Statement_Version2(7, 'text13',
                           'text14')
    ]
)

test_data_data_driven_culture = Text_Kategorie(
    Statement_Version1(
        '1.	Es liegt kein tiefgreifendes, unternehmensweites Verständnis für das Potenzial von Daten vor.',
        '2.	Das Unternehmen beobachtet den Markt aktiv und sucht nach Wegen, um Erfahrung zu sammeln und KI-Lösungen zu implementieren.',
        '3.	Das Unternehmen entscheidet standartmäßig datenbasiert und ist motiviert auch zukünftig Prognosen und KI zu nutzen.')
)

# # --- Organisation und Expertise ---
# Orga_Vision = Text_Kategorie(
#     [
#         Text_Statement(1, 2, 'Im Unternehmen liegt eine ausformulierte KI-Vision vor.'),
#         Text_Statement(1, 1, 'Das Unternehmen hat noch keine KI-Vision formuliert'),
#         Text_Statement(2, 2, 'Innerhalb des Unternehmens herrscht Konzes darüber, welchen Einfluss KI auf das Umfeld, in dem das Unternehmen tätig ist, haben wird.'),
#         Text_Statement(2, 1, 'Innerhalb des Unternehmens herrscht Unklarheit darüber, welchen Einfluss KI auf das Umfeld, in dem das Unternehmen tätig ist, haben wird.'),
#         Text_Statement(3, 2, 'Sowohl Management als auch Mitarbeiter, die in den KI-Aktivitäten involviert sind, haben das gleiche Verständnis der KI- Vision'),
#         Text_Statement(3, 1, 'Management und Mitarbeiter, die in den KI-Aktivitäten involviert sind, haben nicht das gleiche Verständnis der KI- Vision.'),
#     ], "KI_Vision")
#
# Orga_Strategie = Text_Kategorie(
#     [
#         Text_Statement(1, 2, 'Das Unternehmen hat ein KI-Budget festgelegt.'),
#         Text_Statement(1, 1, 'Es herrscht noch Unklarheit darüber, wie hoch das KI-Budget ist.'),
#         Text_Statement(2, 2, 'Das Unternehmen hat eine KI-Strategie festgelegt.'),
#         Text_Statement(2, 1, 'Das Unternehmen hat keine KI-Strategie festgelegt.'),
#         Text_Statement(3, 2, 'Um den Fortschritt bezüglich des Erreichens der KI-Vision zu tracken, hat das Unternehmen Indikatoren (KPIs) definiert.'),
#         Text_Statement(3, 1, 'Dem Unternehmen fehlen noch Indikatoren, um den Fortschritt bezüglich des Erreichens der KI-Vision zu tracken.'),
#     ],
#     'Strategie'
# )
