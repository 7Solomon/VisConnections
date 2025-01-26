from typing import Dict, List
from vtkmodules.vtkRenderingCore import vtkActor
import pyvista as pv

from src.data.connection_data import ConnectionPoint, ConnectionPoints
from src.data.util_data import Vector3D
from src.objectCreaterFunctins import stringToProfile

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject


class SceneObject:
    def __init__(self, type: str, position: Vector3D, length: int, oriantation: Vector3D = Vector3D(1, 0, 0)) -> None:
        self.type = type
        self.position = position
        self.length = length
        self.oriantation = oriantation

        # Mesh generieren
        self.mesh = stringToProfile[type](length)
        self.mesh.translate(position.asTuple())
        # Connection Points
        self._init_connection_points()

    def rotate(self, axis: Vector3D) -> None:
        self.mesh = self.mesh.rotate_vector(axis.asTuple(), 90, point=self.position.asTuple())  # könnte Falsch sein, da es die verischibung in der x achse nicht berücksichtigt
        print('Rotating')
        #self.mesh.rotate_y(90)
        self.oriantation = axis
    def _init_connection_points(self):
        #half_length = self.length / 2
        self.connection_points = ConnectionPoints([
            ConnectionPoint(Vector3D(0, 0, 0)),
            ConnectionPoint(Vector3D(self.length, 0, 0))
        ])


class ObjectManager(QObject):
    objects_changed = pyqtSignal() 

    def __init__(self, plotter: pv.QtInteractor) -> None:
        super().__init__()
        self.objects: List[SceneObject] = []
        self.plotter = plotter
        self._actors: Dict[str,vtkActor|SceneObject|dict] = {}
        self._object_counter = 0
    
    def add_object(self, obj: SceneObject) -> None:
        key = f"object_{self._object_counter}"
        self._object_counter += 1

        self.objects.append(obj)
        actor = self.plotter.add_mesh(obj.mesh, pickable=True)# maybe add pickable=True

        # Add connection points
        points = pv.PolyData()
        point_coords = [p.position.asTuple() for p in obj.connection_points.points]
        points.points = point_coords
        connection_actor = self.plotter.add_mesh(
            points, 
            color='red',
            point_size=10,
            render_points_as_spheres=True
        )

        self._actors[key] = {
                'actor': actor,
                'object': obj, 
                'connections':  {
                                    'points': obj.connection_points.points,
                                    'actor': connection_actor
                                }
                            }
        self.objects_changed.emit()

    def remove_object(self, obj: SceneObject) -> None:
        if obj in self.objects: 
            keyOfObject = next(key for (key, val) in self._actors.items() if val['object'] == obj)
            if keyOfObject:
                self.plotter.remove_actor(self._actors[keyOfObject]['actor'])
                del self._actors[keyOfObject]
            self.objects.remove(obj)

    def rotate_object(self, obj: SceneObject, rotation: Vector3D) -> None:
        if obj in [entry['object'] for entry in self._actors.values()]:
            # Update mesh directly
            obj.rotate(rotation)
            self.update_actor(obj)

    def update_actor(self, obj: SceneObject) -> None:
        """Re-render specific actor in scene"""
        keyOfObject = next(key for (key, val) in self._actors.items() if val['object'] == obj)
        if keyOfObject:
            self.plotter.remove_actor(self._actors[keyOfObject]['actor'])
            self._actors[keyOfObject]['actor'] = self.plotter.add_mesh(obj.mesh, pickable=True)
            self.plotter.render()
    
    def toggle_show_connection_points(self, obj: SceneObject, state :bool) -> None:
        keyOfObject = next(key for (key, val) in self._actors.items() if val['object'] == obj)
        if keyOfObject:
            if state:
                print('Not implemented')
                #obj.show_connection_points(self.plotter)
            else:
                print('Not implemented')
                #obj.hide_connection_points(self.plotter)
            self.update_actor(obj)

    def clear(self) -> None:
        for value in list(self._actors.values()):
            self.remove_object(value['object'])
        self.objects.clear()
        self._actors.clear()