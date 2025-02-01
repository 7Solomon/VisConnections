from PyQt6.QtWidgets import (QMenu, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                            QLineEdit, QPushButton, QLabel, QDoubleSpinBox, QWidgetAction)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIntValidator

from src.data.util_data import Vector3D
from src.data.connection_dimensions import ConnectionType, LochplattenDimensions
from src.viewer.ObjectManager import SceneObject

class InputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        # Type Selection
        type_layout = QHBoxLayout()
        type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(([type.value for type in ConnectionType]))
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)

        # Schrauben X
        schrauben_x_layout = QHBoxLayout()
        schrauben_x_label = QLabel("Anzahl Schrauben in X-Richtung:")
        self.schrauben_x_input = QLineEdit()
        self.schrauben_x_input.setValidator(QIntValidator())
        schrauben_x_layout.addWidget(schrauben_x_label)
        schrauben_x_layout.addWidget(self.schrauben_x_input)

        # Schrauben Y
        schrauben_y_layout = QHBoxLayout()
        schrauben_y_label = QLabel("Anzahl Schrauben in Y-Richtung:")
        self.schrauben_y_input = QLineEdit()
        self.schrauben_y_input.setValidator(QIntValidator())
        schrauben_y_layout.addWidget(schrauben_y_label)
        schrauben_y_layout.addWidget(self.schrauben_y_input)


        # Connect type selection change
        self.updated_type(self.type_combo.currentText())
        self.type_combo.currentTextChanged.connect(self.update_dimensions)
        
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: white;
            }
            QLabel {
                color: white;
            }
            QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox {
                background-color: #353535;
                color: white;
                border: 1px solid #3f3f3f;
                padding: 5px;
            }
        """)

    def updated_type(self, selected_type):
        pass
        #self.dim_combo.clear()
        #try:
        #    profile_type = ProfileType(selected_type)
        #    sizes = get_available_sizes(profile_type)
        #    self.dim_combo.addItems([str(size) for size in sizes])
        #except ValueError as e:
        #    print(f"Error updating dimensions: {e}")

    def get_values(self):
        return (
            self.type_combo.currentText(),
        )

class AddObjectPopup(QMenu):
    object_created = pyqtSignal(LochplattenDimensions)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Configure Connection")
        self.setup_ui()

    def setup_ui(self):
        self.input_widget = InputWidget()
        widget_action = QWidgetAction(self)
        widget_action.setDefaultWidget(self.input_widget)
        self.addAction(widget_action)
        
        self.addSeparator()
        
        create_action = self.addAction("Create")
        create_action.triggered.connect(self.on_create)

    def on_create(self):
        type, dim, pos, length = self.input_widget.get_values()
        if type and dim and length:
            raise ValueError("Not implemented yet")
            self.object_created.emit()
            self.close()