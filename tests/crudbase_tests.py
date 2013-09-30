# -*- coding: utf-8 -*-

import mock
import unittest

from crudbase import Model, Manager

#  This will be our testing API
ExternalAPI = mock.MagicMock()


class TestManager(Manager):

    def create(self, model):
        ExternalAPI.create(property1=model.property1)

    def update(self, model):
        ExternalAPI.modify(property1=model.property1)

    def filter(self):
        return map(self.model, ExternalAPI.read())

    def delete(self, model):
        ExternalAPI.delete(id=model.uid)


class TestModel(Model):

    objects = TestManager

    def __init__(self, id=None):
        self.id = id

    def __eq__(self, other):
        return self.id == other.id


class ModelsLogicTestCase(unittest.TestCase):

    def setUp(self):
        ExternalAPI.reset_mock()

    def test_create(self):
        test = TestModel()
        test.property1 = "test"
        test.save()

        ExternalAPI.create.assert_called_once_with(property1="test")

    def test_read(self):
        ExternalAPI.read.return_value = range(3)
        self.assertEquals(map(TestModel, range(3)), TestModel.objects.filter())

    def test_update(self):
        test = TestModel(1)
        test.property1 = "test 2"
        test.save()

        ExternalAPI.modify.assert_called_once_with(property1="test 2")

    def test_delete(self):
        test = TestModel(1)
        test.delete()

        ExternalAPI.delete.assert_called_once_with(id=1)
