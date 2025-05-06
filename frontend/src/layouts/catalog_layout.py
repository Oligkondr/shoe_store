from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QScrollArea,
    QGridLayout,
)
from PyQt5.QtCore import Qt, QSize, QTimer, QByteArray, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from enum import Enum
import requests
import json

from session import session

from ..utils import (
    get_absolute_path,
    add_class,
    remove_class,
    toggle_class,
    validate_login_email,
    validate_login_password,
    clear_layout,
)
from ..widgets import ClickableWidget, OverlayWidget, CatalogItemWidget


class CatalogLayout(QVBoxLayout):
    def __init__(self, show_overlay, hide_overlay):
        super().__init__()
        
        self.show_overlay = show_overlay
        self.hide_overlay = hide_overlay
        
        self._items = list()

        self._curr_columns = 2
        self._items_layout = QGridLayout()
        self._scroll_area = QScrollArea()
        
        self._init_ui()
        QTimer.singleShot(0, self._init_items_ui)

    def _init_ui(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self._scroll_area.setWidgetResizable(True)

        self._items_layout.setContentsMargins(0, 0, 0, 0)
        self._items_layout.setSpacing(20)

        items_container = QWidget()
        items_container.setLayout(self._items_layout)
        
        centering_layout = QHBoxLayout()
        centering_layout.setContentsMargins(20, 20, 20, 20)
        centering_layout.addWidget(items_container, alignment=Qt.AlignHCenter)
        
        centering_layout_container = QWidget()
        centering_layout_container.setLayout(centering_layout)

        self._scroll_area.setWidget(centering_layout_container)

        self.addWidget(self._scroll_area)
    
        
    
    def _init_items_ui(self):
        columns =  (self._scroll_area.viewport().width() - 20) // 200
        if columns != self._curr_columns:
            self._curr_columns = columns
            clear_layout(self._items_layout)
            for i in range(5):
                widget = CatalogItemWidget({})
                row = i // self._curr_columns
                column = i % self._curr_columns
                self._items_layout.addWidget(widget, row, column)

    def resize_catalog(self):
        self._init_items_ui()
        
