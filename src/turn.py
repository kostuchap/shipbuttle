import abc

from src.command import ICommand
from src.game_object import IUserObject


class ITurnable(abc.ABC):

    def get_direction(self) -> int:
        pass

    def get_directions_number(self) -> int:
        pass

    def set_direction(self, value: int):
        pass

    def get_angular_velocity(self) -> int:
        pass


class TurnableObjectAdaptor(ITurnable):

    def __init__(self, obj: IUserObject):
        self._object = obj

    def get_direction(self) -> int:
        return self._object.get_property("direction")

    def get_directions_number(self) -> int:
        return self._object.get_property("directions_number")

    def set_direction(self, value: int):
        self._object.set_property("direction", value)

    def get_angular_velocity(self) -> int:
        return self._object.get_property("angular_velocity")


class Turn(ICommand):

    def __init__(self, turnable: ITurnable):
        self._turnable = turnable

    def execute(self):
        self._turnable.set_direction(
            (self._turnable.get_direction() + self._turnable.get_angular_velocity())
            % self._turnable.get_directions_number()
        )
