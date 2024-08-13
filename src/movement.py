from __future__ import annotations

import abc
from dataclasses import dataclass
from typing import List, Any


@dataclass
class Vector:

    data: List[float]

    def __add__(self, another: Vector):
        return Vector([a + b for a, b in zip(self.data, another.data)])


class IMovable(abc.ABC):

    def get_position(self) -> Vector:
        pass

    def set_position(self, value: Vector):
        pass

    def get_velocity(self) -> Vector:
        pass


class IUserObject(abc.ABC):

    def get_property(self, key: str) -> Any:
        pass

    def set_property(self, key: str, value: str) -> None:
        pass


class MovableObjectAdaptor(IMovable):

    def __init__(self, obj: IUserObject):
        self._object = obj

    def get_position(self) -> Vector:
        return self._object.get_property("position")

    def set_position(self, value: Vector):
        self._object.set_property("position", value)

    def get_velocity(self) -> Vector:
        return self._object.get_property("velocity")


class Move:

    def __init__(self, movable: IMovable):
        self._movable = movable

    def execute(self):
        self._movable.set_position(
            self._movable.get_position() + self._movable.get_velocity()
        )


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


class Turn:

    def __init__(self, turnable: ITurnable):
        self._turnable = turnable

    def execute(self):
        self._turnable.set_direction(
            (self._turnable.get_direction() + self._turnable.get_angular_velocity())
            % self._turnable.get_directions_number()
        )
