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
    format_price,
    normalize_cart_data,
)
from ..widgets import ClickableWidget, OverlayWidget, CatalogItemWidget, CartItemWidget
from ..classes import RequestThread


class CartLayout(QVBoxLayout):
    def __init__(self, parent_window):
        super().__init__()

        self._parent_window = parent_window

        self._data = None

        self._items_layout = QVBoxLayout()
        self._confirm_btn = QPushButton()
        self._history_btn = QPushButton()
        self._final_price = QLabel()

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

        sublabel = QLabel()
        sublabel.setText("Итоговая цена")
        sublabel.setContentsMargins(0, 0, 1, 0)
        add_class(sublabel, "small-text")

        self._final_price.setText(format_price(0, 0))
        add_class(self._final_price, "title-text")

        final_text_layout = QVBoxLayout()
        final_text_layout.setContentsMargins(0, 0, 0, 0)
        final_text_layout.setSpacing(0)
        final_text_layout.setAlignment(Qt.AlignRight)
        final_text_layout.addSpacing(4)
        final_text_layout.addWidget(sublabel, alignment=Qt.AlignRight)
        final_text_layout.addWidget(self._final_price)

        self._confirm_btn.setText("Оформить заказ")
        add_class(self._confirm_btn, "main-btn", "main-btn_solid")
        self._confirm_btn.setFixedSize(200, 43)
        self._confirm_btn.setCursor(Qt.PointingHandCursor)
        self._confirm_btn.setDisabled(True)

        final_layout = QHBoxLayout()
        final_layout.setContentsMargins(0, 0, 0, 0)
        final_layout.setSpacing(0)
        final_layout.addWidget(self._confirm_btn, alignment=Qt.AlignLeft)
        final_layout.addLayout(final_text_layout, 1)

        ui_layout = QVBoxLayout()
        ui_layout.setContentsMargins(0, 0, 0, 0)
        ui_layout.setSpacing(0)
        ui_layout.setAlignment(Qt.AlignTop)
        ui_layout.addWidget(title)
        ui_layout.addLayout(history_btn_layout)
        ui_layout.addSpacing(17)
        ui_layout.addLayout(final_layout)
        ui_layout.addSpacing(21)
        ui_layout.addWidget(items_container)

        ui_container = QWidget()
        ui_container.setFixedWidth(600)
        ui_container.setLayout(ui_layout)

        centering_layout = QHBoxLayout()
        centering_layout.setContentsMargins(30, 21, 30, 30)
        centering_layout.addWidget(ui_container, alignment=Qt.AlignHCenter)

        centering_layout_container = QWidget()
        centering_layout_container.setLayout(centering_layout)

        scroll_area.setWidget(centering_layout_container)

        self.addWidget(scroll_area)

        # Для обновления числа корзины при открытии главного окна
        self.cart_number_update()

    # Для возможности внешнего вызова
    def full_ui_update(self):
        self._parent_window.show_overlay()
        self._get_cart_data(self._full_ui_update_handler)

    def _full_ui_update_handler(self, response, thread):
        self._handle_get_cart_data_response(response, thread, self._update_ui)

    # Для возможности внешнего вызова
    def price_ui_update(self):
        self._get_cart_data(self._price_ui_update_handler)

    def _price_ui_update_handler(self, response, thread):
        self._handle_get_cart_data_response(response, thread, self._update_price_ui)

    # Для возможности внешнего вызова
    def cart_number_update(self):
        self._get_cart_data(self._cart_number_update_handler)

    def _cart_number_update_handler(self, response, thread):
        self._handle_get_cart_data_response(response, thread, self._update_cart_number)

    def _get_cart_data(self, response_handler):
        url = "http://127.0.0.1:8000/api/v1/order"
        headers = {
            "token": session.token,
        }

        thread = RequestThread(method="GET", url=url, headers=headers)
        session.threads.append(thread)
        thread.finished.connect(response_handler)
        thread.start()

    def _handle_get_cart_data_response(self, response, thread, execute_after_success):
        if thread in session.threads:
            session.threads.remove(thread)

        if isinstance(response, Exception):
            show_error_window()
            self._parent_window.hide_overlay()
        else:
            response_dict = json.loads(response.text)
            if "success" in response_dict:
                if response_dict["success"]:
                    self._data = normalize_cart_data(response_dict["data"])
                else:
                    self._data = {"price": 0, "products": [], "all_amount": 0}
                execute_after_success()
            else:
                show_error_window()

    def _update_ui(self):
        if self._items_layout is not None and self._data is not None:
            clear_layout(self._items_layout)
            if self._data["products"] is None or len(self._data["products"]) == 0:
                label = QLabel("Вы пока не добавили ни одного товара")
                add_class(label, "small-text")

                btn = QPushButton()
                btn.setText("Открыть каталог")
                btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
                add_class(btn, "small-btn")
                btn.setCursor(Qt.PointingHandCursor)
                btn.clicked.connect(self._open_catalog)

                message_layout = QVBoxLayout()
                message_layout.setContentsMargins(0, 0, 0, 0)
                message_layout.setSpacing(0)
                message_layout.setAlignment(Qt.AlignLeft)

                message_layout.addWidget(label)
                message_layout.addWidget(btn)

                message_container = QWidget()
                message_container.setFixedWidth(500)
                message_container.setLayout(message_layout)

                self._items_layout.addWidget(message_container)

                self._final_price.setText(format_price(0, 0))
                self._confirm_btn.setDisabled(True)

            else:
                for item_data in self._data["products"]:
                    widget = CartItemWidget(item_data, self)
                    self._items_layout.addWidget(widget)

            self._parent_window.hide_overlay()

            self._update_price_ui()

    def _update_price_ui(self):
        self._final_price.setText(
            format_price(self._data["price"], self._data["price"])
        )
        if self._data["products"] is None or len(self._data["products"]) == 0:
            self._confirm_btn.setDisabled(True)
        else:
            self._confirm_btn.setDisabled(False)

        self._update_cart_number()

    def _update_cart_number(self):
        self._parent_window.set_cart_number(self._data["all_amount"])

    def _open_catalog(self):
        self._parent_window.show_catalog()
