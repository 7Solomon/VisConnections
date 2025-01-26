import time
import pyvista as pv
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMenu
from PyQt6.QtGui import QCursor

from pyvistaqt import QtInteractor
import numpy as np

# Für QtBindings
import os

from src.viewer.ObjectManager import ObjectManager, SceneObject
from src.objectCreaterFunctins import create_hea_beam
from src.data import Vector3D

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

        # Find the object that owns this actor
        for value in self.objectManager._actors.values():
            if value['actor'] == actor:
                print(f"Selected object: {value['object']}")
                self.open_mesh_menu(value['object'])
                
    

    def open_mesh_menu(self, clicked_obj):
        menu = QMenu(self)
        rotate_action = menu.addAction("Rotate")
        rotate_action.triggered.connect(lambda: self.handle_rotate(clicked_obj))
        delete_action = menu.addAction("Delete")
        delete_action.triggered.connect(lambda: self.handle_delete(clicked_obj))
        self._active_menu = menu
        menu.popup(QCursor.pos())
    
    def handle_rotate(self, clicked_obj):
        self.objectManager.rotate_object(clicked_obj, Vector3D(0, 1, 0))


    def handle_delete(self, clicked_obj):
        self.objectManager.remove_object(clicked_obj)


    #def on_click_position(self, click_position):
    #    """Handle click position"""
    #    print(f"Clicked at position: {click_position}")

    
    ### Object Management
    def add_object(self, obj):
        self.objectManager.add_object(obj)

    def add_hea(self, position= Vector3D(0,0,0), color='white'):
        self.objectManager.add_object(SceneObject('HEA', position, 100))
        
    def clear_scene(self):
        self.objectManager.clear()
        self.plotter.clear()
        self.setup_scene()
