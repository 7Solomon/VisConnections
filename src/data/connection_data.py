from dataclasses import dataclass
from typing import List

import numpy as np

from src.data.util_data import Vector3D


@dataclass
class ConnectionPoint:
    position: Vector3D
    type: str = "standard" 
    def translate(self, translation: Vector3D):
        self.position += translation
    

@dataclass
class ConnectionPoints:
    points: List[ConnectionPoint]
    def translate(self, translation: Vector3D):
        for p in self.points:
           p.translate(translation)
    def asNumpyArray(self):
        return np.array([p.position.asTuple() for p in self.points])