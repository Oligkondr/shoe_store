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
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QColor, QIcon, QResizeEvent

from ..utils import get_absolute_path, clear_layout, add_class
from ..layouts import CatalogLayout
from ..widgets import OverlayWidget, CatalogItemWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

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
        header_layout.setSpacing(0)

        self._logo_btn.setText("Лого")
        self._logo_btn.setFixedWidth(59)
        self._logo_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self._logo_btn.setCursor(Qt.PointingHandCursor)

        self._catalog_btn.setText("Каталог")
        self._catalog_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        add_class(self._catalog_btn, "bold-text")
        self._catalog_btn.setCursor(Qt.PointingHandCursor)

        self._cart_btn.setText("Корзина")
        self._cart_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        add_class(self._cart_btn, "bold-text")
        self._cart_btn.setCursor(Qt.PointingHandCursor)

        self._account_btn.setText("Профиль")
        self._account_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        add_class(self._account_btn, "bold-text")
        self._account_btn.setCursor(Qt.PointingHandCursor)
        
        separators = []
        for i in range(2):
            separators.append(QWidget())
            separators[-1].setFixedWidth(1)
            separators[-1].setStyleSheet("background-color: #dcdcdc")
            separators[-1].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        header_layout.addWidget(self._logo_btn)
        header_layout.addWidget(separators[0])
        header_layout.addSpacing(20)
        header_layout.addWidget(self._catalog_btn)
        header_layout.addStretch(1)
        header_layout.addWidget(separators[1])
        header_layout.addSpacing(20)
        header_layout.addWidget(self._cart_btn)
        header_layout.addSpacing(20)
        header_layout.addWidget(self._account_btn)
        header_layout.addSpacing(20)

        header = QWidget()
        header.setFixedHeight(50)
        header.setLayout(header_layout)
        
        header_underline = QWidget()
        header_underline.setFixedHeight(1)
        header_underline.setStyleSheet("background-color: #dcdcdc")
        header_underline.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        window_layout.addWidget(header, alignment=Qt.AlignTop)
        window_layout.addWidget(header_underline, alignment=Qt.AlignTop)
        window_layout.addWidget(self._main_container)

        self.setLayout(window_layout)
        self.setMinimumSize(640, 480)

        self._overlay.setParent(self)

    def _render_layout(self, new_layout):
        curr_layout = self._main_container.layout()
        if curr_layout is not None:
            clear_layout(curr_layout)
            QWidget().setLayout(curr_layout)
        self._main_container.setLayout(new_layout)

    def show_catalog(self):
        self._render_layout(CatalogLayout(self))

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
