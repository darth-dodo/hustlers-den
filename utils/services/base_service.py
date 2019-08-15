import os
import sys
import logging

from utils.hustlers_den_exceptions import HustlersDenValidationError

logger = logging.getLogger(__name__)


class BaseService:
    """
    Superclass Base Service for Hustlers Den services
    """

    def __init__(self):
        logger.debug('Func %s begins with data %s', sys._getframe().f_code.co_name, locals())

        self.service_response_data = None
        self.valid = None

        self.errors = []

    @property
    def error_message(self):
        """
        """
        return ', '.join(self.errors)

    @property
    def is_valid(self):
        """
        """
        if not self.errors:
            self.valid = True
        else:
            self.valid = False

        return self.valid

    def validate(self, raise_errors=False):
        """
        """
        if not raise_errors:
            return self.is_valid

        if not self.is_valid:
            raise HustlersDenValidationError(message=self.error_message)

    def execute(self, raise_errors=False):
        """
        """
        if self.valid is None:
            self.validate(raise_errors)
