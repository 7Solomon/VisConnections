from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QFrame, QMenu
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QAction


class ListWidget(QListWidget):
    rightClicked = pyqtSignal(QListWidget, QMouseEvent)
    def mousePressEvent(self, event: QMouseEvent):
        item = self.itemAt(event.pos())
        if item is not None:
            if event.button() == Qt.MouseButton.LeftButton:
                if item.isSelected():
                    self.clearSelection()
                    event.accept()
                    return
            if event.button() == Qt.MouseButton.RightButton:
                self.rightClicked.emit(self, event)
        
        super().mousePressEvent(event)

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
        # Variables
        self._previous_selection = set()

        # Setup
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        
        title = QLabel("<b>Scene Objects</b>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        # List
        self.list_widget = ListWidget()
        self.list_widget.setFrameStyle(QFrame.Shape.StyledPanel)
        self.list_widget.setMinimumWidth(200)
        self.list_widget.setMinimumHeight(300)
        self.list_widget.rightClicked.connect(self._show_context_menu)

        
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
        self.list_widget.addItems(self.parent().objectManager.get_object_names())
        self.list_widget.update()
        #print([self.list_widget.item(i).text() for i in range(self.list_widget.count())])
        
    def add_item(self, name: str):
        self.list_widget.addItem(name)
        
    def clear(self):
        self.list_widget.clear()
    
    def _handle_selection(self):
        current_selection = {item.text() for item in self.list_widget.selectedItems()}
        deselected = self._previous_selection - current_selection
        
        # selected items
        for item_text in current_selection:
            self.parent().objectManager.toggle_show_connection_points(
                self.parent().objectManager.get_object_with_id(item_text), 
                True
            )
            
        # deselected items
        for item_text in deselected:
            self.parent().objectManager.toggle_show_connection_points(
                self.parent().objectManager.get_object_with_id(item_text), 
                False
            )
        self._previous_selection = current_selection
    def _show_context_menu(self, list_widget, event):
        item = list_widget.itemAt(event.pos())
        if item is not None:
            menu = QMenu(self)
            obj = self.parent().objectManager.get_object_with_id(item.text())
            is_visible = obj.actor.visibility
        
            visible_action = QAction("Visible", checkable=True, checked=is_visible)
            visible_action.triggered.connect(lambda checked: self._handle_visible(item, checked))
            menu.addAction(visible_action)

            menu.exec(event.globalPos())
    def _handle_visible(self, item, checked):
        obj = self.parent().objectManager.get_object_with_id(item.text())
        self.parent().objectManager.toggle_show_object(obj, checked)