import pyvista as pv
from PyQt6.QtWidgets import QWidget, QVBoxLayout

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
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        # Create plotter with OpenGL2 rendering
        self.plotter = QtInteractor(lighting='none')
        self.plotter.renderer.SetUseDepthPeeling(True)
        self.plotter.renderer.SetMaximumNumberOfPeels(4)
        
        self.objectManager = ObjectManager(self.plotter)

        layout.addWidget(self.plotter.interactor)
        self.setLayout(layout)
       
        self.setup_scene()
        
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
            color='#808080',
            font_size=10,
            #grid=True,
            #location='all',
            #ticks='inside'
        )
        
        # Set initial camera to isometric view
        self.plotter.camera_position = [
            (1.5, 1.5, 1.5),  # Camera position
            (0.0, 0.0, 0.0),  # Focal point
            (0.0, 0.0, 1.0)   # Camera up vector
        ]
        
        # Weird Stuff
        self.plotter.enable_shadows()
        self.plotter.enable_depth_peeling()
        self.plotter.enable_eye_dome_lighting()


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

    
    ### Object Management
    def add_object(self, obj):
        self.objectManager.add_object(obj)

    def add_hea(self, position= Vector3D(0,0,0), color='white'):
        self.objectManager.add_object(SceneObject('HEA', position, 100))
        
    def clear_scene(self):
        self.objectManager.clear()
        self.plotter.clear()
        self.setup_scene()
    
