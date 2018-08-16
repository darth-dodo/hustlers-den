from django.core.exceptions import PermissionDenied
from rest_framework_jwt.settings import api_settings

# binding.pry equivalent
# import code; code.interact(local=locals())


def get_hustler_data(hustler_object):
    """
    Serializes a Hustler object for JSON
    :param hustler_object:  Hustler object
    :return: dict
    """
    
    from hustlers.api.serializers import HustlerSerializer
    serialized_hustler_data = HustlerSerializer(hustler_object).data
    return serialized_hustler_data


def jwt_response_payload_handler(token=None, user=None, request=None):
    """
    Custom JWT payload creator
    
    /auth/login/ will redirects to this endpoint
    User auth using tokens or user object wrapper around vanilla auth/login
    
    :param token: JWT token
    :param user: User object
    :param request: Request object
    :return: dict
    """

    if hasattr(user, 'hustler'):
        if user.is_active is False:
            raise PermissionDenied('Hustler is inactive')
    else:
        raise PermissionDenied('Hustler does not exist!')

    hustler_data = get_hustler_data(user.hustler)

    if token is None:
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

    return_data = {
        'auth_token': token,
        'hustler_data': hustler_data
    }

    return return_data
