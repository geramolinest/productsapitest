from pydantic import BaseModel
from typing import Optional


class BaseResponse(BaseModel):
    message: Optional[str] = ""
    status_code: Optional[int] = 0
    status_code_text: Optional[str] = ""
    data: dict | list


class OkResponse(BaseResponse):
    def __init__(self, data: dict | list) -> None:
        super().__init__(data=data)
        self.message: str = "Operation completed successfully"
        self.status_code: int = 200
        self.status_code_text: str = "OK_RESPONSE"


class CreatedResponse(BaseResponse):
    def __init__(self, data: dict | list) -> None:
        super().__init__(data=data)
        self.message: str = "Item created successfully"
        self.status_code: int = 201
        self.status_code_text: str = "CREATED_RESPONSE"


