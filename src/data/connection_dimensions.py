

from dataclasses import dataclass, fields
from enum import Enum
from typing import List

class LochplattenType(Enum):
    STANDART = 'standard_plate'
    DOUBLE = 'double_plate'
    VERSETZT = 'offset_bolts'

@dataclass
class LochplattenDimensions:
    length: int
    height: int
    tm: int
    t: int

    # Speific
    type: LochplattenType
    e1: int
    e2: int
    p1: int
    p2: int
    d: int
    nx: int
    ny: int

    @classmethod
    def attributes(cls) -> List[str]:
        """Returns list of all attribute names."""
        return [field.name for field in fields(cls)]


class ConnectionType(Enum):
    Lochplatte='Lochplatte' 

