from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class Vector:

    data: List[float]

    def __add__(self, another: Vector):
        return Vector([a + b for a, b in zip(self.data, another.data)])