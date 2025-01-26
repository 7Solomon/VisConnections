from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QFrame
from PyQt6.QtCore import Qt

class ObjectListOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Qt.WindowType.FramelessWindowHint |
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(43, 43, 43, 230);
                color: white;
                border: 1px solid #3f3f3f;
                border-radius: 5px;
            }
            QListWidget {
                background-color: rgba(35, 35, 35, 230);
                border: none;
                color: white;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #404040;
            }
        """)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        
        title = QLabel("<b>Scene Objects</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        # List
        self.list_widget = QListWidget()
        self.list_widget.setFrameStyle(QFrame.Shape.StyledPanel)
        self.list_widget.setMinimumWidth(200)
        self.list_widget.setMinimumHeight(300)
        
        layout.addWidget(title)
        layout.addWidget(self.list_widget)
        
        self.setFixedWidth(250)
        self.setMinimumHeight(400)
        
        self.refresh_items()
        self.parent().objectManager.objects_changed.connect(self.refresh_items)

        # Connect signals
        self.list_widget.itemSelectionChanged.connect(self._handle_selection)


    def refresh_items(self):
        #print('Refreshing items')
        self.list_widget.clear()
        self.list_widget.addItems(self.parent().objectManager._actors.keys())
        self.list_widget.update()
        #print([self.list_widget.item(i).text() for i in range(self.list_widget.count())])
        
    def add_item(self, name: str):
        self.list_widget.addItem(name)
        
    def clear(self):
        self.list_widget.clear()
    
    def _handle_selection(self):
        selected_items = self.list_widget.selectedItems()
        for item in selected_items:
           self.parent().objectManager.toggle_show_connection_points(self.parent().objectManager._actors[item.text()]['object'], True)
        
