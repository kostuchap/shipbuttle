from typing import List, Any
import abc


class IUserObject(abc.ABC):

    def get_property(self, key: str) -> Any:
        pass

    def set_property(self, key: str, value: str) -> None:
        pass