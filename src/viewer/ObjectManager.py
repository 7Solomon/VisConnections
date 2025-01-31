from typing import Dict, List
import vtkmodules.vtkRenderingCore as vtk
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkRenderingCore import vtkActor

from pyvista.core.pointset import PolyData
import pyvista as pv

from src.data.profile_dimensions import ProfileType, get_profile_dimensions
from src.data.connection_dimensions import ConnectionType, LochplattenType, LochplattenDimensions
from src.data.connection_data import ConnectionPoint, ConnectionPoints
from src.data.util_data import Vector3D
from src.objectCreaterFunctins import stringToProfile, stringToConnection

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal, QObject


class SceneObject:
    def __init__(self, type_name: ProfileType, type_number, position: Vector3D, length: int, obj_counter: str, oriantation: Vector3D = Vector3D(1, 0, 0)) -> None:
        self.id =   f"object_{obj_counter}"
        self.origin = position
        self.length = length
        self.oriantation = oriantation

        # Mesh generieren
        self.dimensions = get_profile_dimensions(type_name, type_number)   # Leider double call aber jetzt egal
        self.mesh = stringToProfile[type_name](type_number, length)
        self.mesh.translate(self.origin.asTuple(), inplace=True)

        # Connection Points
        self.actor = None
        self.connection_actor = None
        self.connection_point_mash = None
    
    def set_actor(self, actor: vtkActor) -> None:
        self.actor = actor
    def set_connection_actor(self, actor: vtkActor) -> None:
        self.connection_actor = actor

    def rotate(self, axis: Vector3D, degree: int = 90) -> None:
        self.mesh = self.mesh.rotate_vector(axis.asTuple(), degree, point=self.origin.asTuple())  
        print('ORIANTATION DOES NOT CHANGE, PLEASE IMPLEMENT!!!!')
        #self.oriantation = self.oriantation.rotate(axis, degree)
        self.actor.GetMapper().SetInputData(self.mesh)
        self.actor.GetMapper().Update()
    def rotate_arround_axis(self, axis: str = 'x') -> None:
        if axis == 'x':
            self.rotate(Vector3D(1, 0, 0))
        elif axis == 'y':
            self.rotate(Vector3D(0, 1, 0))
        elif axis == 'z':
            self.rotate(Vector3D(0, 0, 1))
        else:
            raise ValueError(f"Axis {axis} not supported")

    def get_connection_point_mash(self) -> ConnectionPoints:
        self.connection_points = ConnectionPoints([
            ConnectionPoint(Vector3D(0, 0, 0), oriantation=Vector3D(-1, 0, 0)),
            ConnectionPoint(Vector3D(self.length, 0, 0), oriantation=Vector3D(1, 0, 0))
        ])
        self.connection_points.translate(self.origin)
        self.connection_point_mash = pv.PolyData(self.connection_points.asNumpyArray(), force_float=False) # force_float=False, weil asNumpyArray returns int
        return self.connection_point_mash

    ## Color Stuff
    def set_metallic(self):
        colors = vtkNamedColors()
        silver_color = colors.GetColor3d('Silver')
        
        self.actor.GetProperty().SetColor(silver_color)
        #self.actor.GetProperty().SetSpecular(0.7)
        #self.actor.GetProperty().SetSpecularPower(20)
        #self.actor.GetProperty().SetAmbient(0.2)
        #self.actor.GetProperty().SetDiffuse(0.8)

        self.actor.GetMapper().Update()


class SceneConnectorObject:
    def __init__(self, object_1, connection_type, object_2=None) -> None:
        pos1 = object_1.connection_points.points[0].position
        oriantation = object_1.connection_points.points[0].oriantation
        if object_2 is not None:
            pos2 = object_2.connection_points.points[0].position
        else:
            pos2 = oriantation*100 + pos1

        self.origin = pos1
        pos_vector = pos2 - pos1
        self.length = pos_vector.length_in_direction(oriantation)
        ## Add Function for matching type to dimesnion please Future jj
        print('Connection Type:', connection_type)
        print('But makes Lochplatte because of dcebugging')

        print('Here add ABFRAGE OF E1, E2, P1, P2, D, NX, NY')
        self.dimensions = LochplattenDimensions(
                                        type=LochplattenType.DOUBLE, 
                                        length=self.length,
                                        height=object_1.dimensions.h,
                                        tm=object_1.dimensions.tw, 
                                        t=10,
                                        e1=100, e2=100,p1=100, p2=100, d=10, nx=10, ny=10
                                    )
        
        self.mesh = stringToConnection[ConnectionType.Lochplatte](self.dimensions)
        self.mesh.translate(self.origin.asTuple(), inplace=True)
        #self.mesh = stringToConnection[type_name](type_number, length)
        
        # init vars
        self.actor = None 

    
    def set_actor(self, actor: vtkActor) -> None:
        self.actor = actor



class ObjectManager(QObject):
    objects_changed = pyqtSignal() 

    def __init__(self, plotter: pv.QtInteractor) -> None:
        super().__init__()
        self.objects: List[SceneObject] = []
        self.connector_objects: List[SceneConnectorObject] = []
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
            point_size=30,
            #render_points_as_spheres=True,
        )
        obj.set_connection_actor(connection_actor)
        obj.set_metallic()

        self.objects.append(obj)
        self.toggle_show_connection_points(obj, False)
        self.objects_changed.emit()
    def add_connection(self, obj, connection_type, obj_2=None):

        obj = SceneConnectorObject(obj, connection_type, obj_2)

        actor = self.plotter.add_mesh(obj.mesh, pickable=True)
        obj.set_actor(actor)

        self.connector_objects.append(obj)

        #obj = SceneObject(type, , **kwargs)
        
    def add_interconnection(self, main_a:SceneObject, main_b:SceneObject, connector:SceneObject):
        self._interconnections.add({
         'main':   main_a,
         'co_main': main_b,
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
            #obj.actor.mesh = mesh
    
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