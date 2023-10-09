from Document import Document
import pprint


class DocumentCollection:
    def __init__(self, documents: list[Document]):
        self.__docs: list[Document] = documents

    def show(self):
        for e in self.__docs:
            pprint.pprint(e.get_doc_fields())

    def print_csv(self):
        print(";".join([*self.__docs[0].get_content()]))
        for e in self.__docs:
            print(e.get_csv_row())

    @classmethod
    def generate_empty(cls):
        return cls([Document({})])
