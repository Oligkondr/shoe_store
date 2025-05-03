from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, Qt


class ClickableWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cursor_inside = False

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.cursor_inside = True

    def mouseMoveEvent(self, event):
        if not self.rect().contains(event.pos()):
            self.cursor_inside = False

    def mouseReleaseEvent(self, event):
        if self.cursor_inside and (event.button() == Qt.LeftButton):
            self.clicked.emit()
        self.cursor_inside = False
