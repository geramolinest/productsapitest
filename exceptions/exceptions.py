from fastapi import HTTPException


class BadRequestException(HTTPException):
    def __init__(self, status_code: int, status_text: str = 'BAD_REQUEST', detail: str = "") -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.status_text = status_text

