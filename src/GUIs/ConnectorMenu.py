from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import pyqtSignal

from src.data.connection_dimensions import ConnectionType

class ConnectorMenu(QMenu):
    #mesh_type_changes = pyqtSignal(str)
    add_connection_signal = pyqtSignal(ConnectionType)

    def __init__(self, obj, parent=None):
        super().__init__(parent=parent)
        self.obj = obj
        self.setup_actions()

    def setup_actions(self):
        self.setup_add_connection_action()
    
    ## actions
    def setup_add_connection_action(self):
        add_connection_action = QAction('Add Connection', self)
        add_connection_menu = QMenu(self)
        add_connection_menu.addAction('Add Lochplatte', lambda: self.add_connection_signal.emit(ConnectionType.Lochplatte))
        #if self.obj.

        add_connection_action.setMenu(add_connection_menu)
        self.addAction(add_connection_action)
