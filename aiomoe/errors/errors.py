class APIError(Exception):
    pass


class BadRequest(APIError):
    pass


class QuotaError(APIError):
    pass


class NotFoundError(APIError):
    pass


class MethodNotAllowed(APIError):
    pass


class ForbiddenError(APIError):
    pass


class TooManyRequestsError(APIError):
    pass


class InternalServerError(APIError):
    pass


class ServiceUnavailable(APIError):
    pass


class GatewayTimeout(APIError):
    pass
