from Type import Type


class Boolean(Type):

    def __init__(self, data):
        self.data = data

    def is_type(self):
        return isinstance(self.data, bool)

    def __str__(self):
        return "Bool"
