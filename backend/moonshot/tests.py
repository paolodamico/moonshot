# -*- coding: utf-8 -*-

from django.test import TestCase
from rest_framework import status  # noqa: F401
from rest_framework.test import APITestCase


class MoonshotTestCase:
    def validate_close_date(self, date1, date2, tolerance=1.5):
        """
        Returns a :bool of whether two dates are close to each other,
        up to the tolerance (in seconds)
        """
        if abs((date2 - date1).total_seconds()) < tolerance:
            return True
        return False


class MoonshotUnitTestCase(TestCase, MoonshotTestCase):
    pass


class MoonshotFunctionalTestCase(APITestCase, MoonshotTestCase):
    pass
