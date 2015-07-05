from django.db import models
from django.test import TestCase

from .fields import JSONPGPField


class TestModel(models.Model):
    secure_json = JSONPGPField()


class JSONPGPFieldTest(TestCase):

    def test_nothing(self):
        instance = TestModel.objects.create()
        self.assertIsInstance(instance, TestModel)
