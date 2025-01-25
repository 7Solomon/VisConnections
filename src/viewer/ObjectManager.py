from typing import Dict, List
from vtkmodules.vtkRenderingCore import vtkActor
import pyvista as pv

from src.data import Vector3D
from src.objectCreaterFunctins import stringToProfile

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal


class SceneObject:
    def __init__(self, type: str, position: Vector3D, length: int, oriantation: Vector3D = Vector3D(1, 0, 0)) -> None:
        self.type = type
        self.mesh = stringToProfile[type](position, length)
        self.position = position
        self.length = length
        self.oriantation = oriantation
            
    def get_connection_points(self) -> List[Vector3D]:
        print('Not implemented yet')
        return []
        

class ObjectManager:
    def __init__(self, plotter: pv.QtInteractor) -> None:
        self.objects: List[SceneObject] = []
        self.plotter = plotter
        self._actors: Dict[SceneObject, vtkActor] = {}
    
    def add_object(self, obj: SceneObject) -> None:
        self.objects.append(obj)
        actor = self.plotter.add_mesh(obj.mesh)
        self._actors[obj] = actor
    
    def remove_object(self, obj: SceneObject) -> None:
        if obj in self.objects:
            if obj in self._actors:
                self.plotter.remove_actor(self._actors[obj])
                del self._actors[obj]
            self.objects.remove(obj)
    
    def clear(self) -> None:
        for obj in list(self._actors.keys()):
            self.remove_object(obj)
        self.objects.clear()
        self._actors.clear()