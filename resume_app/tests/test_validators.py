from rest_framework.exceptions import ValidationError
from django.test import TestCase
from resume_app.utils import validate_list


class ValidateListTestCase(TestCase):
    def setUp(self):
        self.validator_default = validate_list()
        self.validator_custom = validate_list(25)

    def test_validate_list_within_limit(self):
        """Prueba que la validación pasa cuando la lista está dentro del límite"""
        self.validator_default(list(range(50)))
        self.validator_custom(list(range(25)))

    def test_validate_list_exceeds_limit(self):
        """Prueba que la validación lanza error si la lista excede el límite"""
        with self.assertRaises(ValidationError):
            self.validator_default(list(range(51)))

        with self.assertRaises(ValidationError):
            self.validator_custom(list(range(26)))

    def test_validate_list_empty(self):
        """Prueba que la validación pasa con una lista vacía"""
        self.validator_default([])
        self.validator_custom([])

    def test_validate_list_non_list_type(self):
        """Prueba que la validación ignora valores que no son listas"""
        self.validator_default("string")
        self.validator_custom(123)
