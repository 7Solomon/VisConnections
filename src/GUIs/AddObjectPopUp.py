from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QComboBox, 
                            QLineEdit, QPushButton, QLabel, QDoubleSpinBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIntValidator

from src.data.util_data import Vector3D
from src.data.profile_dimensions import DIMENSION_MAP
from src.viewer.ObjectManager import SceneObject

class AddObjectPopup(QDialog):
    object_created = pyqtSignal(str,str,Vector3D,int) 

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Object")
        self.setFixedWidth(300)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setup_ui()

    def setup_ui(self):
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
        
        # Connect type selection change
        self.type_combo.currentTextChanged.connect(self.update_dimensions)
        
        # Length
        length_layout = QHBoxLayout()
        length_label = QLabel("Length:")
        self.length_input = QLineEdit()
        self.length_input.setValidator(QIntValidator())
        length_layout.addWidget(length_label)
        length_layout.addWidget(self.length_input)

        ## Name Input
        #name_layout = QHBoxLayout()
        #name_label = QLabel("Name:")
        #self.name_input = QLineEdit()
        #self.name_input.setPlaceholderText("Enter object name")
        #name_layout.addWidget(name_label)
        #name_layout.addWidget(self.name_input)

        # Create spin boxes for pos
        self.spinboxes = {}
        spin_layout = QHBoxLayout()
        for i, axis in enumerate(['X', 'Y', 'Z']):
            spin_layout.addWidget(QLabel(f"{axis}:"))
            spinbox = QDoubleSpinBox()
            spinbox.setRange(999999, 999999)
            spinbox.setDecimals(0)
            spinbox.setValue(0)
            #spinbox.valueChanged.connect(self.on_value_changed) Brauche ich nicht
            self.spinboxes[axis] = spinbox
            spin_layout.addWidget(spinbox)
        
        # Buttons
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        
        # Add to main layout
        layout.addLayout(type_layout)
        layout.addLayout(dim_layout)
        layout.addLayout(length_layout)
        layout.addLayout(spin_layout)
        layout.addLayout(button_layout)

        
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: white;
                border: 1px solid #3f3f3f;
            }
            QLabel {
                color: white;
            }
            QComboBox, QLineEdit {
                background-color: #353535;
                color: white;
                border: 1px solid #3f3f3f;
                padding: 5px;
            }
            QPushButton {
                background-color: #353535;
                color: white;
                border: 1px solid #3f3f3f;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #404040;
            }
        """)
    def update_dimensions(self, selected_type):
        self.dim_combo.clear()
        filtered_dims = [_ for _ in DIMENSION_MAP[selected_type]]
        self.dim_combo.addItems(filtered_dims)
    ### SpinBox
    #def on_value_changed_of_spinbox(self):
    #    x = self.spinboxes['X'].value()
    #    y = self.spinboxes['Y'].value()
    #    z = self.spinboxes['Z'].value()
    #    self.valueChanged.emit(x, y, z)
    #def set_values_of_spinbox(self, x, y, z):
    #    self.spinboxes['X'].setValue(x)
    #    self.spinboxes['Y'].setValue(y)
    #    self.spinboxes['Z'].setValue(z)
    def get_values_of_spinbox(self):
        return Vector3D(
            self.spinboxes['X'].value(),
            self.spinboxes['Y'].value(),
            self.spinboxes['Z'].value()
        )

    def accept(self):
        type = self.type_combo.currentText()
        dim = self.dim_combo.currentText()
        pos = self.get_values_of_spinbox()
        len = self.length_input.text()
        if type and dim and len:
            self.object_created.emit(type, dim, pos, len)
            super().accept()