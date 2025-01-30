

from dataclasses import dataclass, fields
from enum import Enum
from typing import List

class LochAbstandsType(Enum):
    STANDART = 1
    VERSETZT = 2

@dataclass
class LochplattenDimensions:
    length: int
    height: int
    t: int

    # Speific
    type: LochAbstandsType
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