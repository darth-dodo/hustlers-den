# third party imports

# django imports
from django.utils.deprecation import MiddlewareMixin
from django.http.response import JsonResponse
from rest_framework.status import  HTTP_500_INTERNAL_SERVER_ERROR

# project level imports

# app level imports
from utils.hustlers_den_exceptions import HustlersDenBaseException, HustlersDenValidationError


class HustlersDenExceptionMiddleware(MiddlewareMixin):
    """
    Custom Middleware used to process Custom Exceptions
    """

    def process_exception(self, request, exception):
        """

        :param request: request object
        :param exception: Exception object
        :return: JsonResponse with specific status code
        """

        response_data = dict()
        response_data['message'] = None
        status_code = HTTP_500_INTERNAL_SERVER_ERROR

        # custom processing only for errors subclassed from BaseException
        if isinstance(exception, HustlersDenBaseException):

            if isinstance(exception, HustlersDenValidationError):
                response_data['message'] = exception.message
                status_code = exception.status_code

        return JsonResponse(response_data, status=status_code)

