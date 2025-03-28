from django.http import HttpRequest
import ipaddress
from rest_framework.exceptions import ValidationError
import json
from django.conf import settings
import re

webcomponent_regex = re.compile(r"^[a-z]+-[a-z]+(?:-[a-z]+)*$")
SCHEMA_DIR = settings.BASE_DIR / "resume_app" / "schemas"


class SchemaLoader:
    """Singleton to load and store JSON schemas in memory."""

    _schemas = {}

    @classmethod
    def load_schema(cls, filename: str):
        """Loads a schema only if it's not already in memory."""
        if filename not in cls._schemas:
            schema_path = SCHEMA_DIR / filename
            try:
                cls._schemas[filename] = json.loads(schema_path.read_text("utf-8"))
            except FileNotFoundError:
                raise FileNotFoundError(f"Schema file '{filename}' not found.")
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON schema '{filename}': {e}")
        return cls._schemas[filename]


def is_valid_webcomponent(name):
    if bool(webcomponent_regex.fullmatch(name)) is False:
        raise ValidationError(
            f"The component name {name} is not valid. It must be in lowercase, contain at least one hyphen (`-`), "
            "and must not start or end with a number or a hyphen. "
            "app-component ✅ Valid. "
            "app-name-component ✅ Valid. "
            "component123 ❌ Invalid. "
            "App-Component ❌ Invalid. "
            "singleword ❌ Invalid."
        )
    return True


def check_list_does_not_exceed_50(value):
    if not isinstance(value, list):
        raise ValidationError("The field must be a list.")

    if len(value) > 50:
        raise ValidationError("The list must have less than 50 elements.")


def is_ip_in_range(user_ip, allowed_range):
    return ipaddress.ip_address(user_ip) in ipaddress.ip_network(allowed_range)


def get_client_ip(request: "HttpRequest"):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
