from Type import Type


class Float32(Type):

    def __init__(self, data: float):
        self.data = data

    def is_type(self):
        return isinstance(self.data, float)

    def is_length(self):
        integer = int(self.data)
        decimal = self.data - integer
        decimal = int(decimal * 10 ** (len(list(str(decimal))) - 1))
        return integer.bit_length() + decimal.bit_length() <= 32

    def __str__(self):
        return "Float32"
