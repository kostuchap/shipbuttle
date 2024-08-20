import abc

from src.command import ICommand
from src.game_object import IUserObject
from src.game_types import Vector


# @dataclass
# class Vector:
#
#     data: List[float]
#
#     def __add__(self, another: Vector):
#         return Vector([a + b for a, b in zip(self.data, another.data)])


class IMovable(abc.ABC):

    def get_position(self) -> Vector:
        pass

    def set_position(self, value: Vector):
        pass

    def get_velocity(self) -> Vector:
        pass


# class IUserObject(abc.ABC):
#
#     def get_property(self, key: str) -> Any:
#         pass
#
#     def set_property(self, key: str, value: str) -> None:
#         pass


class MovableObjectAdaptor(IMovable):

    def __init__(self, obj: IUserObject):
        self._object = obj

    def get_position(self) -> Vector:
        return self._object.get_property("position")

    def set_position(self, value: Vector):
        self._object.set_property("position", value)

    def get_velocity(self) -> Vector:
        return self._object.get_property("velocity")


class Move(ICommand):

    def __init__(self, movable: IMovable):
        self._movable = movable

    def execute(self):
        self._movable.set_position(
            self._movable.get_position() + self._movable.get_velocity()
        )


