from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal


class ClickableWidget(QWidget):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()
