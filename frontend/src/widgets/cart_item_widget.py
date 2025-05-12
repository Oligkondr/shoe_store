from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize

import json

from ..utils import get_absolute_path, add_class, format_price, show_error_window
from ..classes import RequestThread
from session import session

example = {
    "item_id": 10,
    "model_name": "Топовые тяги",
    "model_id": 2,
    "variation_name": "Закат твтоей карьеры",
    "variation_id": 2,
    "size": "41",
    "amount": 1,
    "price": 1000,
}


class CartItemWidget(QWidget):
    def __init__(self, data, parent_layout, parent=None):
        super().__init__(parent)

        self._parent_layout = parent_layout

        self._item_id = data["item_id"]
        self._item_model_name = data["model_name"]
        self._item_model_id = data["model_id"]
        self._item_variation_name = data["variation_name"]
        self._item_variation_id = data["variation_id"]
        self._item_size = data["size"]
        self._item_amount = data["amount"]
        self._item_price = data["price"]
        self._item_product_size_id = data["product_size_id"]

        self._title_btn = QPushButton()
        self._plus_btn = QPushButton()
        self._minus_btn = QPushButton()
        self._amount_label = QLabel()
        self._delete_btn = QPushButton()
        self._price_label = QLabel()
        self._amount_input_container = QWidget()
        self._overlay = QWidget()

        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        self.setFixedSize(600, 150)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        image_container = QLabel()
        image_container.setFixedSize(150, 150)
        pixmap = QPixmap(
            get_absolute_path(__file__, f"../images/small/{self._item_variation_id}.jpg")
        )
        image_container.setPixmap(
            pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        self._title_btn.setText(self._item_model_name)
        add_class(self._title_btn, "catalog-item-price")
        self._title_btn.setCursor(Qt.PointingHandCursor)

        color = QLabel()
        color.setText(self._item_variation_name)
        add_class(color, "catalog-item-text")

        size = QLabel()
        size.setText(f"Размер: {self._item_size}")
        add_class(size, "catalog-item-text")

        self._amount_input_container = QWidget()
        self._amount_input_container.setFixedSize(110, 32)

        self._minus_btn.setFixedSize(32, 32)
        self._minus_btn.setIcon(
            QIcon(get_absolute_path(__file__, "../icons/minus.png"))
        )
        self._minus_btn.setIconSize(QSize(12, 12))
        self._minus_btn.setCursor(Qt.PointingHandCursor)
        add_class(self._minus_btn, "amount-input-btn")

        self._plus_btn.setFixedSize(32, 32)
        self._plus_btn.setIcon(QIcon(get_absolute_path(__file__, "../icons/plus.png")))
        self._plus_btn.setIconSize(QSize(12, 12))
        self._plus_btn.setCursor(Qt.PointingHandCursor)
        add_class(self._plus_btn, "amount-input-btn")

        self._amount_label.setFixedHeight(32)
        self._amount_label.setAlignment(Qt.AlignCenter)
        self._amount_label.setContentsMargins(0, 0, 0, 1)
        add_class(self._amount_label, "amount-input")

        amount_input_layout = QHBoxLayout()
        amount_input_layout.setContentsMargins(0, 0, 0, 0)
        amount_input_layout.setSpacing(0)
        amount_input_layout.addWidget(self._minus_btn)
        amount_input_layout.addWidget(self._amount_label, 1)
        amount_input_layout.addWidget(self._plus_btn)

        self._amount_input_container.setLayout(amount_input_layout)

        layout1 = QVBoxLayout()
        layout1.setContentsMargins(0, 12, 0, 20)
        layout1.setSpacing(0)
        layout1.setAlignment(Qt.AlignLeft)
        layout1.addWidget(self._title_btn)
        layout1.addWidget(color)
        layout1.addWidget(size)
        layout1.addStretch(1)
        layout1.addWidget(self._amount_input_container)

        add_class(self._price_label, "catalog-item-price")

        self._delete_btn.setText("Удалить")
        self._delete_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        add_class(self._delete_btn, "small-btn")
        self._delete_btn.setCursor(Qt.PointingHandCursor)

        layout2 = QVBoxLayout()
        layout2.setContentsMargins(0, 12, 0, 20)
        layout2.setSpacing(0)
        layout2.setAlignment(Qt.AlignRight)
        layout2.addWidget(self._price_label)
        layout2.addWidget(self._delete_btn, alignment=Qt.AlignRight)
        layout2.addStretch(1)

        layout.addWidget(image_container)
        layout.addLayout(layout1, 1)
        layout.addLayout(layout2, 1)

        self.setLayout(layout)

        self._overlay.setAttribute(Qt.WA_TransparentForMouseEvents, False)
        self._overlay.setStyleSheet("background-color: rgba(255, 255, 255, 127)")
        self._overlay.setGeometry(0, 0, self.width(), self.height())
        self._overlay.hide()
        self._overlay.setParent(self)

        self._update_ui()

    def _connect_signals(self):
        self._plus_btn.clicked.connect(self._plus_btn_handler)
        self._minus_btn.clicked.connect(self._minus_btn_handler)
        self._delete_btn.clicked.connect(self._delete_item)
        self._title_btn.clicked.connect(self._open_item_page)

    def _update_ui(self):
        new_price = self._item_amount * self._item_price
        self._price_label.setText(format_price(new_price, new_price))
        self._amount_label.setText(str(self._item_amount))
        self._update_btns()

    def _plus_btn_handler(self):
        self._item_amount += 1
        self._update_ui()
        self._update_item_amount()

    def _minus_btn_handler(self):
        self._item_amount -= 1
        self._update_ui()
        self._update_item_amount()

    def _delete_item(self):
        self._overlay.show()
        url = f"http://127.0.0.1:8000/api/v1/product/{self._item_id}"
        headers = {
            "token": session.token,
        }

        thread = RequestThread(method="DELETE", url=url, headers=headers)
        session.threads.append(thread)
        thread.finished.connect(self._handle_delete_item_response)
        thread.start()

    def _handle_delete_item_response(self, response, thread):
        if thread in session.threads:
            session.threads.remove(thread)

        if isinstance(response, Exception):
            show_error_window()
            self._overlay.hide()
        else:
            response_dict = json.loads(response.text)
            if "success" in response_dict:
                if response_dict["success"]:
                    self._parent_layout.price_ui_update()
                    self.hide()
                else:
                    show_error_window()
            else:
                show_error_window()

        self._overlay.hide()

    def _update_item_amount(self):
        self._amount_input_container.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        url = f"http://127.0.0.1:8000/api/v1/product/{self._item_id}"
        headers = {
            "token": session.token,
        }
        data = {
            "quantity": self._item_amount,
        }
        data_json = json.dumps(data)

        thread = RequestThread(method="PATCH", url=url, headers=headers, data=data_json)
        session.threads.append(thread)
        thread.finished.connect(self._handle_update_item_amount_response)
        thread.start()

    def _handle_update_item_amount_response(self, response, thread):
        if thread in session.threads:
            session.threads.remove(thread)

        if isinstance(response, Exception):
            show_error_window()
            self._overlay.hide()
        else:
            response_dict = json.loads(response.text)
            if "success" in response_dict:
                if response_dict["success"]:
                    self._parent_layout.price_ui_update()
                else:
                    show_error_window()
            else:
                show_error_window()

        self._amount_input_container.setAttribute(
            Qt.WA_TransparentForMouseEvents, False
        )

    def _update_btns(self):
        if self._item_amount == 1:
            self._minus_btn.setDisabled(True)
            self._minus_btn.setIcon(
                QIcon(get_absolute_path(__file__, "../icons/minus_grey.png"))
            )
        elif self._item_amount == 10:
            self._plus_btn.setDisabled(True)
            self._plus_btn.setIcon(
                QIcon(get_absolute_path(__file__, "../icons/plus_grey.png"))
            )
        else:
            self._minus_btn.setDisabled(False)
            self._minus_btn.setIcon(
                QIcon(get_absolute_path(__file__, "../icons/minus.png"))
            )
            self._plus_btn.setDisabled(False)
            self._plus_btn.setIcon(
                QIcon(get_absolute_path(__file__, "../icons/plus.png"))
            )

    def _open_item_page(self):
        from ..windows import ItemWindow

        window = ItemWindow(self._item_model_id, self._item_variation_id)
        window.show()
