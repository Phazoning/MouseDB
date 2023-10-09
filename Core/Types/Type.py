class Type:

    def is_type(self):
        return True

    def is_length(self):
        return True

    def is_correct(self):
        return self.is_type() and self.is_length()

