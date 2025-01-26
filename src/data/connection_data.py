from dataclasses import dataclass
from typing import List

from src.data.util_data import Vector3D


@dataclass
class ConnectionPoint:
    position: Vector3D
    type: str = "standard" 

@dataclass
class ConnectionPoints:
    points: List[ConnectionPoint]