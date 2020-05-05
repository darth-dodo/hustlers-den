import os
import sys
import logging

from utils.hustlers_den_exceptions import HustlersDenValidationError

logger = logging.getLogger(__name__)


class BaseService:
    def __init__(self):
        """
        Superclass Base Service for Hustlers Den services
        """

        logger.debug('Func %s begins with data %s', sys._getframe().f_code.co_name, locals())

        self.service_response_data = None
        self.valid = None

        self.errors = []

    @property
    def error_message(self):
        """
        Property to stringify the error messages

        return :str:
        """
        logger.debug('Func %s begins with data %s', sys._getframe().f_code.co_name, locals())

        return ', '.join(self.errors)

    @property
    def is_valid(self):
        """
        Returns a boolean based on errors

        return :bool:
        """
        logger.debug('Func %s begins with data %s', sys._getframe().f_code.co_name, locals())

        if not self.errors:
            self.valid = True
        else:
            self.valid = False

        return self.valid

    def validate(self, raise_errors=False):
        """
        Wrapper over subclassed validate. Used to check if the validations ran
        successfully. Optionally raise an error which bubbles up to the caller

        return :bool:
        return :HustlersDenValidationError: Raise the errors in a stringify
                manner
        """
        logger.debug('Func %s begins with data %s', sys._getframe().f_code.co_name, locals())

        if not self.is_valid and raise_errors:
            raise HustlersDenValidationError(message=self.error_message)

        return self.is_valid

    def execute(self, raise_errors=False):
        """
        Wrapper for running the execute method. Needs to be called at the start
        of the subclassed method.

        Implicitly runs the validations in case the validations haven't been
        run already

        Optionally raises validation errors and "explodes" the service

        return :bool: Returns whether the execution was valid.
        """
        logger.debug('Func %s begins with data %s', sys._getframe().f_code.co_name, locals())

        if self.valid is None:
            self.validate(raise_errors)

        return self.valid
