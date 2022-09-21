from enum import Enum

class Text_Statement:
    def __init__(self, question, text1, text2):
        self.question = question
        self.text1 = text1
        self.text2 = text2
    def get_text(self, option):
        if option == 1: return self.text1
        else : return self.text2

class Text_Kategorie:
    def __init__(self, statements:[]):
        self.statements = statements


test_orga_kategorie = Text_Kategorie(
    [
        Text_Statement(1, 'Das Unternehmen hat ein KI-Budget festgelegt.',
                       'Es herrscht noch Unklarheit darüber, wie hoch das KI-Budget ist.'),
        Text_Statement(2, 'Das Unternehmen hat eine KI-Strategie festgelegt.',
                       'Das Unternehmen hat keine KI-Strategie festgelegt.'),
        Text_Statement(3, 'Um den Fortschritt bezüglich des Erreichens der KI-Vision zu tracken, hat das Unternehmen Indikatoren (KPIs) definiert.',
                       'Dem Unternehmen fehlen noch Indikatoren, um den Fortschritt bezüglich des Erreichens der KI-Vision zu tracken.'),
        Text_Statement(4, 'Im Unternehmen liegt eine ausformulierte KI-Vision vor. ',
                       'Das Unternehmen hat noch keine KI-Vision formuliert.'),
        Text_Statement(5, 'Innerhalb des Unternehmens herrscht Konzes darüber, welchen Einfluss KI auf das Umfeld, in dem das Unternehmen tätig ist, haben wird. ',
                       'Innerhalb des Unternehmens herrscht Unklarheit darüber, welchen Einfluss KI auf das Umfeld, in dem das Unternehmen tätig ist, haben wird. '),
        Text_Statement(6, 'Sowohl Management als auch Mitarbeiter, die in den KI-Aktivitäten involviert sind, haben das gleiche Verständnis der KI- Vision',
                       'Management und Mitarbeiter, die in den KI-Aktivitäten involviert sind, haben nicht das gleiche Verständnis der KI- Vision. '),
        Text_Statement(7, 'text13',
                       'text14')
    ]
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




