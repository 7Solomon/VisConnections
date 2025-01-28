from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal

from src.GUIs.AddObjectPopUp import AddObjectPopup

class MenuBar(QMenuBar):
    add_scene_object = pyqtSignal()
    toggle_axes_triggered = pyqtSignal(bool)
    toggle_grid_triggered = pyqtSignal(bool)
    toggle_object_list_triggered = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_file_menu()
        self.setup_mesh_menu()
        self.setup_view_menu()

    def setup_file_menu(self):
        file_menu = self.addMenu('File')
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+X')
        exit_action.triggered.connect(self.parent().close)
        file_menu.addAction(exit_action)

    def setup_mesh_menu(self):
        mesh_menu = self.addMenu('Mesh')
        add_sphere = QAction('Add Object', self)
        add_sphere.triggered.connect(self.show_add_popup)
        mesh_menu.addAction(add_sphere)

    def setup_view_menu(self):
        view_menu = self.addMenu('View')
        
        self.toggle_axes = QAction('Axes', self)
        self.toggle_axes.setCheckable(True)
        self.toggle_axes.setChecked(True)
        self.toggle_axes.triggered.connect(self.toggle_axes_triggered.emit)
        
        self.toggle_grid = QAction('Grid', self)
        self.toggle_grid.setCheckable(True)
        self.toggle_grid.triggered.connect(self.toggle_grid_triggered.emit)
        
        self.toggle_object_list = QAction('Object List', self)
        self.toggle_object_list.setCheckable(True)
        self.toggle_object_list.setChecked(True)
        self.toggle_object_list.triggered.connect(self.toggle_object_list_triggered.emit)
        
        view_menu.addAction(self.toggle_axes)
        view_menu.addAction(self.toggle_grid)
        view_menu.addAction(self.toggle_object_list)
    
    def show_add_popup(self):
        popup = AddObjectPopup(self)
        popup.object_created.connect(lambda type, dim, pos, len: self.add_scene_object.emit(type, dim, pos, len))
        popup.exec()
