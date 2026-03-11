class ApiResponse:
    def __init__(
        self, status_code: int, message: str = "Success", data = None
    ):
        self.status_code = status_code
        self.message = message
        self.data = data
        self.success = status_code < 400

    def to_dict(self):
        return {"success": self.success, "message": self.message, "data": self.data}
