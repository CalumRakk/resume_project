from django.http import HttpRequest
import ipaddress
from rest_framework.exceptions import ValidationError


def validate_list(value, max_length=50):
    if isinstance(value, list) and len(value) > max_length:
        raise ValidationError("La lista no puede contener más de 100 elementos.")


def is_ip_in_range(user_ip, allowed_range):
    return ipaddress.ip_address(user_ip) in ipaddress.ip_network(allowed_range)


def get_client_ip(request: "HttpRequest"):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
