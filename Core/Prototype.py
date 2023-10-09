from Core.Types.Int8 import Int8 as I8
from Core.Types.Int16 import Int16 as I16
from Core.Types.Int32 import Int32 as I32
from Core.Types.Int64 import Int64 as I64
from Core.Types.Float8 import Float8 as Fl8
from Core.Types.Float16 import Float16 as Fl16
from Core.Types.Float32 import Float32 as Fl32
from Core.Types.Float64 import Float64 as Fl64
from Core.Types.Boolean import Boolean as Bool
from Core.Types.String import String as Str
from Core.Document import Document
from pickle import dump as to_bin, load as from_bin
from os import path


class Prototype:

    def __init__(self, type_ref: dict[str, I8 | I16 | I32 | I64 | Fl8 | Fl16 | Fl32 | Fl64 | Bool | Str]):
        self.ref = type_ref

    def document_follows(self, doc: Document):
        ret = True

        for e in [*doc.get_content()]:
            dataclass = self.ref[e](doc.get_field(e))

            ret = dataclass.is_correct()

        return ret

    def serialize(self, folder_path: str):
        to_bin(self, open(path.join(folder_path, ".prototype"), "wb+"))

    @classmethod
    def deserialize(cls, folder_path: str):
        return from_bin(open(path.join(folder_path, ".prototype"), "wb+"))
