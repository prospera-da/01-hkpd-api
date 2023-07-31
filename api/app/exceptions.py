from enum import Enum
from typing import Any, Dict
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from .utils.env_var import MODEL_VERSION


class ErrorMessage(str, Enum):
    REQUEST_NOT_PARSEABLE = "REQUEST_NOT_PARSEABLE"
    BAD_REQUEST = "BAD_REQUEST"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    SUCCESS = "SUCCESS"
    DATABASE_NOT_CONNECTED = "DATABASE_NOT_CONNECTED"
    UNPROCESSABLE_ENTITY = "UNPROCESSABLE_ENTITY"


METADATA = {"version": MODEL_VERSION}


async def validation_exception_handler(
    request_in: Request, exc: RequestValidationError
):
    try:
        response: Dict[str, Any] = {}
        response["message"] = ", ".join(
            [f"{x['loc'][-1]} - {x['msg']} - {x['type']}" for x in exc.errors()]
        )
        response["status"] = ErrorMessage.UNPROCESSABLE_ENTITY.value
        response["metadata"] = METADATA

        return JSONResponse(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY,
            content=response,
        )

    except Exception as exc:
        raise BaseException(
            message=f"There's an error in the validation handler - {str(exc)}"
        )


async def starlette_exception_handler(request: Request, exc: StarletteHTTPException):
    response = {
        "message": str(exc.detail),
        "status": str(exc.detail),
        "metadata": METADATA,
    }
    return JSONResponse(
        status_code=exc.status_code,
        content=response,
    )


class BaseException(Exception):
    message = ErrorMessage.INTERNAL_SERVER_ERROR.value
    status_code = 500

    def __init__(self, message=None, payload: Dict = None):
        super().__init__(message)
        self.message = message if message else self.message
        self.payload = payload or {}

    def to_dict(self) -> Dict:
        return {
            "message": self.message,
            "status": ErrorMessage.INTERNAL_SERVER_ERROR.value,
            "metadata": METADATA,
            **self.payload,
        }


class DatabaseNotConnected(BaseException):
    """Exception raised for where database is not connected
    e.g. an unexpected disconnect occurs, the data source name is not
    found"""

    message = ErrorMessage.DATABASE_NOT_CONNECTED.value
    status = 500
