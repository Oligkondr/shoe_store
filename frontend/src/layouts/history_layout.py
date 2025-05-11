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
from ..widgets import ClickableWidget, OverlayWidget, CatalogItemWidget, CartItemWidget
from ..classes import RequestThread


class HistoryLayout(QVBoxLayout):
    def __init__(self, parent_window):
        super().__init__()
        
        self._parent_window = parent_window
                
        self._items = [1, 2]

        self._items_layout = QVBoxLayout()
        self._confirm_btn = QPushButton()
        self._history_btn = QPushButton()
        self._final_price = QLabel()
        self._final_amount = QLabel()
        
        self._init_ui()

    def _init_ui(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)
        
        title = QLabel()
        title.setText("КОРЗИНА")
        add_class(title, "title-text")
        
        self._history_btn.setText("История заказов")
        self._history_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        add_class(self._history_btn, "small-btn")
        self._history_btn.setCursor(Qt.PointingHandCursor)
        
        history_btn_icon = QLabel(" →")
        history_btn_icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        history_btn_icon.setContentsMargins(0, 0, 0, 1)
        add_class(history_btn_icon, "small-text")

        history_btn_layout = QHBoxLayout()
        history_btn_layout.addWidget(self._history_btn)
        history_btn_layout.addWidget(history_btn_icon)
        history_btn_layout.addStretch(1)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._items_layout.setContentsMargins(0, 0, 0, 0)
        self._items_layout.setSpacing(20)
        self._items_layout.setAlignment(Qt.AlignTop)

        items_container = QWidget()
        items_container.setLayout(self._items_layout)
        
        self._final_amount.setText("Всего товаров: 0")
        add_class(self._final_amount, "small-text")

        self._final_price.setText("0 Р")
        add_class(self._final_price, "title-text")
        
        self._confirm_btn.setText("Оформить заказ")
        add_class(self._confirm_btn, "main-btn", "main-btn_solid")
        self._confirm_btn.setFixedHeight(40)
        self._confirm_btn.setCursor(Qt.PointingHandCursor)
        self._confirm_btn.setDisabled(True)
        
        final_layout = QVBoxLayout()
        final_layout.setContentsMargins(0,0,0,0)
        final_layout.setSpacing(0)
        final_layout.addWidget(self._final_amount, alignment=Qt.AlignLeft)
        final_layout.addWidget(self._final_price, alignment=Qt.AlignLeft)
        final_layout.addSpacing(21)
        final_layout.addWidget(self._confirm_btn)
        
        final_container = QWidget()
        final_container.setFixedWidth(200)
        final_container.setLayout(final_layout)
        
        cart_data_layout = QHBoxLayout()
        cart_data_layout.setContentsMargins(0,0,0,0)
        cart_data_layout.setSpacing(40)
        cart_data_layout.addWidget(items_container)
        cart_data_layout.addWidget(final_container, alignment=Qt.AlignTop)
        
        ui_layout = QVBoxLayout()
        ui_layout.setContentsMargins(0,0,0,0)
        ui_layout.setSpacing(0)
        ui_layout.setAlignment(Qt.AlignTop)
        ui_layout.addWidget(title)
        ui_layout.addLayout(history_btn_layout)
        ui_layout.addSpacing(30)
        ui_layout.addLayout(cart_data_layout)
        
        ui_container = QWidget()
        ui_container.setLayout(ui_layout)
        
        centering_layout = QHBoxLayout()
        centering_layout.setContentsMargins(30, 21, 30, 30)
        centering_layout.addWidget(ui_container, alignment=Qt.AlignHCenter)
        
        centering_layout_container = QWidget()
        centering_layout_container.setLayout(centering_layout)

        scroll_area.setWidget(centering_layout_container)
        
        self.addWidget(scroll_area)

        self._update_ui()
        self._get_items()
    
    def _get_items(self):
        self._parent_window.show_overlay()

        url = "http://127.0.0.1:8000/api/v1/order"
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
                    print (response_dict)
                    # self._data = normalize_catalog_products(products)
                    # self._init_items_ui()

                else:
                    show_error_window()
                    self._parent_window.hide_overlay()
            else:
                show_error_window()
                self._parent_window.hide_overlay()

        self._parent_window.hide_overlay()
        
    def _update_ui(self):
        if self._items_layout is not None:
            clear_layout(self._items_layout)
            if self._items is None or len(self._items) == 0:
                label = QLabel("Вы пока не добавили ни одного товара")
                add_class(label, "small-text")
                
                btn = QPushButton()
                btn.setText("Открыть каталог")
                btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
                add_class(btn, "small-btn")
                btn.setCursor(Qt.PointingHandCursor)
                btn.clicked.connect(self._open_catalog)

                
                message_layout = QVBoxLayout()
                message_layout.setContentsMargins(0,0,0,0)
                message_layout.setSpacing(0)
                message_layout.setAlignment(Qt.AlignLeft)
                
                message_layout.addWidget(label)
                message_layout.addWidget(btn)
                
                message_container = QWidget()
                message_container.setFixedWidth(500)
                message_container.setLayout(message_layout)
                
                self._items_layout.addWidget(message_container)
                
            else:
                for i in range(10):
                    widget = CartItemWidget()
                    self._items_layout.addWidget(widget)
        
    def _update_price(self):
        pass
        # Обновляем только кнопку, цену и итоговое количество продуктов без перерисовки списка товаров
        
    def _open_catalog(self):
        self._parent_window.show_catalog()

    # def _init_items_ui(self):
    #     columns = (self._scroll_area.viewport().width() - 40) // 210
    #     if columns != self._curr_columns:
    #         self._curr_columns = columns
    #         if self._items_layout is not None:
    #             clear_layout(self._items_layout)
                        
    #             title = QLabel()
    #             title.setText("КАТАЛОГ")
    #             add_class(title, "title-text")
    #             title.setFixedHeight(34)
                
    #             self._items_layout.addWidget(title, 0, 0)
    #             if self._data is not None:
    #                 for i, model_data in enumerate(self._data.values()):
    #                     widget = CatalogItemWidget(model_data)
    #                     row = i // self._curr_columns + 1
    #                     column = i % self._curr_columns
    #                     self._items_layout.addWidget(widget, row, column)
    #                 if len(self._data) < self._curr_columns:
    #                     self._items_layout.setColumnStretch(len(self._data), 1)
    #                 self._items_layout.setRowStretch(
    #                     ((len(self._data) - 1) // self._curr_columns) + 2, 1
    #                 )

        
