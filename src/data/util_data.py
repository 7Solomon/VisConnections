from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Vector3D:
    x: int
    y: int
    z: int
    
    def asTuple(self):
        return self.x, self.y, self.z
