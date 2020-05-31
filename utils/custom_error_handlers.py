import logging

from django.http.response import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from den.settings.base import get_env_variable
from utils.constants import DEFAULT_SERVER_ERROR
from utils.hustlers_den_exceptions import (
    HustlersDenBaseException,
    HustlersDenValidationError,
    HustlersPermissionDenied,
)

logger = logging.getLogger(__name__)


class HustlersDenExceptionMiddleware(MiddlewareMixin):
    """
    Custom Middleware used to process Custom Exceptions
    """

    def process_exception(self, request, exception):
        """
        Catches errors which are bubbled up application wide
        Custom middleware used to log, sanitize and mask errors
        Pass the exception to relevant exception handlers before returning the response

        :param request: request object
        :param exception: Exception object
        :return: JsonResponse with specific status code
        """

        logger.debug("Request: {0} | Exception: {1}".format(request, exception))

        response_data = dict()
        response_data["message"] = DEFAULT_SERVER_ERROR.message
        status_code = DEFAULT_SERVER_ERROR.status_code

        # custom processing only for errors subclassed from BaseException
        if isinstance(exception, HustlersDenBaseException):

            if isinstance(
                exception, (HustlersDenValidationError, HustlersPermissionDenied)
            ):
                response_data["message"] = exception.message
                status_code = exception.status_code
                return JsonResponse(response_data, status=status_code)

        # process response if not captured by custom error handlers
        # return default message for non dev envs
        if get_env_variable("DEBUG_MODE"):
            return
        else:
            return JsonResponse(response_data, status=status_code)
