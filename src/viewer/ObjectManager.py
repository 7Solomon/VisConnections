from typing import Dict, List
from vtkmodules.vtkRenderingCore import vtkActor
import pyvista as pv

from src.data.connection_data import ConnectionPoint, ConnectionPoints
from src.data.util_data import Vector3D
from src.objectCreaterFunctins import stringToProfile

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject


class SceneObject:
    def __init__(self, type_name: str, type_number, position: Vector3D, length: int, obj_counter: str, oriantation: Vector3D = Vector3D(1, 0, 0)) -> None:
        self.id =   f"object_{obj_counter}"
        self.position = position
        self.length = length
        self.oriantation = oriantation

        # Mesh generieren
        self.mesh = stringToProfile[type_name](type_number, length)
        self.mesh.translate(position.asTuple())

        # Connection Points
        self.actor = None
        self.connection_actor = None
        self.connection_point_mash = None
    
    def set_actor(self, actor: vtkActor) -> None:
        self.actor = actor
    def set_connection_actor(self, actor: vtkActor) -> None:
        self.connection_actor = actor


    def rotate(self, axis: Vector3D) -> None:
        #self.mesh = self.mesh.rotate_vector(axis.asTuple(), 90, point=self.position.asTuple())  # könnte Falsch sein, da es die verischibung in der x achse nicht berücksichtigt
        print('Rotating')
        #self.mesh.rotate_y(90)
        #self.oriantation = axis
    def get_connection_point_mash(self) -> ConnectionPoints:
        connection_points = ConnectionPoints([
            ConnectionPoint(Vector3D(0, 0, 0)),
            ConnectionPoint(Vector3D(self.length, 0, 0))
        ])
        connection_points.translate(self.position)
        self.connection_point_mash = pv.PolyData(connection_points.asNumpyArray(), force_float=False) # force_float=False, weil asNumpyArray returns int
        return self.connection_point_mash


class ObjectManager(QObject):
    objects_changed = pyqtSignal() 

    def __init__(self, plotter: pv.QtInteractor) -> None:
        super().__init__()
        self.objects: List[SceneObject] = []
        self.plotter = plotter
        self._interconnections = set()
        self._object_counter = 0
    
    def add_object(self, type, dim, position, len) -> None:
        obj = SceneObject(type, dim, position, len, self._object_counter)
        self._object_counter += 1

        actor = self.plotter.add_mesh(obj.mesh, pickable=True)# maybe add pickable=True
        obj.set_actor(actor)    
        # Add connection points
        connection_point_mesh = obj.get_connection_point_mash()
        connection_actor = self.plotter.add_points(
            connection_point_mesh, 
            color='red',
            point_size=10,
            #render_points_as_spheres=True,
        )
        obj.set_connection_actor(connection_actor)

        self.objects.append(obj)
        self.toggle_show_connection_points(obj, False)
        self.objects_changed.emit()
    def add_interconnection(self, main_a:SceneObject, main_b:SceneObject, connector:SceneObject):
        self._interconnections.add({
         'A':   main_a,
         'B': main_b,
         'connector': connector
        })
    

    def remove_object(self, obj: SceneObject) -> None:
        if obj in self.objects: 
            self.plotter.remove_actor(obj.actor)
            self.objects.remove(obj)
            self.objects_changed.emit()

    def rotate_object(self, obj: SceneObject, rotation: Vector3D) -> None:
        if obj in self.objects:
            obj.rotate(rotation)
    
    def toggle_show_object(self, obj: SceneObject, state :bool) -> None:
        if obj in self.objects:
            obj.actor.visibility = state

    def toggle_show_connection_points(self, obj: SceneObject, state :bool) -> None:
        if obj in self.objects:
            obj.connection_actor.visibility = state

    def clear(self) -> None:
        for obj in list(self.objects):
            self.remove_object(obj)
        self.objects.clear()


    def get_object_names(self) -> List[str]:
        return [obj.id for obj in self.objects]
    def get_object_with_id(self, id: str) -> SceneObject:
        for obj in self.objects:
            if obj.id == id:
                return obj    
        raise ValueError(f"Object with id {id} not found")