from Core.Operator import Operator
from pickle import load as frombin, dump as tobin
from os import path


class Document(Operator):

    def __init__(self, doc: dict):
        super().__init__()
        self.__content = doc

    def get_field(self, field):
        ret = self.__content
        if "." in field:
            for e in field.split("."):
                try:
                    assert isinstance(ret, dict) or isinstance(ret, Document)
                    ret = ret.get_field(e) if isinstance(ret, Document) else ret[e]
                except AssertionError:
                    return ret
        else:
            ret = ret[field]
        return ret

    def get_doc_fields(self):
        return [*self.__content]

    def alter_field(self, field, value):
        self.__content[field] = value

    def delete_field(self, field):
        del self.__content[field]

    def add_field(self, field, value):
        self.__content[field] = value

    def get_content(self):
        return self.__content

    def get_csv_row(self):
        return ";".join([str(e) for e in [*self.content.values()]])

    def serialize_to_file(self, filepath=""):
        with open(path.join(filepath, f"{self.content['_id']}.mouse"), "wb") as docfile:
            tobin(self, docfile)

    @classmethod
    def load_from_file(cls, file):
        with open(file, "rb") as docfile:
            ret = frombin(docfile)

        return ret
