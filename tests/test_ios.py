from typing import Any
from unittest import TestCase

from src.command import MacroCommand
from src.fiel import CheckFuel, BurnFuel
from src.game_object import IUserObject
from src.ioc import IoCResolver, MacroCmdFactory


class MockUserObject(IUserObject):

    def __init__(self):
        self._properties = {}

    def get_property(self, key: str) -> Any:
        return self._properties[key]

    def set_property(self, key: str, value: str) -> None:
        self._properties[key] = value


class IoCTest(TestCase):

    def test_ios(self):
        ioc = IoCResolver()
        # ioc.register_factory('GameFactory', GameFactory)
        ioc.register_factory('MacroCommand', MacroCommand)
        # object_with_fuel = MockUserObject()
        # object_with_fuel.set_property("fuel_volume", 1)
        # object_with_fuel.set_property("fuel_velocity", 1)
        # check_fuel_cmd = CheckFuel(object_with_fuel)
        # check_fuel_cmd.execute()
        # burn_fuel_cmd = BurnFuel(object_with_fuel)
        object_with_fuel = MockUserObject()
        object_with_fuel.set_property("fuel_volume", 1)
        object_with_fuel.set_property("fuel_velocity", 1)
        macro_commands = [
            CheckFuel(object_with_fuel),
            BurnFuel(object_with_fuel),
        ]
        check_fuel_cmd = ioc.resolve('MacroCommand', macro_commands)
        check_fuel_cmd.execute()
        self.assertTrue(object_with_fuel.get_property("fuel_volume") == 0)

    def test_ios_factory(self):
        ioc = IoCResolver()
        ioc.register_factory('MacroCmdFactory', MacroCmdFactory)
        # object_with_fuel = MockUserObject()
        # object_with_fuel.set_property("fuel_volume", 1)
        # object_with_fuel.set_property("fuel_velocity", 1)
        # check_fuel_cmd = CheckFuel(object_with_fuel)
        # check_fuel_cmd.execute()
        # burn_fuel_cmd = BurnFuel(object_with_fuel)
        object_with_fuel = MockUserObject()
        object_with_fuel.set_property("fuel_volume", 1)
        object_with_fuel.set_property("fuel_velocity", 1)
        macro_commands = [
            CheckFuel(object_with_fuel),
            BurnFuel(object_with_fuel),
        ]
        check_fuel_cmd = ioc.resolve_factory('MacroCmdFactory', macro_commands)
        check_fuel_cmd.execute()
        self.assertTrue(object_with_fuel.get_property("fuel_volume") == 0)

    def test_ios_factory_register(self):
        ioc = IoCResolver()
        ioc.resolve_factory('MacroCmdFactory', MacroCmdFactory)
        # object_with_fuel = MockUserObject()
        # object_with_fuel.set_property("fuel_volume", 1)
        # object_with_fuel.set_property("fuel_velocity", 1)
        # check_fuel_cmd = CheckFuel(object_with_fuel)
        # check_fuel_cmd.execute()
        # burn_fuel_cmd = BurnFuel(object_with_fuel)
        object_with_fuel = MockUserObject()
        object_with_fuel.set_property("fuel_volume", 1)
        object_with_fuel.set_property("fuel_velocity", 1)
        macro_commands = [
            CheckFuel(object_with_fuel),
            BurnFuel(object_with_fuel),
        ]
        check_fuel_cmd = ioc.resolve_factory('MacroCmdFactory', macro_commands)
        check_fuel_cmd.execute()
        self.assertTrue(object_with_fuel.get_property("fuel_volume") == 0)