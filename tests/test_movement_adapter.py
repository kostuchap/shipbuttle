from typing import Any
from unittest import TestCase
from unittest.mock import Mock

from src.ioc import IoC
from src.movement import IMovable, MovableObjectAdaptor, Vector, IUserObject, Move

from src.turn import Turn, TurnableObjectAdaptor, ITurnable

from src.adapter import AdapterMetaClass


class MockUserObject(IUserObject):

    def __init__(self):
        self._properties = {}

    def get_property(self, key: str) -> Any:
        return self._properties[key]

    def set_property(self, key: str, value: str) -> None:
        self._properties[key] = value


class MoveTestCase(TestCase):

    def test_move_successful(self):
        obj = MockUserObject()

        obj.set_property("position", Vector([12.0, 5.0]))
        obj.set_property("velocity", Vector([-7, 3]))

        IoC.resolve(
            'IoC.Register',
            'Adapter',
            AdapterMetaClass,
        ).execute()

        meta_adapter = IoC.resolve('Adapter', IMovable).execute()
        movable = meta_adapter(obj)

        movable.get_velocity()
        move = Move(movable)
        move.execute()

        self.assertTrue(obj.get_property("position") == Vector([5, 8]))

    def test_move_successful(self):
        obj = MockUserObject()

        obj.set_property("position", Vector([10.0, 10.0]))
        obj.set_property("velocity", Vector([0, 0]))

        IoC.resolve(
            'IoC.Register',
            'Adapter',
            AdapterMetaClass,
        ).execute()

        meta_adapter = IoC.resolve('Adapter', IMovable).execute()
        movable = meta_adapter(obj)

        movable.get_velocity()
        move = Move(movable)
        move.execute()

        self.assertTrue(obj.get_property("position") == Vector([10, 10]))
