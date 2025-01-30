from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QDockWidget, QListWidget, QFrame
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QEvent
import sys

from pyvistaqt import QtInteractor

from src.data.profile_dimensions import ProfileType
from src.GUIs.MenuBar import MenuBar
from src.GUIs.ObjectList import ObjectListOverlay

from src.viewer.View3D import Viewer3DWidget
from src.data.util_data import Vector3D

from src.viewer.ObjectManager import ObjectManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # window properties
        self.setWindowTitle("VisConnect")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Enable key events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setAttribute(Qt.WidgetAttribute.WA_KeyCompression)
        self.installEventFilter(self)   
        self.eventInitialiser()   

        self.plotter = QtInteractor(lighting='none')
        self.objectManager = ObjectManager(self.plotter)
        self.viewer = Viewer3DWidget(self.plotter, self.objectManager)
        self.initUi(layout)
        self.setup_object_list()
        self.setup_menu_bar()

    def initUi(self, layout):
        layout.addWidget(self.viewer)
        self.add_example_objects()
    def setup_menu_bar(self):
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.menu_bar.toggle_object_list_triggered.connect(self.toggle_object_list_action)
        self.menu_bar.toggle_axes_triggered.connect(self.toggle_axes)
        self.menu_bar.toggle_grid_triggered.connect(self.toggle_grid)
        self.menu_bar.add_scene_object.connect(self.add_scene_object)
    def setup_object_list(self):
        self.object_list = ObjectListOverlay(self)
        self.object_list.move(self.width() - self.object_list.width() - 20, 60)
        
    def toggle_axes(self):
        print('Toggle Axes')
        #self.viewer.toggle_axes_visibility(not self.axes_visible)
        #self.toggle_axes_action.setText('Hide Axes' if self.axes_visible else 'Show Axes')
    def toggle_grid(self):
        print('Toggle Grid')
        #self.viewer.toggle_grid_visibility(not self.axes_visible)
        #self.toggle_grid_action.setText('Hide Grid' if self.axes_visible else 'Show Grid')
    def toggle_object_list_action(self):
        self.object_list.setVisible(not self.object_list.isVisible())
        self.menu_bar.toggle_object_list.setText('Hide Object List' if self.object_list.isVisible() else 'Show Object List')
    
    
    def eventInitialiser(self):
        self.shift_pressed = False
        self.object_list_locked = False
    def eventFilter(self, obj, event):
        # Handle shortcut override first
        if event.type() == QEvent.Type.ShortcutOverride:
            if event.key() == int(Qt.Key.Key_Shift):
                event.accept()
                self.shift_pressed = True
                if not self.object_list_locked:
                    self.object_list.show()
                return True
                
            if (event.key() == int(Qt.Key.Key_Space) and 
                event.modifiers() == Qt.KeyboardModifier.ShiftModifier):
                event.accept()
                self.object_list_locked = not self.object_list_locked
                self.object_list.setVisible(self.object_list_locked)
                return True
                
        # Handle key release
        elif event.type() == QEvent.Type.KeyRelease:
            if event.key() == int(Qt.Key.Key_Shift):
                self.shift_pressed = False
                if not self.object_list_locked:
                    self.object_list.hide()
                return True
                
        return super().eventFilter(obj, event)
    
    def add_example_objects(self):
        self.objectManager.add_object(ProfileType.HEA, 100, Vector3D(0,0,0), 1000)
    def add_scene_object(self, type, dim, position, len):
        self.objectManager.add_object(type, dim, position, len)
        


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()