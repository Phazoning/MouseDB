from Type import Type


class String(Type):

    def __init__(self, data: str):
        self.data = data

    def is_type(self):
        return isinstance(self.data, str)

    def __str__(self):
        return "String"
