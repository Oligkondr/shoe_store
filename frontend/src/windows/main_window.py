from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QFormLayout,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
    QFrame,
    QGridLayout,
    QScrollArea,
)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QColor, QIcon, QResizeEvent

from ..utils import get_absolute_path, clear_layout
from ..layouts import CatalogLayout
from ..widgets import OverlayWidget, CatalogItemWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self._header = QWidget()
        self._logo_btn = QPushButton()
        self._catalog_btn = QPushButton()
        self._search_btn = QPushButton()
        self._cart_btn = QPushButton()
        self._account_btn = QPushButton()

        self._main_container = QWidget()

        self._overlay = OverlayWidget()

        self._init_ui()
        self.show_catalog()

    def _init_ui(self):
        # Подключение файла стилей
        style_file_path = get_absolute_path(__file__, "../styles/main_style.qss")
        with open(style_file_path, "r") as file:
            style = file.read()
            self.setStyleSheet(style)

        window_layout = QVBoxLayout()
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        self._logo_btn.setText("Лого")

        self._catalog_btn.setText("Каталог")

        self._cart_btn.setText("Корзина")

        self._account_btn.setText("Профиль")

        header_layout.addWidget(self._logo_btn)
        header_layout.addWidget(self._catalog_btn)
        header_layout.addStretch(1)
        header_layout.addWidget(self._cart_btn)
        header_layout.addWidget(self._account_btn)

        self._header.setStyleSheet("border-bottom: 1px solid black")
        self._header.setFixedHeight(51)
        self._header.setLayout(header_layout)

        window_layout.addWidget(self._header, alignment=Qt.AlignTop)
        window_layout.addWidget(self._main_container)

        self._overlay.setParent(self._main_container)

        self.setLayout(window_layout)
        self.setMinimumSize(500, 200)

    def _render_form_layout(self, new_layout):
        curr_layout = self._main_container.layout()
        if curr_layout is not None:
            clear_layout(curr_layout)
            QWidget().setLayout(curr_layout)
        self._main_container.setLayout(new_layout)

    def show_catalog(self):
        self._render_form_layout(CatalogLayout(self))

    def show_overlay(self):
        self._overlay.resize()
        self._overlay.show()

    def hide_overlay(self):
        self._overlay.hide()

    def resizeEvent(self, event):
        self._overlay.resize()
        if isinstance(self._main_container.layout(), CatalogLayout):
            self._main_container.layout().resize_catalog()
        super().resizeEvent(event)
