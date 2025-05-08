from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5.QtCore import Qt

from ..utils import get_absolute_path
from session import session

class ItemWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        # Добавляем окно в отслеживаемые
        session.windows.append(self)
        
        self._init_ui()
    
    def _init_ui(self):
        # Подключение файла стилей
        style_file_path = get_absolute_path(__file__, "../styles/main_style.qss")
        with open(style_file_path, "r") as file:
            style = file.read()
            self.setStyleSheet(style)

        self.setFixedSize(780, 390)
        
    def closeEvent(self, event):
        if self in session.windows:
            session.windows.remove(self)
        
        super().closeEvent(event)