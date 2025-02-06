from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from .utils import is_ip_in_range, get_client_ip


class JWTMetadataValidationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwt_auth = JWTAuthentication()
        try:
            auth_result = jwt_auth.authenticate(request)
            if auth_result:
                user, token = auth_result
                self.validate_token_metadata(token, request)
        except TokenError as e:
            return JsonResponse({"error": "Token inválido"}, status=401)

        response = self.get_response(request)
        return response

    def validate_token_metadata(self, token, request):
        user_metadata = token.payload.get("user_metadata", {})
        stored_ip = user_metadata.get("ip_address")
        stored_user_agent = user_metadata.get("user_agent")

        current_ip = get_client_ip(request)
        current_user_agent = request.META.get("HTTP_USER_AGENT", "")

        if stored_user_agent != current_user_agent or not is_ip_in_range(
            current_ip, stored_ip
        ):
            raise TokenError("Token no válido: posible acceso no autorizado")
