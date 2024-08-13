from typing import Any
from unittest import TestCase
from unittest.mock import Mock

from src.movement import IMovable, MovableObjectAdaptor, Turn, TurnableObjectAdaptor, Vector, IUserObject, Move, \
    ITurnable


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

        movable = MovableObjectAdaptor(obj)
        move = Move(movable)
        move.execute()

        self.assertTrue(obj.get_property("position") == Vector([5, 8]))

    def test_move_get_position_exception(self):
        mock_movable = Mock(spec_set=IMovable)

        mock_movable.get_position.side_effect = NotImplementedError()
        self.assertRaises(Exception, Move(MovableObjectAdaptor(mock_movable)).execute)

    def test_move_get_velocity_exception(self):
        mock_movable = Mock(spec_set=IMovable)

        mock_movable.get_velocity.side_effect = NotImplementedError()
        self.assertRaises(Exception, Move(MovableObjectAdaptor(mock_movable)).execute)

    def test_move_set_position_exception(self):
        mock_movable = Mock(spec_set=IMovable)

        mock_movable.set_position.side_effect = NotImplementedError()
        self.assertRaises(Exception, Move(MovableObjectAdaptor(mock_movable)).execute)


class TurnTestCase(TestCase):

    def test_turn_successful(self):
        obj = MockUserObject()
        obj.set_property("direction", 0)
        obj.set_property("directions_number", 100)
        obj.set_property("angular_velocity", 150)

        turnable = TurnableObjectAdaptor(obj)
        turn = Turn(turnable)
        turn.execute()

        self.assertTrue(obj.get_property("direction") == 50)

    def test_turn_zero_successful(self):
        obj = MockUserObject()
        obj.set_property("direction", 0)
        obj.set_property("directions_number", 100)
        obj.set_property("angular_velocity", 100)

        turnable = TurnableObjectAdaptor(obj)
        turn = Turn(turnable)
        turn.execute()

        self.assertTrue(obj.get_property("direction") == 0)

    def test_turn_get_direction_exception(self):
        mock_turnable = Mock(spec_set=ITurnable)

        mock_turnable.get_direction.side_effect = NotImplementedError()
        self.assertRaises(Exception, Turn(TurnableObjectAdaptor(mock_turnable)).execute)

    def test_turn_get_direction_exception(self):
        mock_turnable = Mock(spec_set=ITurnable)

        mock_turnable.get_direction.side_effect = NotImplementedError()
        self.assertRaises(Exception, Turn(TurnableObjectAdaptor(mock_turnable)).execute)

    def test_turn_get_angular_velocity_exception(self):
        mock_turnable = Mock(spec_set=ITurnable)

        mock_turnable.get_angular_velocity.side_effect = NotImplementedError()
        self.assertRaises(Exception, Turn(TurnableObjectAdaptor(mock_turnable)).execute)

    def test_turn_get_directions_number_exception(self):
        mock_turnable = Mock(spec_set=ITurnable)

        mock_turnable.get_directions_number.side_effect = NotImplementedError()
        self.assertRaises(Exception, Turn(TurnableObjectAdaptor(mock_turnable)).execute)
