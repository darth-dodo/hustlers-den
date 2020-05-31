from collections import namedtuple

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_500_INTERNAL_SERVER_ERROR,
)

HUSTLERS_DEN_ERROR_CONTAINER = namedtuple(
    "HUSTLERS_DEN_ERROR_CONTAINER", ["message", "status_code"]
)

DEFAULT_SERVER_ERROR = HUSTLERS_DEN_ERROR_CONTAINER(
    message="Something went wrong on the server side. " "Please check the logs!",
    status_code=HTTP_500_INTERNAL_SERVER_ERROR,
)

DEFAULT_VALIDATION_ERROR = HUSTLERS_DEN_ERROR_CONTAINER(
    message="Oops! Something went wrong!", status_code=HTTP_400_BAD_REQUEST
)

DEFAULT_PERMISSION_DENIED_ERROR = HUSTLERS_DEN_ERROR_CONTAINER(
    message="You are not authorized for this action", status_code=HTTP_403_FORBIDDEN
)

AUTO_GENERATED_PASSWORD_LENGTH = 30
