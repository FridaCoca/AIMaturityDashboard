from typing import List

from category import CategoryName
from statement import Statement


class BlockStatement(Statement):
    def __init__(self, category_name: CategoryName, texts: List[str]):
        self.category_name = category_name
        self.texts = texts

    def get_text(self, points):
        if points <= 2:
            return self.texts[0]
        if points == 3:
            return self.texts[1]
        else:
            return self.texts[2]
