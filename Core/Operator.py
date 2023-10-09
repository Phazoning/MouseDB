class Operator:

    def __init__(self):
        self.__content = {}

    def __get_parameters(self, parameters: dict):
        search = {}
        operations = {}
        for key, val in parameters.items():
            if "$" not in key and not isinstance(val, dict):
                search[key] = val
            elif isinstance(val, dict) and "$" not in key:
                operations[key] = val if "$" in [*val][0] else None
            elif "$" in key:
                operations[key] = val

        return search, operations

    def __search(self, parameters: dict):
        ret = True
        for e in [*parameters]:
            ret = self.__content[e] == parameters[e]
        return ret

    def __or(self, parameters: list[dict] | dict):

        assert (isinstance(parameters, dict) or
                (isinstance(parameters, list) and [e for e in parameters if isinstance(e, dict)] == parameters))

        if isinstance(parameters, dict):

            ret = False

            for e in [*parameters]:
                if "$" in e:
                    ret = True if self.__operate(e) and not ret else ret
                else:
                    ret = True if self.__search({e: parameters[e]}) and not ret else ret
            return ret

        else:
            ret = False
            for e in parameters:
                ret = True if self.__search(e) and not ret else ret
            return ret

    def __xor(self, parameters: list[dict] | dict):
        assert (isinstance(parameters, dict) or
                (isinstance(parameters, list) and [e for e in parameters if isinstance(e, dict)] == parameters))

        if isinstance(parameters, dict):

            ret = False
            trues = 0
            for e in [*parameters]:
                if "$" in e:
                    hit = self.__operate(e)
                    trues += 1 if hit else 0
                    ret = True if hit and not ret else ret
                else:
                    hit = self.__search({e: parameters[e]})
                    trues += 1 if hit else 0
                    ret = True if hit and not ret else ret
            return trues == 1

        else:
            ret = False
            trues = 0
            for e in parameters:
                hit = self.__search(e)
                trues += 1 if hit else 0
                ret = True if hit and not ret else ret
            return trues == 1

    def __and(self, parameters: list[dict]):
        ret = False
        for e in parameters:
            keys, ops = self.__get_parameters(e)
            ret = self.__search(keys) and self.__operate(ops)
        return ret

    def __xand(self, parameters: list[dict]):
        hits = 0
        for e in parameters:
            keys, ops = self.__get_parameters(e)
            hits += 1 if self.__search(keys) and self.__operate(ops) else 0
        return hits == len(parameters) or hits == 0

    def __greater_than(self, field: str, value: int | float):
        return self.__content[field] > value

    def __greater_or_equal_than(self, field: str, value: int | float):
        return self.__content[field] >= value

    def __less_than(self, field: str, value: int | float):
        return self.__content[field] < value

    def __less_or_equal_than(self, field: str, value: int | float):
        return self.__content[field] <= value

    def __not_equal(self, field: str, value: any):
        return self.__content[field] != value

    def __in(self, field: str, value: list | set):
        return self.__content[field] in value

    def __nin(self, field: str, value: list | set):
        return self.__content[field] not in value

    def __operate(self, operations: dict):
        ret = True

        simple_ops = {
            "$and": self.__and,
            "$xand": self.__xand,
            "$or": self.__or,
            "$xor": self.__xor
        }

        field_ops = {
            "$gt": self.__greater_than,
            "$gte": self.__greater_or_equal_than,
            "$lt": self.__less_than,
            "$lte": self.__less_or_equal_than,
            "$neq": self.__not_equal,
            "$in": self.__in,
            "$nin": self.__nin
        }

        for e in [*operations]:

            if "$" in e:
                ret = simple_ops[e](operations[e])

            elif "$" not in e and isinstance(operations[e], dict):
                ret = field_ops[[*operations[e]][0]](e, operations[e][[*operations[e]][0]])

            elif "$" not in e and [*operations[e]][0] == "$and":
                ret = self.__and([{e: j} for j in operations[e][[*operations[e]][0]]])

            else:
                ret = False

        return ret

    def check_parameters(self, params: dict):
        search, ops = self.__get_parameters(params)
        return self.__search(search) and self.__operate(ops)

