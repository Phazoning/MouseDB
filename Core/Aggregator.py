from Collection import Collection
from Document import Document


class Aggregator:

    def __init__(self):
        self.docs: list[Document] = []

    def __search(self, parameters):
        docs = []
        for e in self.docs:
            if e.check_parameters(parameters):
                docs.append(e)
        self.docs = docs

    def __lookup(self, parameters: dict):
        foreign_col: Collection = parameters["from"]
        self_field: str = parameters["field"]
        foreign_field: str = parameters["foreign_field"]
        as_field: str = parameters["as"]

        for e in self.docs:
            actual_val = e.get_field(self_field)
            e.add_field(as_field, foreign_col.select({foreign_field: actual_val}))

    def __unwind(self, field):
        # TODO Unificar con la identificación de campos mediante #
        ret_docs = []
        for e in self.docs:
            for j in e.get_field(field):
                newdoc = e
                newdoc.alter_field(field, j)
                ret_docs.append(newdoc)
            self.docs.pop(0)
        self.docs = ret_docs

    def __unset(self, fields: str | list[str]):
        # TODO Unificar con la identificación de campos mediante #
        if isinstance(fields, str):
            [e.delete_field(fields) for e in self.docs]
        elif isinstance(fields, list):
            [[e.delete_field(j) for j in fields] for e in self.docs]

    def __group(self, parameters: dict):
        ret_docs = []
        sample_doc = Document({key: None for key, val in parameters.items()})
        try:
            assert("_id" in [*parameters] and "#" in [*parameters["_id"]][0])
            values = []
            for e in self.docs:
                if e.get_field(parameters["_id"][1:]) not in values:
                    values.append(e.get_field(parameters["_id"][1:]))
            values.sort()
            for e in values:
                matched_docs = [i for i in self.docs if i.get_field(parameters["_id"][1:]) == e]
                new_doc = sample_doc
                new_doc.alter_field("_id", e)

                for j in [*parameters]:
                    assert "#" in [*parameters[j].values()][0]
                    old_field = [*parameters[j].values()][0][1:]
                    assert "$" in [*parameters[j]][0]
                    operation = [*parameters[j]][0]

                    if operation == "$sum":
                        new_doc.alter_field(j, self.__group_sum(old_field))
                    elif operation == "$sort":
                        new_doc.alter_field(j, self.__group_sort(old_field))
                    elif operation == "$isort":
                        new_doc.alter_field(j, self.__group_sort(old_field, True))
                    elif operation == "$set":
                        new_doc.alter_field(j, self.__group_set(old_field))
                    elif operation == "$avg":
                        new_doc.alter_field(j, self.__group_average(old_field))

                ret_docs.append(new_doc)
                self.docs = [i for i in self.docs if i not in matched_docs]

            self.docs = ret_docs

        except AssertionError:
            return None

    def __project(self, parameters: dict):

        ret_docs: list[Document] = []

        project_doc = Document({key: None for key, val in parameters.items()})

        project_ops = {
            "$sum": self.__op_sum,
            "$avg": self.__op_average,
            "$sort": self.__op_sort,
            "$array": self.__op_make_array
        }

        for e in self.docs:
            base_doc = project_doc
            for j in base_doc.get_doc_fields():
                if base_doc.get_field(j)[1:] in e.get_doc_fields() and "#" == base_doc.get_field(j)[0]:
                    base_doc.alter_field(j, e.get_field([j][1:]))
                elif j in e.get_doc_fields() and parameters[j] != 0 and parameters[j]:
                    base_doc.alter_field(j, parameters[j])
                elif isinstance(base_doc.get_field(j), dict):
                    op, params = project_ops[[*base_doc.get_field(j)][0]], [*base_doc.get_field(j).values()][0] 

                    base_doc.alter_field(j, op(e, params))

            ret_docs.append(base_doc)

        self.docs = ret_docs

    def __group_sum(self, doc_field):
        ret = 0
        for e in self.docs:
            ret += e.get_field(doc_field)
        return ret

    def __group_sort(self, doc_field, is_reversed=False):
        values = [e.get_field(doc_field) for e in self.docs]

        return values.sort(reverse=is_reversed)

    def __group_set(self, doc_field):
        values = [j.get_field(doc_field) for j in self.docs]
        values = [j for j in values if values.count(j) == 1]

        return values

    def __group_average(self, doc_field):
        values = [e.get_field(doc_field) for e in self.docs]
        return sum(values)//len(values)

    def __op_sum(self, doc: Document, doc_field):
        values = doc.get_field(doc_field)
        ret = 0

        for e in values:
            ret += e
        return ret

    def __op_average(self, doc: Document, doc_field):
        values = doc.get_field(doc_field)
        ret = 0

        for e in values:
            ret += e
        return ret//len(values)

    def __op_sort(self, doc: Document, doc_field, is_reversed=False):
        return doc.get_field(doc_field).sort(reverse=is_reversed)

    def __op_make_array(self, doc: Document, fields):
        return [doc.get_field(e) for e in fields]

    def aggregate(self, pipelines: list[dict]):

        pipeline_ops = {
            "$search": self.__search,
            "$lookup": self.__lookup,
            "$unwind": self.__unwind,
            "$unset": self.__unset,
            "$group": self.__group,
            "$project": self.__project
        }

        for e in pipelines:
            try:
                assert isinstance(e, dict) and len(e) == 1
                pipeline_operation = pipeline_ops[[*e][0]]
                pipeline_parameters = [*e.values()][0]
                pipeline_operation(pipeline_parameters)

            except AssertionError:
                pass
