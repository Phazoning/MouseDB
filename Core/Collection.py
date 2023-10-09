from Document import Document
import os
from Aggregator import Aggregator


class Collection(Aggregator):

    def __init__(self, folderpath):
        super().__init__()
        documents = [os.path.join(folderpath, e) for e in os.listdir(folderpath)]

    def select(self, parameters):
        ret_docs = []
        for e in self.documents:
            doc: Document = Document.load_from_file(e)
            if doc.check_parameters(parameters):
                ret_docs.append(e)
        return ret_docs