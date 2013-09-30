# -*- coding: utf-8 -*-

""" This module contains logic behind models

Every model inherits from ``Model`` class and it must have an ``objects`` class
variable
"""


class Manager(object):
    def create(self, model):
        raise NotImplementedError()

    def update(self, model):
        raise NotImplementedError()

    def filter(self):
        raise NotImplementedError()

    def delete(self, model):
        raise NotImplementedError()


class ModelMetaclass(type):

    def __new__(cls, name, bases, dct):
        Manager = dct['objects']
        manager = Manager()
        dct['objects'] = manager
        model = super(ModelMetaclass, cls).__new__(cls, name, bases, dct)
        manager.model = model
        return model


class Model(object):
    __metaclass__ = ModelMetaclass

    objects = Manager

    def get_uid(self):
        """ This method must return unique ID for this object in set of all
        objects of this class.
        This by default is used to detect if the object is retrievd from
        server or is a new object. Thad behaviour might be changed in
        ``is_created`` method

        Default is ``id`` but it might be changed here.
        """
        return self.id
    uid = property(get_uid)

    def is_created(self):
        """ Returns ``True if model was created and has not yet been saved to
        server.

        By default it checks if ``uid`` is ``None``.
        """
        return self.uid is None
    created = property(is_created)

    def save(self):
        if self.created:
            self.objects.create(self)
        else:
            self.objects.update(self)

    def delete(self):
        self.objects.delete(self)


class Adapter(object):

    def to_object(self, data):
        raise NotImplementedError()

    def from_object(self, obj):
        raise NotImplementedError()


class AdaptableManager(Manager):

    adapter = Adapter()

    def create(self, model):
        self.adapter.from_object(model)

    def update(self, model):
        self.adapter.from_object(model)

    def filter(self):
        return map(self.adapter.to_object, self.fetch())

    def delete(self, model):
        raise NotImplementedError()