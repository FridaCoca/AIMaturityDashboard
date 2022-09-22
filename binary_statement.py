from statement import Statement


class BinaryStatement(Statement):
    def __init__(self, text1: str, text2: str):
        self.text1 = text1
        self.text2 = text2

    def get_text(self, points):
        if points <= 3:
            return self.text1
        else:
            return self.text2
