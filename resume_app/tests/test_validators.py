from rest_framework.exceptions import ValidationError
from django.test import TestCase
from resume_app.utils import check_list_does_not_exceed_50


class ValidateListTestCase(TestCase):
    def test_validate_list_within_limit(self):
        """Prueba que la validación pasa cuando la lista está dentro del límite"""
        check_list_does_not_exceed_50(list(range(50)))

    def test_validate_list_exceeds_limit(self):
        """Prueba que la validación lanza error si la lista excede el límite"""
        with self.assertRaises(ValidationError):
            check_list_does_not_exceed_50(list(range(51)))

    def test_validate_list_empty(self):
        """Prueba que la validación pasa con una lista vacía"""
        check_list_does_not_exceed_50([])

    def test_validate_list_non_list_type(self):
        """Prueba que la validación genera error a valores que no son listas"""
        with self.assertRaises(ValidationError):
            check_list_does_not_exceed_50("not a list")

        with self.assertRaises(ValidationError):
            check_list_does_not_exceed_50(123)

        with self.assertRaises(ValidationError):
            check_list_does_not_exceed_50({"key": "value"})
