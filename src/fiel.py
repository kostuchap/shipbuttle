import abc

from src.command import ICommand
from src.game_object import IUserObject
from src.game_types import CommandException


class CheckFuel(ICommand):

    def __init__(self, obj: IUserObject):
        self._obj = obj
        self._fuel_volume = obj.get_property("fuel_volume")
        self._fuel_velocity = obj.get_property("fuel_velocity")

    def execute(self):
        if self._fuel_volume < self._fuel_velocity:
            raise CommandException("Command exception", 999)


class BurnFuel(ICommand):

    def __init__(self, obj: IUserObject):
        self._obj = obj
        self._fuel_volume = obj.get_property("fuel_volume")
        self._fuel_velocity = obj.get_property("fuel_velocity")

    def execute(self):
        self._obj.set_property("fuel_volume", self._fuel_volume - self._fuel_velocity)


