from django.http import HttpRequest
import ipaddress
from rest_framework.exceptions import ValidationError
import json
from django.conf import settings

SCHEMA_DIR = settings.BASE_DIR / "resume_app" / "schemas"


class SchemaLoader:
    """Singleton para cargar y almacenar los esquemas JSON en memoria."""

    _schemas = {}

    @classmethod
    def load_schema(cls, filename: str):
        """Carga un esquema solo si aún no está en memoria."""
        if filename not in cls._schemas:
            schema_path = SCHEMA_DIR / filename
            try:
                cls._schemas[filename] = json.load(schema_path.read_text("utf-8"))
            except FileNotFoundError:
                raise FileNotFoundError(f"Schema file '{filename}' not found.")
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON schema '{filename}': {e}")
        return cls._schemas[filename]


def check_list_does_not_exceed_50(value):
    if not isinstance(value, list):
        raise ValidationError("El campo debe ser una lista.")

    if len(value) > 50:
        raise ValidationError("La lista debe tener menos de 50 elementos.")


def is_ip_in_range(user_ip, allowed_range):
    return ipaddress.ip_address(user_ip) in ipaddress.ip_network(allowed_range)


def get_client_ip(request: "HttpRequest"):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
