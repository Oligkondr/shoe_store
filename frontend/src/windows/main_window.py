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
from ..layouts import LoginFormLayout, RegistrationFormLayout
from ..widgets import OverlayWidget, CatalogItemWidget


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self._header = QWidget()
        self._logo_btn = QPushButton()
        self._all_btn = QPushButton()
        self._men_btn = QPushButton()
        self._women_btn = QPushButton()
        self._search_btn = QPushButton()
        self._cart_btn = QPushButton()
        self._account_btn = QPushButton()

        self._main_container = QWidget()
        
        self._curr_columns = 4

        # self.form_container = QWidget()
        # self.close_button = QPushButton()
        # self.overlay = OverlayWidget()

        # # Cохранение позиции для перемещения
        # self.old_window_pos = None

        self._init_ui()
        #self.show_login_form()

    def _init_ui(self):
        # Подключение файла стилей
        # style_file_path = get_absolute_path(__file__, "../styles/login_style.qss")
        # with open(style_file_path, "r") as file:
        #     style = file.read()
        #     self.setStyleSheet(style)

        window_layout = QVBoxLayout()
        window_layout.setContentsMargins(0, 0, 0, 0)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)

        self._header.setStyleSheet("border-bottom: 1px solid black")
        self._header.setFixedHeight(51)
        self._header.setLayout(header_layout)
        
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        
        container = QWidget()
        self._catalog_layout = QGridLayout(container)
        
        scroll_area.setWidget(container)
        
        # columns = 3
        # for i in range(10):
        #     widget = QWidget()
        #     widget.setStyleSheet("background-color: red")
        #     row = i // columns
        #     column = i % columns
        #     self.catalog_layout.addWidget(widget, row, column)

        window_layout.addWidget(self._header, alignment=Qt.AlignTop)
        window_layout.addWidget(scroll_area)

        self.setLayout(window_layout)
        self.setMinimumSize(500, 200)
        
    def resizeEvent(self, event):
        columns = self.width() // 250
        if columns != self._curr_columns:
            self._curr_columns = columns
            clear_layout(self._catalog_layout)
            for i in range(10):
                widget = CatalogItemWidget({})
                #widget.setStyleSheet("background: red")
                row = i // self._curr_columns
                column = i % self._curr_columns
                self._catalog_layout.addWidget(widget, row, column)
            self._catalog_layout.setRowStretch((10 // self._curr_columns) + 2, 1)
        super().resizeEvent(event)
