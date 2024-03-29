from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from traceback import print_exception
from fastapi.exceptions import RequestValidationError

from exceptions import exceptions as ex
from schemas import schemas


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except ex.HTTPExceptionCustom as eh:
            status_text_local: str = ""

            if eh.status_code == 400:
                status_text_local = "BAD_REQUEST"
            elif eh.status_code == 404:
                status_text_local = "NOT_FOUND"
            else:
                status_text_local = "UNKNOWN_EXCEPTION"

            return JSONResponse(
                status_code=eh.status_code,
                content=ex.CustomException(status_code=eh.status_code, detail=eh.detail,
                                           status_text=status_text_local, error=eh.__class__.__name__,
                                           messages=eh.args).__dict__
            )
        except RequestValidationError as e:
            print_exception(e)
            return JSONResponse(
                status_code=400,
                content={'error': 'Error en entity'}
            )
        except Exception as e:
            print_exception(e)
            return JSONResponse(
                status_code=500,
                content=ex.CustomException(status_code=500, detail="Internal Server Error",
                                           status_text="INTERNAL_SERVER_ERROR", error=e.__class__.__name__,
                                           messages=e.args).__dict__

            )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    custom_errors: list[dict] = []

    for e in exc.errors():
        error_dict: schemas.ValidationErrorSchema = schemas.ValidationErrorSchema(field=e['loc'][1], error=e['msg'])
        custom_errors.append(error_dict.__dict__)

    return JSONResponse(status_code=400, content=ex.CustomValidationException(custom_errors).__dict__)
