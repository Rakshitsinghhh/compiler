class TACInstruction:

    def __init__(
        self,
        result,
        arg1,
        operator=None,
        arg2=None
    ):
        self.result = result
        self.arg1 = arg1
        self.operator = operator
        self.arg2 = arg2

    def __str__(self):

        if self.result == "PRINT":
            return f"PRINT {self.arg1}"

        if self.result == "ARG":
            return f"ARG {self.arg1}"

        if self.result == "IF_FALSE":
            return (
                f"IF_FALSE {self.arg1} "
                f"GOTO {self.operator}"
            )

        if self.result == "GOTO":
            return f"GOTO {self.arg1}"

        if self.result == "LABEL":
            return f"LABEL {self.arg1}:"

        if self.result == "FUNC":
            if self.operator:
                params = ", ".join(str(p) for p in self.operator)
                return f"FUNC {self.arg1}({params})"
            return f"FUNC {self.arg1}"

        if self.result == "END_FUNC":
            return f"END_FUNC {self.arg1}"

        if self.result == "RETURN":
            return f"RETURN {self.arg1}"

        if self.result == "CALL":
            return (
                f"{self.arg2} = "
                f"CALL {self.arg1} "
                f"{self.operator}"
            )

        if self.operator is None:
            return f"{self.result} = {self.arg1}"

        return (
            f"{self.result} = "
            f"{self.arg1} "
            f"{self.operator} "
            f"{self.arg2}"
        )

    def __repr__(self):
        return self.__str__()
