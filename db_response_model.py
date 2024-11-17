class ResponseModel:
    def __init__(self, success, data):
        self.success = success
        self.data = data

    def dict(self):
        return {"success": self.success, "data": self.data}
