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
    normalize_catalog_products,
)
from ..widgets import ClickableWidget, OverlayWidget, CatalogItemWidget
from ..classes import RequestThread


class CatalogLayout(QVBoxLayout):
    def __init__(self, parent_window):
        super().__init__()

        self._parent_window = parent_window

        self._data = None
        self._items = list()

        self._curr_columns = 0
        self._items_layout = QGridLayout()
        self._scroll_area = QScrollArea()

        self._init_ui()

    def _init_ui(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._items_layout.setContentsMargins(0, 0, 0, 0)
        self._items_layout.setHorizontalSpacing(20)
        self._items_layout.setVerticalSpacing(24)

        items_container = QWidget()
        items_container.setLayout(self._items_layout)

        centering_layout = QHBoxLayout()
        centering_layout.setContentsMargins(30, 23, 30, 30)
        centering_layout.addWidget(items_container, alignment=Qt.AlignHCenter)

        centering_layout_container = QWidget()
        centering_layout_container.setLayout(centering_layout)

        self._scroll_area.setWidget(centering_layout_container)

        self.addWidget(self._scroll_area)

        self._get_items()

    def _get_items(self):
        self._parent_window.show_overlay()

        url = "http://127.0.0.1:8000/api/v1/products"
        headers = {
            "token": session.token,
        }

        thread = RequestThread(method="GET", url=url, headers=headers)
        session.threads.append(thread)
        thread.finished.connect(self._handle_get_items_response)
        thread.start()

    def _handle_get_items_response(self, response, thread):
        if thread in session.threads:
            session.threads.remove(thread)

        if isinstance(response, Exception):
            show_error_window()
            self._parent_window.hide_overlay()
        else:
            response_dict = json.loads(response.text)
            if "success" in response_dict:
                if response_dict["success"]:
                    products = response_dict["data"]["products"]
                    self._data = normalize_catalog_products(products)
                    self._init_items_ui()

                else:
                    show_error_window()
                    self._parent_window.hide_overlay()
            else:
                show_error_window()
                self._parent_window.hide_overlay()

        self._parent_window.hide_overlay()

    def _init_items_ui(self):
        columns = (self._scroll_area.viewport().width() - 40) // 210
        if columns != self._curr_columns:
            self._curr_columns = columns
            if self._items_layout is not None:
                clear_layout(self._items_layout)
                        
                title = QLabel()
                add_class(title, "title-text")
                title.setFixedHeight(34)
                self._items_layout.addWidget(title, 0, 0)

                if self._data is not None:
                    for i, model_data in enumerate(self._data.values()):
                        widget = CatalogItemWidget(model_data)
                        row = i // self._curr_columns + 1
                        column = i % self._curr_columns
                        self._items_layout.addWidget(widget, row, column)
                    if len(self._data) < self._curr_columns:
                        self._items_layout.setColumnStretch(len(self._data), 1)
                    self._items_layout.setRowStretch(
                        ((len(self._data) - 1) // self._curr_columns) + 2, 1
                    )
                    title.setText("КАТАЛОГ")


    def resize_catalog(self):
        self._init_items_ui()
