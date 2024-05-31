from fastapi import status


class PayrollException(Exception):
    def __init__(self, msg: str, **kwargs):
        self.msg = msg
        super().__init__(msg)


class UnauthorizedError(PayrollException):
    status_code = status.HTTP_401_UNAUTHORIZED


class ForbiddenError(PayrollException):
    status_code = status.HTTP_403_FORBIDDEN


class InvalidConfigurationError(PayrollException):
    status_code = status.HTTP_400_BAD_REQUEST
