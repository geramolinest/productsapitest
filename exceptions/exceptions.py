class CustomException:
    def __init__(self, status_code: int, detail: str = "", status_text: str = "", error: str = "",
                 messages: tuple[any] = ()) -> None:
        if messages is None:
            messages = []
        self.status_code: int = status_code
        self.detail: str = detail
        self.status_text: str = status_text
        self.error: str = error
        self.messages: tuple[any] = messages


class HTTPExceptionCustom(Exception):

    def __init__(self, status_code: int, detail: str = "") -> None:
        self.status_code: int = status_code
        self.detail: str = detail


class HTTPExceptionBadRequest(HTTPExceptionCustom):
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=400, detail="Bad request exception" if detail is None else detail)


class HTTPNotFoundException(HTTPExceptionCustom):
    def __init__(self, detail: str = None) -> None:
        super().__init__(status_code=404, detail="Resource not found" if detail is None else detail)


class CustomValidationException(HTTPExceptionCustom):
    def __init__(self, errors: list) -> None:
        super().__init__(status_code=400, detail='Field validation error')
        self.status_text = "BAD_REQUEST"
        self.errors: list = errors if errors is not None else []
