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
    show_error_window,
)
from ..widgets import ClickableWidget, OverlayWidget, CatalogItemWidget
from ..classes import RequestThread


class CatalogLayout(QVBoxLayout):
    def __init__(self, parent_window):
        super().__init__()
        
        self._parent_window = parent_window
        
        self._items = list()

        self._curr_columns = 0
        self._items_layout = QGridLayout()
        self._scroll_area = QScrollArea()
        
        self._init_ui()

    def _init_ui(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self._scroll_area.setWidgetResizable(True)

        self._items_layout.setContentsMargins(0, 0, 0, 0)
        self._items_layout.setHorizontalSpacing(20)
        self._items_layout.setVerticalSpacing(24)

        items_container = QWidget()
        items_container.setLayout(self._items_layout)
        
        centering_layout = QHBoxLayout()
        centering_layout.setContentsMargins(30, 30, 30, 30)
        centering_layout.addWidget(items_container, alignment=Qt.AlignHCenter)
        
        centering_layout_container = QWidget()
        centering_layout_container.setLayout(centering_layout)

        self._scroll_area.setWidget(centering_layout_container)

        self.addWidget(self._scroll_area)
        
        # self._get_items()

        QTimer.singleShot(0, self._init_items_ui)
            
    def _get_items(self):
        self._parent_window.show_overlay()

        url = "http://127.0.0.1:8000/api/v1/products"
        headers = {
            "token": session.token,
        }
        
        thread = session.new_thread(
            RequestThread(method="GET", url=url, headers=headers)
        )
        thread.finished.connect(self._handle_get_items_response)
        thread.start()

    def _handle_get_items_response(self, response, thread):
        session.delete_thread(thread)

        if isinstance(response, Exception):
            show_error_window()
            self._parent_window.hide_overlay()
        else:
            print(response.text)
            data = json.loads(response.text)
            if response.status_code == 200:
                pass
            else:
                show_error_window()
                self._parent_window.hide_overlay()
        self._parent_window.hide_overlay()

    def _init_items_ui(self):
        items_count = 100
        columns =  (self._scroll_area.viewport().width() - 40) // 210
        if columns != self._curr_columns:
            self._curr_columns = columns
            if self._items_layout is not None:
                clear_layout(self._items_layout)
                for i in range(items_count):
                    widget = CatalogItemWidget({})
                    row = i // self._curr_columns
                    column = i % self._curr_columns
                    self._items_layout.addWidget(widget, row, column)
            

    def resize_catalog(self):
        self._init_items_ui()
        
