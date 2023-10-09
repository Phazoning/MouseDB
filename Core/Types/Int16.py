from Type import Type


class Int16 (Type):

    def __init__(self, data: int):
        self.data = data

    def is_type(self):
        return isinstance(self.data, int)

    def is_length(self):
        return self.data.bit_length() <= 16

    def __str__(self):
        return "Int16"
