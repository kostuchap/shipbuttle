from typing import Any
from unittest import TestCase

from src.command import MacroCommand
from src.fiel import CheckFuel, BurnFuel
from src.game_object import IUserObject
from src.ioc import IoC, Scope


class MockUserObject(IUserObject):

    def __init__(self):
        self._properties = {}

    def get_property(self, key: str) -> Any:
        return self._properties[key]

    def set_property(self, key: str, value: str) -> None:
        self._properties[key] = value


class IoCTest(TestCase):

    def test_ios(self):
        # scope = Scope()
        IoC.resolve(
            'IoC.Register',
            'MacroCommand',
            MacroCommand,
        ).execute()

        object_with_fuel = MockUserObject()
        object_with_fuel.set_property("fuel_volume", 1)
        object_with_fuel.set_property("fuel_velocity", 1)
        macro_commands = [
            CheckFuel(object_with_fuel),
            BurnFuel(object_with_fuel),
        ]
        check_fuel_cmd = IoC.resolve('MacroCommand', macro_commands)
        check_fuel_cmd.execute()
        self.assertTrue(object_with_fuel.get_property("fuel_volume") == 0)

    def test_ios_factory_register_unregister(self):
        IoC.resolve('IoC.Register', 'MacroCommand', MacroCommand).execute()
        object_with_fuel = MockUserObject()
        object_with_fuel.set_property("fuel_volume", 1)
        object_with_fuel.set_property("fuel_velocity", 1)
        macro_commands = [
            CheckFuel(object_with_fuel),
            BurnFuel(object_with_fuel),
        ]
        check_fuel_cmd = IoC.resolve('MacroCommand', macro_commands)
        check_fuel_cmd.execute()
        self.assertTrue(object_with_fuel.get_property("fuel_volume") == 0)
        IoC.resolve('IoC.Register', 'MacroCommand', None).execute()
        self.assertRaises(Exception, IoC.resolve, 'MacroCommand', macro_commands)
