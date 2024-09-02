from typing import Any
from unittest import TestCase

from src.command import MacroCommand
from src.fiel import CheckFuel, BurnFuel
from src.game_object import IUserObject
from src.game_types import Vector
from src.movement import MovableObjectAdaptor, Move


class MockUserObject(IUserObject):

    def __init__(self):
        self._properties = {}

    def get_property(self, key: str) -> Any:
        return self._properties[key]

    def set_property(self, key: str, value: str) -> None:
        self._properties[key] = value


class CommandTestCase(TestCase):

    def test_check_fuel_exception(self):
        object_with_fuel = MockUserObject()
        object_with_fuel.set_property("fuel_volume", 0)
        object_with_fuel.set_property("fuel_velocity", 1)
        check_fuel_cmd = CheckFuel(object_with_fuel)
        self.assertRaises(Exception, check_fuel_cmd.execute)

    def test_burn_fuel_success(self):
        object_with_fuel = MockUserObject()
        object_with_fuel.set_property("fuel_volume", 1)
        object_with_fuel.set_property("fuel_velocity", 1)
        check_fuel_cmd = CheckFuel(object_with_fuel)
        check_fuel_cmd.execute()
        burn_fuel_cmd = BurnFuel(object_with_fuel)
        burn_fuel_cmd.execute()
        self.assertTrue(object_with_fuel.get_property("fuel_volume") == 0)

    def test_macro_command(self):
        object_with_fuel = MockUserObject()
        object_with_fuel.set_property("fuel_volume", 1)
        object_with_fuel.set_property("fuel_velocity", 1)
        macro_commands = [
            CheckFuel(object_with_fuel),
            BurnFuel(object_with_fuel),
        ]
        macro_command = MacroCommand(macro_commands)
        macro_command.execute()
        self.assertTrue(object_with_fuel.get_property("fuel_volume") == 0)

    def test_macro_command_exception(self):
        object_with_fuel = MockUserObject()
        object_with_fuel.set_property("fuel_volume", 10)
        object_with_fuel.set_property("fuel_velocity", 100)
        macro_commands = [
            CheckFuel(object_with_fuel),
            BurnFuel(object_with_fuel),
        ]
        macro_command = MacroCommand(macro_commands)
        self.assertRaises(Exception, macro_command.execute)
        self.assertTrue(object_with_fuel.get_property("fuel_volume") == 10)

    def test_macro_command_move_exception(self):
        object_with_fuel = MockUserObject()
        object_with_fuel.set_property("fuel_volume", 10)
        object_with_fuel.set_property("fuel_velocity", 100)
        object_with_fuel.set_property("position", Vector([12.0, 5.0]))
        object_with_fuel.set_property("velocity", Vector([-7, 3]))
        movable = MovableObjectAdaptor(object_with_fuel)

        macro_commands = [
            CheckFuel(object_with_fuel),
            Move(movable),
            BurnFuel(object_with_fuel),
        ]
        macro_command = MacroCommand(macro_commands)
        self.assertRaises(Exception, macro_command.execute)
        self.assertTrue(object_with_fuel.get_property("fuel_volume") == 10)
        self.assertTrue(object_with_fuel.get_property("position") == Vector([12, 5]))

    def test_macro_command_move(self):
        object_with_fuel = MockUserObject()
        object_with_fuel.set_property("fuel_volume", 10)
        object_with_fuel.set_property("fuel_velocity", 10)
        object_with_fuel.set_property("position", Vector([12.0, 5.0]))
        object_with_fuel.set_property("velocity", Vector([-7, 3]))
        movable = MovableObjectAdaptor(object_with_fuel)

        macro_commands = [
            CheckFuel(object_with_fuel),
            Move(movable),
            BurnFuel(object_with_fuel),
        ]
        macro_command = MacroCommand(macro_commands)
        macro_command.execute()
        self.assertTrue(object_with_fuel.get_property("fuel_volume") == 0)
        self.assertTrue(object_with_fuel.get_property("position") == Vector([5, 8]))
