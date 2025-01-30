import time
import pyvista as pv
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMenu
from PyQt6.QtGui import QCursor, QAction

from pyvistaqt import QtInteractor
import numpy as np

# Für QtBindings
import os

from src.data.connection_dimensions import ConnectionType
from src.GUIs.MeshMenu import MeshMenu
from src.GUIs.ConnectorMenu import ConnectorMenu
from src.viewer.ObjectManager import ObjectManager, SceneObject
from src.objectCreaterFunctins import create_hea_beam
from src.data.util_data import Vector3D


os.environ["QT_API"] = "pyqt6"
pv.renderer = 'opengl'

class Viewer3DWidget(QWidget):
    def __init__(self, plotter: QtInteractor, object_manager: ObjectManager, parent = None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Create plotter with OpenGL2 rendering
        self.objectManager = object_manager
        self.plotter = plotter
        self.plotter.renderer.SetUseDepthPeeling(True)
        self.plotter.renderer.SetMaximumNumberOfPeels(4)
        

        layout.addWidget(self.plotter.interactor)
        self.setLayout(layout)
       
        self.initVariables()
        self.setup_scene()
        self.setup_mesh_menu()
        self.setup_picker()
    
    def initVariables(self):
        self._active_menu = None

    def setup_scene(self):
        # Configure viewport settings
        self.plotter.background_color = '#263238'  # Material dark blue
        self.plotter.enable_anti_aliasing()
        
        # Add coordinate system with labels
        self.plotter.add_axes(
            xlabel='X', ylabel='Y', zlabel='Z',
            line_width=2,
            x_color='#E74C3C',  # Red
            y_color='#2ECC71',  # Green
            z_color='#3498DB',  # Blue
            shaft_length=0.7,
            tip_length=0.2,
        )
        
        # Add reference grid
        self.plotter.show_grid(
            #color='#808080',
            color='white',
            font_size=12,
            #grid=True,
            #location='all',
            #ticks='inside'
        )
        
        # Set initial camera to isometric view
        self.plotter.camera_position = [
            (500, 150, 150),  # Camera position
            (0.0, 0.0, 0.0),  # Focal point
            (0.0, 0.0, 1.0)   # Camera up vector
        ]
        
        # Weird Stuff
        self.plotter.enable_shadows()
        self.plotter.enable_depth_peeling()
        self.plotter.enable_eye_dome_lighting()


        ## Better Performance
        self.plotter.render_window.SetDesiredUpdateRate(15.0)

    # View Settings
    def toggle_axes_visibility(self, visible=True):
        """Toggle coordinate system visibility"""
        if visible:
            self.plotter.show_axes()
        else:
            self.plotter.hide_axes()

    def toggle_grid_visibility(self, visible=True):
        """Toggle grid visibility"""
        self.plotter.show_grid(show_xaxis=visible, show_yaxis=visible, show_zaxis=visible)
    
    ### Picking
    def setup_picker(self):
        """Setup picking system"""
        # Configure picker
        self.plotter.picker = 'cell'  # Enable cell picking mode
        
        # Enable point picking with debug info
        self.plotter.enable_mesh_picking(
            callback=self.one_mesh_picked,
            show=False,
            show_message=False
            ## Maybe here the drag options of but ka how
        )
        
        ## Track right clicks
        #self.plotter.track_click_position(
        #    callback=self.on_click_position, 
        #    side="right"
        #)

    def one_mesh_picked(self, mesh):
        """Handle cell picking on mesh"""
        actor = self.plotter.picked_actor
        if actor is None:
            return
        
        # Search if connector clicked
        for obj in self.objectManager.objects:
            if obj.connection_actor == actor:
                self.open_connector_menu(obj)
                break         

        # Find the object that owns this actor
        for obj in self.objectManager.objects:
            if obj.actor == actor:
                self.open_mesh_menu(obj)       


    def open_mesh_menu(self, clicked_obj): 
        self.clicked_obj = clicked_obj
        self._active_menu = self.mesh_menu
        self.mesh_menu.popup(QCursor.pos())
    def setup_mesh_menu(self):
        self.mesh_menu = MeshMenu(self)
        self.mesh_menu.delete_signal.connect(lambda: self.handle_delete(self.clicked_obj))
        self.mesh_menu.rotate_signal.connect(lambda axis: self.handle_rotate(self.clicked_obj, axis))
        self.mesh_menu.visibility_signal.connect(lambda checked: self.objectManager.toggle_show_object(self.clicked_obj, checked))
    def open_connector_menu(self, clicked_obj):  # No setup because need clicked obj in init
        connector_menu = ConnectorMenu(clicked_obj, parent=self)
        connector_menu.add_connection_signal.connect(lambda: self.handle_add_connection(clicked_obj))
        self._active_menu = connector_menu
        connector_menu.popup(QCursor.pos())

    def handle_rotate(self, clicked_obj:SceneObject, axis:str):
        clicked_obj.rotate_arround_axis(axis)
    def handle_delete(self, clicked_obj):
        self.objectManager.remove_object(clicked_obj)
    
    def handle_add_connection(self, clicked_obj):
        conn_point = clicked_obj.connection_points.points[0]
        self.objectManager.add_connection(ConnectionType.Lochplatte, conn_point.position, conn_point.oriantation)
        

    #def on_click_position(self, click_position):
    #    """Handle click position"""
    #    print(f"Clicked at position: {click_position}")
        
    def clear_scene(self):
        self.objectManager.clear()
        self.plotter.clear()
        self.setup_scene()
