from PyQt5.QtWidgets import QLabel, QWidget, QLayout, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from ..utils import (
    get_absolute_path,
    delete_layout,
    delete_widget,
    replace_widget_in_layout,
)


class OverlayMessageWidget(QWidget):
    def __init__(self, message_widget=None, parent=None):
        super().__init__(parent)

        # Блокировка событий мыши по объектам под виджетом
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        self._layout = QVBoxLayout()
        self._message_widget = message_widget

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: rgba(0, 0, 0, 50)")
        self.move(0, 0)

        self._layout.setContentsMargins(0, 0, 0, 0)

        self._layout.addStretch(1)
        self._layout.addWidget(self._message_widget, alignment=Qt.AlignHCenter)
        self._layout.addStretch(1)

        self.setLayout(self._layout)
        self.hide()

    def change_message_widget(self, new_widget: QWidget):
        replace_widget_in_layout(self._layout, self._message_widget, new_widget)
        self._message_widget = new_widget

    def resize(self):
        if self.parent():
            self.setFixedSize(self.parent().width(), self.parent().height())
