from enum import Enum

class Text_Statement:
    def __init__(self, question, level, text):
        self.question = question
        self.level = level
        self.text = text


class Text_Dimension:
    def __init__(self, statements: [], category: str):
        self.statements = statements
        self.category = category

# --- Organisation und Expertise ---
# --- KI-Vision ---
Orga = Text_Dimension(
    [
        Text_Statement(1, 2, 'Im Unternehmen liegt eine ausformulierte KI-Vision vor.'),
        Text_Statement(1, 1, 'Das Unternehmen hat noch keine KI-Vision formuliert'),
        Text_Statement(2, 2, 'Innerhalb des Unternehmens herrscht Konzes darüber, welchen Einfluss KI auf das Umfeld, in dem das Unternehmen tätig ist, haben wird.'),
        Text_Statement(2, 1, 'Innerhalb des Unternehmens herrscht Unklarheit darüber, welchen Einfluss KI auf das Umfeld, in dem das Unternehmen tätig ist, haben wird.'),
        Text_Statement(3, 2, 'Sowohl Management als auch Mitarbeiter, die in den KI-Aktivitäten involviert sind, haben das gleiche Verständnis der KI- Vision'),
        Text_Statement(3, 1, 'Management und Mitarbeiter, die in den KI-Aktivitäten involviert sind, haben nicht das gleiche Verständnis der KI- Vision.'),
    ], "KI_Vision")
