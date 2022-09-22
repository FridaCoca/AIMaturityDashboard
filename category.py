from enum import Enum
from typing import List

from statement import Statement


class CategoryName(Enum):
    DataDrivenCulture = 'Data Driven Culture'
    DataSource = 'Datenherkunft und -haltung'
    DataMonitoring = 'Datamonitoring, -governance und -policies'
    DataQuality = 'Datenqualität'
    DataLegal = 'Rechtliche Grundlagen'


class Category:
    def __init__(self, statements: List[Statement]):
        self.statements = statements

    def get_statement_result(self, points: List[int]):
        compound_statement = ""
        for i, s in enumerate(self.statements):
            current_statement_points = points[i]
            compound_statement += s.get_text(current_statement_points) + '\n'
        return compound_statement
