from PyQt5.QtWidgets import (
    QLabel,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
)
from PyQt5.QtCore import Qt

from ..utils import add_class


class OverlayMessageWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Блокировка событий мыши по объектам под виджетом
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        self.message_window = QWidget()
        self.message = QLabel()
        self._close_btn = QPushButton()

        self.init_ui()

    def init_ui(self):
        add_class(self, "transparent-background")
        self.move(0, 0)

        self.message.setContentsMargins(10, 0, 10, 0)
        self.message.setWordWrap(True)
        self.message.setAlignment(Qt.AlignCenter)
        self.message.setFixedHeight(50)
        self.message.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        add_class(self.message, "small-text")

        self.message_window.setFixedWidth(230)

        self._close_btn.setText("Закрыть")
        add_class(self._close_btn, "main-btn")
        self._close_btn.setFixedSize(100, 32)
        self._close_btn.setCursor(Qt.PointingHandCursor)
        self._close_btn.clicked.connect(self.hide)

        message_layout = QVBoxLayout()
        message_layout.setContentsMargins(20, 19, 20, 20)
        message_layout.setSpacing(0)

        message_layout.addWidget(self.message)
        message_layout.addSpacing(10)
        message_layout.addWidget(self._close_btn, alignment=Qt.AlignHCenter)

        self.message_window.setLayout(message_layout)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addStretch(1)
        layout.addWidget(self.message_window, alignment=Qt.AlignHCenter)
        layout.addStretch(1)

        self.setLayout(layout)
        self.hide()

    def resize(self):
        if self.parent():
            self.setFixedSize(self.parent().width(), self.parent().height())
