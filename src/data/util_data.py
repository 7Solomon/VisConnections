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
    def __sub__(self, other: Union['Vector3D', tuple[int, int, int]]) -> 'Vector3D':
        if isinstance(other, tuple):
            ox, oy, oz = other
        else:
            ox, oy, oz = other.x, other.y, other.z
        return Vector3D(
            x=self.x - ox,
            y=self.y - oy,
            z=self.z - oz
        )
    def __mul__(self, other: Union[int, float]) -> 'Vector3D':
        """Multiply vector with scalar."""
        if not isinstance(other, (int, float)):
            raise TypeError(f"unsupported operand type(s) for *: '{type(self)}' and '{type(other)}'")
        return Vector3D(
            x=self.x * other,
            y=self.y * other,
            z=self.z * other
        )
    def __rmul__(self, other: Union[int, float]) -> 'Vector3D':
        """Enable multiplication from right side (int * Vector)."""
        return self.__mul__(other)

    def length_in_direction(self, direction: 'Vector3D') -> int:
        return self.x * direction.x + self.y * direction.y + self.z * direction.z