from typing import Type

from pydantic import BaseModel

from ..errors import (
    BadRequest,
    ForbiddenError,
    GatewayTimeout,
    InternalServerError,
    MethodNotAllowed,
    NotFoundError,
    QuotaError,
    ServiceUnavailable,
    TooManyRequestsError,
)

errors = {
    400: BadRequest,
    402: QuotaError,
    403: ForbiddenError,
    404: NotFoundError,
    405: MethodNotAllowed,
    429: TooManyRequestsError,
    500: InternalServerError,
    503: ServiceUnavailable,
    504: GatewayTimeout,
}


async def check_response(status, response: dict, datatype: Type[BaseModel]):
    if status == 200:
        return datatype(**response)
    exception = errors[status]
    raise exception(response["error"])
