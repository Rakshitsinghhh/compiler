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

        # PRINT x
        if self.result == "PRINT":
            return f"PRINT {self.arg1}"

        # IF_FALSE t1 GOTO L1
        if self.result == "IF_FALSE":
            return (
                f"IF_FALSE {self.arg1} "
                f"GOTO {self.operator}"
            )

        # LABEL L1
        
        if self.result == "GOTO":
            return f"GOTO {self.arg1}"
        if self.result == "LABEL":
            return f"LABEL {self.arg1}"

        # x = 10
        if self.operator is None:
            return f"{self.result} = {self.arg1}"

        # t1 = x + y
        return (
            f"{self.result} = "
            f"{self.arg1} "
            f"{self.operator} "
            f"{self.arg2}"
        )

    def __repr__(self):
        return self.__str__()