import logging
import sys

from utils.constants import DEFAULT_PERMISSION_DENIED_ERROR, DEFAULT_VALIDATION_ERROR

# init logger
logger = logging.getLogger(__name__)


class HustlersDenBaseException(Exception):
    """
    Base Level Exception for Hustlers Den
    """

    def __init__(self, message=None, status_code=None):
        logger.debug(
            "Function %s with data %s", sys._getframe().f_code.co_name, locals()
        )

        self.message = message
        self.status_code = status_code

        super().__init__(message)

    def to_dict(self):
        return {"status_code": self.status_code, "message": self.message}


class HustlersDenValidationError(HustlersDenBaseException):
    """
    Custom Validation Error Exception
    """

    def __init__(
        self,
        message=DEFAULT_VALIDATION_ERROR.message,
        status_code=DEFAULT_VALIDATION_ERROR.status_code,
    ):

        logger.debug(
            "Function %s with data %s", sys._getframe().f_code.co_name, locals()
        )

        self.message = message
        self.status_code = status_code
        super().__init__(message=message, status_code=status_code)


class HustlersPermissionDenied(HustlersDenBaseException):
    """
    Raises a 403 with default/custom error message
    401 stands for unauthenticated -> no account
    403 stands for unauthorized -> no authority due to business logic
    """

    def __init__(
        self,
        message=DEFAULT_PERMISSION_DENIED_ERROR.message,
        status_code=DEFAULT_PERMISSION_DENIED_ERROR.status_code,
    ):

        logger.debug(
            "Function %s with data %s", sys._getframe().f_code.co_name, locals()
        )

        self.message = message
        self.status_code = status_code

        super().__init__(message=message, status_code=status_code)
