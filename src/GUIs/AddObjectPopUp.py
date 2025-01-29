from PyQt6.QtWidgets import (QMenu, QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                            QLineEdit, QPushButton, QLabel, QDoubleSpinBox, QWidgetAction)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIntValidator

from src.data.util_data import Vector3D
from src.data.profile_dimensions import DIMENSION_MAP
from src.viewer.ObjectManager import SceneObject

class InputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        # Type Selection
        type_layout = QHBoxLayout()
        type_label = QLabel("Type:")
        self.type_combo = QComboBox()
        self.type_combo.addItems(DIMENSION_MAP.keys())
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        
        # Dimension Selection
        dim_layout = QHBoxLayout()
        dim_label = QLabel("Dimension:")
        self.dim_combo = QComboBox()
        dim_layout.addWidget(dim_label)
        dim_layout.addWidget(self.dim_combo)
        
        # Length
        length_layout = QHBoxLayout()
        length_label = QLabel("Length:")
        self.length_input = QLineEdit()
        self.length_input.setValidator(QIntValidator())
        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_input)

        # Position spinboxes
        self.spinboxes = {}
        spin_layout = QHBoxLayout()
        for i, axis in enumerate(['X', 'Y', 'Z']):
            spin_layout.addWidget(QLabel(f"{axis}:"))
            spinbox = QDoubleSpinBox()
            spinbox.setRange(-999999, 999999)
            spinbox.setDecimals(0)
            spinbox.setValue(0)
            self.spinboxes[axis] = spinbox
            spin_layout.addWidget(spinbox)

        layout.addLayout(type_layout)
        layout.addLayout(dim_layout)
        layout.addLayout(length_layout)
        layout.addLayout(spin_layout)
        
        # Connect type selection change
        self.update_dimensions(self.type_combo.currentText())
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

    def update_dimensions(self, selected_type):
        self.dim_combo.clear()
        filtered_dims = [str(_) for _ in DIMENSION_MAP[selected_type]]
        self.dim_combo.addItems(filtered_dims)

    def get_values(self):
        return (
            self.type_combo.currentText(),
            self.dim_combo.currentText(),
            Vector3D(
                self.spinboxes['X'].value(),
                self.spinboxes['Y'].value(),
                self.spinboxes['Z'].value()
            ),
            self.length_input.text()
        )

class AddObjectPopup(QMenu):
    object_created = pyqtSignal(str,int,Vector3D,int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("Add Object")
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
            self.object_created.emit(type, int(dim), pos, int(length))
            self.close()