from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QScrollArea,
)
from PyQt5.QtCore import Qt

import json
from datetime import datetime, timezone

from session import session
from ..utils import (
    add_class,
    clear_layout,
    show_error_window,
    normalize_order_data,
)
from ..widgets import AccordeonWidget
from ..classes import RequestThread


class HistoryLayout(QVBoxLayout):
    def __init__(self, parent_window):
        super().__init__()

        self._parent_window = parent_window

        self._orders = []

        self._items_layout = QVBoxLayout()
        self._cart_btn = QPushButton()

        self._init_ui()

    def _init_ui(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setSpacing(0)

        title = QLabel()
        title.setText("ИСТОРИЯ ЗАКАЗОВ")
        add_class(title, "title-text")

        self._cart_btn.setText("Корзина")
        self._cart_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        add_class(self._cart_btn, "small-btn")
        self._cart_btn.setCursor(Qt.PointingHandCursor)
        self._cart_btn.clicked.connect(self._parent_window.show_cart)

        cart_btn_icon = QLabel("← ")
        cart_btn_icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        cart_btn_icon.setContentsMargins(0, 0, 0, 1)
        add_class(cart_btn_icon, "small-text")

        cart_btn_layout = QHBoxLayout()
        cart_btn_layout.addWidget(cart_btn_icon)
        cart_btn_layout.addWidget(self._cart_btn)
        cart_btn_layout.addStretch(1)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._items_layout.setContentsMargins(0, 0, 0, 0)
        self._items_layout.setSpacing(9)
        self._items_layout.setAlignment(Qt.AlignTop)

        items_container = QWidget()
        items_container.setLayout(self._items_layout)

        ui_layout = QVBoxLayout()
        ui_layout.setContentsMargins(0, 0, 0, 0)
        ui_layout.setSpacing(0)
        ui_layout.setAlignment(Qt.AlignTop)
        ui_layout.addWidget(title)
        ui_layout.addLayout(cart_btn_layout)
        ui_layout.addSpacing(20)
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

    def ui_update(self):
        self._parent_window.show_overlay()
        self._get_orders()

    def _get_orders(self):
        url = "http://127.0.0.1:8000/api/v1/orders"
        headers = {
            "token": session.token,
        }

        thread = RequestThread(method="GET", url=url, headers=headers)
        session.threads.append(thread)
        thread.finished.connect(self._handle_get_orders_response)
        thread.start()

    def _handle_get_orders_response(self, response, thread):
        if thread in session.threads:
            session.threads.remove(thread)

        if isinstance(response, Exception):
            show_error_window()
            self._parent_window.hide_overlay()
        else:
            response_dict = json.loads(response.text)
            if "success" in response_dict:
                if response_dict["success"]:
                    self._orders.clear()
                    order_data_list = map(
                        normalize_order_data, response_dict["data"]["orders"]
                    )
                    # Сортируем по времени
                    self._orders = sorted(
                        order_data_list,
                        key=lambda order: datetime.strptime(
                            order["timestamp_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
                        ).replace(tzinfo=timezone.utc),
                        reverse=True,
                    )
                    self._update_ui()

                else:
                    show_error_window()
                    self._parent_window.hide_overlay()
            else:
                show_error_window()
                self._parent_window.hide_overlay()

    def _update_ui(self):
        if self._items_layout is not None:
            clear_layout(self._items_layout)
            if len(self._orders) == 0:
                label = QLabel("Вы пока не совершили ни одного заказа")
                add_class(label, "small-text")

                self._items_layout.addWidget(label)
            else:
                for order_data in self._orders:
                    widget = AccordeonWidget(order_data)
                    add_class(widget, "gray-border")
                    self._items_layout.addWidget(widget, alignment=Qt.AlignTop)
        self._parent_window.hide_overlay()
