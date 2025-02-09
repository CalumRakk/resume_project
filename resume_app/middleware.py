import logging
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from django.conf import settings
from .utils import is_ip_in_range, get_client_ip

logger = logging.getLogger(__name__)


class JWTMetadataValidationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        self.excluded_paths = getattr(
            settings, "EXCLUDED_PATHS_FROM_TOKEN_VALIDATION", []
        )

    def __call__(self, request):
        if any(
            request.path.startswith(public_path) for public_path in self.excluded_paths
        ):
            logger.debug(f"Ruta excluida de la validación de token: {request.path}")
            response = self.get_response(request)
            return response

        logger.debug(
            f"Iniciando middleware JWTMetadataValidationMiddleware para la ruta: {request.path}"
        )
        jwt_auth = JWTAuthentication()
        try:
            auth_result = jwt_auth.authenticate(request)
            if auth_result:
                user, token = auth_result
                logger.info(
                    f"Token JWT encontrado para el usuario: {user.username} en la ruta: {request.path}"
                )
                self.validate_token_metadata(token, request)
            else:
                logger.warning(
                    f"No se encontró un token JWT en la solicitud para la ruta: {request.path}"
                )
        except TokenError as e:
            logger.error(f"Error en la validación del token: {str(e)}")
            return JsonResponse({"error": "Token inválido"}, status=401)

        response = self.get_response(request)
        logger.debug(
            f"Middleware JWTMetadataValidationMiddleware completado para la ruta: {request.path}"
        )
        return response

    def validate_token_metadata(self, token, request):
        logger.info("Validando metadatos del token JWT")
        user_metadata = token.payload.get("user_metadata", {})
        stored_ip = user_metadata.get("ip_address")
        stored_user_agent = user_metadata.get("user_agent")

        current_ip = get_client_ip(request)
        current_user_agent = request.META.get("HTTP_USER_AGENT", "")

        logger.debug(f"IP almacenada en el token: {stored_ip}")
        logger.debug(f"User-Agent almacenado en el token: {stored_user_agent}")
        logger.debug(f"IP actual de la solicitud: {current_ip}")
        logger.debug(f"User-Agent actual de la solicitud: {current_user_agent}")

        if stored_user_agent != current_user_agent or not is_ip_in_range(
            current_ip, stored_ip
        ):
            logger.warning(
                f"Token no válido: posible acceso no autorizado. "
                f"IP actual: {current_ip}, IP almacenada: {stored_ip}. "
                f"User-Agent actual: {current_user_agent}, User-Agent almacenado: {stored_user_agent}"
            )
            raise TokenError("Token no válido: posible acceso no autorizado")

        logger.info("Metadatos del token validados exitosamente")
