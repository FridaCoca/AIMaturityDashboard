from binary_statement import BinaryStatement
from block_statement import BlockStatement
from category import Category, CategoryName

binaryCategory = Category(
    [
        BinaryStatement(
            'Das Unternehmen hat ein KI-Budget festgelegt.',
            'Es herrscht noch Unklarheit darüber, wie hoch das KI-Budget ist.'),
        BinaryStatement(
            'Das Unternehmen hat eine KI-Strategie festgelegt.',
            'Das Unternehmen hat keine KI-Strategie festgelegt.'),
        BinaryStatement(
            'Um den Fortschritt bezüglich des Erreichens der KI-Vision zu tracken, hat das Unternehmen Indikatoren (KPIs) definiert.',
            'Dem Unternehmen fehlen noch Indikatoren, um den Fortschritt bezüglich des Erreichens der KI-Vision zu tracken.'),
        BinaryStatement(
            'Im Unternehmen liegt eine ausformulierte KI-Vision vor. ',
            'Das Unternehmen hat noch keine KI-Vision formuliert.'),
        BinaryStatement(
            'Innerhalb des Unternehmens herrscht Konzes darüber, welchen Einfluss KI auf das Umfeld, in dem das Unternehmen tätig ist, haben wird. ',
            'Innerhalb des Unternehmens herrscht Unklarheit darüber, welchen Einfluss KI auf das Umfeld, in dem das Unternehmen tätig ist, haben wird. '),
        BinaryStatement(
            'Sowohl Management als auch Mitarbeiter, die in den KI-Aktivitäten involviert sind, haben das gleiche Verständnis der KI- Vision',
            'Management und Mitarbeiter, die in den KI-Aktivitäten involviert sind, haben nicht das gleiche Verständnis der KI- Vision. '),
        BinaryStatement(
            'text13', 'text14')
    ]
)

blockCategory = Category([
    BlockStatement(
        CategoryName.DataLegal,
        [
            '1.	Es liegt kein tiefgreifendes, unternehmensweites Verständnis für das Potenzial von Daten vor.',
            '2.	Das Unternehmen beobachtet den Markt aktiv und sucht nach Wegen, um Erfahrung zu sammeln und KI-Lösungen zu implementieren.',
            '3.	Das Unternehmen entscheidet standartmäßig datenbasiert und ist motiviert auch zukünftig Prognosen und KI zu nutzen.'
        ])
])

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
