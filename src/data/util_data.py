from dataclasses import dataclass
from typing import List, Union

@dataclass(frozen=True)
class Vector3D:
    x: int
    y: int
    z: int
    
    def asTuple(self):
        return self.x, self.y, self.z
    def __add__(self, other: Union['Vector3D', tuple[int, int, int]]) -> 'Vector3D':
        if isinstance(other, tuple):
            ox, oy, oz = other
        else:
            ox, oy, oz = other.x, other.y, other.z
        return Vector3D(
            x=self.x + ox,
            y=self.y + oy,
            z=self.z + oz
        )
