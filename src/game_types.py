from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class Vector:

    data: List[float]

    def __add__(self, another: Vector):
        return Vector([a + b for a, b in zip(self.data, another.data)])


class CommandException(Exception):

    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code

    def __str__(self):
        return f"{self.args[0]} (Error Code: {self.error_code})"