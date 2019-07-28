# system level imports
import os
import sys
import logging

# django imports
from utils.constants import DEFAULT_VALIDATION_ERROR

# project level imports
# app level imports

# init logger
logger = logging.getLogger(__name__)


class HustlersDenBaseException(Exception):
    """
    Base Level Exception for Hustlers Den
    """

    def __init__(self, message=None, status_code=None):
        logger.debug('Function %s with data %s', sys._getframe().f_code.co_name, locals())

        super().__init__(message)

        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {'status_code': self.status_code, 'message': self.message}


class HustlersDenValidationError(HustlersDenBaseException):
    """
    Custom Validation Error Exception
    """

    def __init__(self, message=DEFAULT_VALIDATION_ERROR.get('message'),
                 status_code=DEFAULT_VALIDATION_ERROR.get('status_code')):
        self.message = message
        self.status_code = status_code
        super(HustlersDenValidationError, self).__init__(message=message, status_code=status_code)
