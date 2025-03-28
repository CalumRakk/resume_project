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
            logger.debug(f"Path excluded from token validation: {request.path}")
            response = self.get_response(request)
            return response

        logger.debug(
            f"Starting JWTMetadataValidationMiddleware for path: {request.path}"
        )
        jwt_auth = JWTAuthentication()
        try:
            auth_result = jwt_auth.authenticate(request)
            if auth_result:
                user, token = auth_result
                logger.info(
                    f"JWT token found for user: {user.username} on path: {request.path}"
                )
                self.validate_token_metadata(token, request)
            else:
                logger.warning(
                    f"No JWT token found in the request for path: {request.path}"
                )
        except TokenError as e:
            logger.error(f"Error in token validation: {str(e)}")
            return JsonResponse({"error": "Invalid token"}, status=401)

        response = self.get_response(request)
        logger.debug(
            f"JWTMetadataValidationMiddleware completed for path: {request.path}"
        )
        return response

    def validate_token_metadata(self, token, request):
        logger.info("Validating JWT token metadata")
        user_metadata = token.payload.get("user_metadata", {})
        stored_ip = user_metadata.get("ip_address")
        stored_user_agent = user_metadata.get("user_agent")

        current_ip = get_client_ip(request)
        current_user_agent = request.META.get("HTTP_USER_AGENT", "")

        logger.debug(f"IP stored in the token: {stored_ip}")
        logger.debug(f"User-Agent stored in the token: {stored_user_agent}")
        logger.debug(f"Current IP of the request: {current_ip}")
        logger.debug(f"Current User-Agent of the request: {current_user_agent}")

        if stored_user_agent != current_user_agent or not is_ip_in_range(
            current_ip, stored_ip
        ):
            logger.warning(
                f"Invalid token: possible unauthorized access. "
                f"Current IP: {current_ip}, Stored IP: {stored_ip}. "
                f"Current User-Agent: {current_user_agent}, Stored User-Agent: {stored_user_agent}"
            )
            raise TokenError("Invalid token: possible unauthorized access")

        logger.info("Token metadata validated successfully")
