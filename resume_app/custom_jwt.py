import logging
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .utils import get_client_ip

logger = logging.getLogger(__name__)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(self, user):
        logger.info(
            f"Iniciando generación de token JWT para el usuario: {user.username}"
        )
        refresh = super().get_token(user)
        request = self.context["request"]

        client_ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")

        logger.debug(f"IP del cliente: {client_ip}")
        logger.debug(f"User-Agent del cliente: {user_agent}")

        # Agregar metadatos al token
        refresh["user_metadata"] = {
            "ip_address": client_ip,
            "user_agent": user_agent,
        }

        logger.info(f"Token JWT generado exitosamente para el usuario: {user.username}")
        logger.debug(f"Metadatos del token: {refresh['user_metadata']}")
        return refresh
