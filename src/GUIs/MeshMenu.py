from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal

class MeshMenu(QMenu):
    #mesh_type_changes = pyqtSignal(str)
    rotate_signal = pyqtSignal(str)
    visibility_signal = pyqtSignal(bool)
    delete_signal = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__("Mesh", parent)
        self.setup_actions()

    def setup_actions(self):
        self.setup_rotation_action()
        self.setup_visibility_action()
        self.setup_delete_action()
    
    ## actions
    def setup_type_action():
        pass
    def setup_rotation_action(self):
        rotate_action = QAction('Rotate', self)
        rotation_menu = QMenu(self)
        rotation_menu.addAction('90° X', lambda: self.rotate_signal.emit('x'))
        rotation_menu.addAction('90° Y', lambda: self.rotate_signal.emit('y'))
        rotation_menu.addAction('90° Z', lambda: self.rotate_signal.emit('z'))
        rotate_action.setMenu(rotation_menu)
        self.addAction(rotate_action)
    def setup_visibility_action(self):
        visibility_action = QAction('Visibility', self)
        visibility_action.setCheckable(True)
        visibility_action.setChecked(True)
        visibility_action.triggered.connect(lambda: self.visibility_signal.emit(visibility_action.isChecked()))
        self.addAction(visibility_action)
    def setup_delete_action(self):
        delete_action = QAction('Delete', self)
        delete_action.triggered.connect(lambda: self.delete_signal.emit())
        self.addAction(delete_action)
