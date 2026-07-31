class AppException(Exception):
    """Base class for all application-level exceptions."""

    status_code: int = 500
    error_code: str = "internal_error"
    message: str = "An unexpected error occurred"

    def __init__(self, message: str | None = None, error_code: str | None = None):
        if message is not None:
            self.message = message
        if error_code is not None:
            self.error_code = error_code
        super().__init__(self.message)


class ItemNotFoundException(AppException):
    status_code = 404
    error_code = "item_not_found"
    message = "Menu item not found"


class InvalidCategoryError(AppException):
    status_code = 400
    error_code = "invalid_category"
    message = "No menu items found for the requested category"


class InvalidRequestError(AppException):
    status_code = 400
    error_code = "invalid_request"
    message = "The request is invalid"
