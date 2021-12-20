

from multimethod import multimeta


class Result(metaclass=multimeta):
    """
    封装的返回函数
    """

    def __init__(self):
        self.result = {
            "message": "",
            "data": None,
            "state": 1,
        }

    def renderError(self, i: int, msg: str):
        self.result["message"] = msg
        self.result["state"] = i
        return self.Ret(self.result)

    def renderError(self, msg: str):
        self.result["message"] = msg
        return self.Ret(self.result)

    def renderError(self):
        self.result["message"] = "404 Error"
        return self.Ret(self.result)

    def renderSuccess(self, res: dict):
        self.result["data"] = res
        self.result["state"] = 0
        return self.Ret(self.result)

    def renderSuccess(self, res: list):
        self.result["data"] = res
        self.result["state"] = 0
        return self.Ret(self.result)

    def renderSuccess(self, res: str):
        self.result["data"] = res
        self.result["state"] = 0
        return self.Ret(self.result)

    def renderSuccess(self):
        self.result["state"] = 0
        return self.Ret(self.result)

    def Ret(self, res):
        return res
