from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap

from ..utils import get_absolute_path


class OverlayWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Блокировка событий мыши по объектам под виджетом
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        self.setStyleSheet("background-color: rgba(0, 0, 0, 50)")

        pixmap = QPixmap(get_absolute_path(__file__, "../icons/logo_white.png")).scaled(
            50,
            50,
            aspectRatioMode=Qt.KeepAspectRatio,
            transformMode=Qt.SmoothTransformation,
        )
        self.setPixmap(pixmap)
        self.setAlignment(Qt.AlignCenter)

        self.move(0, 0)
        self.hide()

    def resize(self):
        if self.parent():
            self.setFixedSize(self.parent().width(), self.parent().height())
