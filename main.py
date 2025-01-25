from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QAction, QIcon
import sys

from src.viewer.View3D import Viewer3DWidget
from src.data import Vector3D

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
        
        self.initUi(layout)
        self.setup_menu_bar()

    
    def setup_menu_bar(self):
        mainMenu = self.menuBar()

        # File menu
        fileMenu = mainMenu.addMenu('File')
        exitButton = QAction('Exit', self)
        exitButton.setShortcut('Ctrl+X')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # Mesh menu
        meshMenu = mainMenu.addMenu('Mesh')
        self.add_sphere_action = QAction('Add Cube', self)
        self.add_sphere_action.triggered.connect(lambda: print("Add Cube"))
        meshMenu.addAction(self.add_sphere_action)

        # View menu
        viewMenu = mainMenu.addMenu('View')
        self.axes_visible = True  # Track visibility state
        self.toggle_axes_action = QAction('Hide Axes', self)
        self.toggle_axes_action.setCheckable(True)
        self.toggle_axes_action.setChecked(True)
        self.toggle_axes_action.triggered.connect(self.toggle_axes)
        viewMenu.addAction(self.toggle_axes_action)

        self.toggle_grid_action = QAction('Hide Grid', self)
        self.toggle_grid_action.setCheckable(True)
        self.toggle_grid_action.setChecked(True)
        self.toggle_grid_action.triggered.connect(self.toggle_grid)
        viewMenu.addAction(self.toggle_grid_action)
        
    def toggle_axes(self):
        self.viewer.toggle_axes_visibility(not self.axes_visible)
        self.toggle_axes_action.setText('Hide Axes' if self.axes_visible else 'Show Axes')
    def toggle_grid(self):
        self.viewer.toggle_grid_visibility(not self.axes_visible)
        self.toggle_grid_action.setText('Hide Grid' if self.axes_visible else 'Show Grid')
        
    def initUi(self, layout):
        self.viewer = Viewer3DWidget()
        layout.addWidget(self.viewer)
        
        # Add some example objects
        self.add_example_objects()
    
    def add_example_objects(self):
        # Add a cube and cylinder as example
        self.viewer.add_hea(position=Vector3D(0,0,0))



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()