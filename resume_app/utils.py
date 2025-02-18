from django.http import HttpRequest
import ipaddress
from rest_framework.exceptions import ValidationError


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
