from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QScrollArea,
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from ..widgets import (
    OverlayWidget,
    ShoeSizeBtnWidget,
    ModelVariationBtnWidget,
    OverlayMessageWidget,
)
from ..utils import (
    get_absolute_path,
    show_error_window,
    add_class,
    clear_layout,
    normalize_item_page_data,
    normalize_order_data,
)
from ..classes import RequestThread
import json
from session import session


class ItemWindow(QWidget):
    def __init__(self, model_id, curr_variation=None):
        super().__init__()

        # Добавляем окно в отслеживаемые
        session.windows.append(self)

        self._model_id = model_id
        self._data = None
        self._curr_variation = curr_variation
        self._curr_size = None

        self._variation_btns = []
        self._size_btns = []

        self._image_container = QLabel()
        self._category_label = QLabel()
        self._title_label = QLabel()
        self._description_label = QLabel()
        self._colors_layout = QHBoxLayout()
        self._colors_grid = QGridLayout()
        self._sizes_grid = QGridLayout()
        self._price_label = QLabel()
        self._add_btn = QPushButton()

        self._overlay_message = OverlayMessageWidget()
        self._overlay = OverlayWidget()

        self._init_ui()
        self._get_model_data()

    def _init_ui(self):
        # Подключение файла стилей
        style_file_path = get_absolute_path(__file__, "../styles/main_style.qss")
        with open(style_file_path, "r") as file:
            style = file.read()
            self.setStyleSheet(style)

        self.setFixedSize(780, 390)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._image_container.setFixedSize(390, 390)

        add_class(self._category_label, "small-text")

        add_class(self._title_label, "title-text")

        self._description_label.setWordWrap(True)
        add_class(self._description_label, "small-text")

        self._colors_layout.setContentsMargins(0, 0, 0, 0)
        self._colors_layout.setSpacing(2)
        self._colors_layout.setAlignment(Qt.AlignLeft)

        self._colors_grid.setSpacing(5)
        self._colors_grid.setContentsMargins(0, 0, 0, 0)

        self._sizes_grid.setSpacing(5)
        self._sizes_grid.setContentsMargins(0, 0, 0, 0)

        add_class(self._price_label, "catalog-item-price")

        self._add_btn.setText("Добавить в корзину")
        add_class(self._add_btn, "main-btn", "main-btn_solid")
        self._add_btn.setFixedHeight(40)
        self._add_btn.setCursor(Qt.PointingHandCursor)
        self._add_btn.setDisabled(True)
        # Вешаем сигнал на кнопку добавления товара
        self._add_btn.clicked.connect(self._start_product_adding)
        self._add_btn.hide()

        ui_layout = QVBoxLayout()
        ui_layout.setContentsMargins(30, 26, 30, 30)
        ui_layout.setSpacing(0)
        ui_layout.setAlignment(Qt.AlignTop)

        ui_layout.addWidget(self._category_label)
        ui_layout.addWidget(self._title_label)
        ui_layout.addSpacing(18)
        ui_layout.addWidget(self._description_label)
        ui_layout.addSpacing(21)
        ui_layout.addLayout(self._colors_layout)
        ui_layout.addSpacing(9)
        ui_layout.addLayout(self._colors_grid)
        ui_layout.addSpacing(30)
        ui_layout.addLayout(self._sizes_grid)
        ui_layout.addSpacing(14)
        ui_layout.addWidget(self._price_label)
        ui_layout.addSpacing(24)
        ui_layout.addWidget(self._add_btn)

        ui_container = QWidget()
        ui_container.setFixedWidth(380)
        ui_container.setLayout(ui_layout)

        scroll_area = QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(ui_container)

        layout.addWidget(self._image_container)
        layout.addWidget(scroll_area)

        self.setLayout(layout)

        self._overlay_message.message.setText("Товар успешно добавлен в корзину!")
        self._overlay_message.setParent(self)
        self._overlay_message.resize()

        self._overlay.setParent(self)
        self._overlay.resize()

    def _get_model_data(self):
        self._overlay.show()

        url = f"http://127.0.0.1:8000/api/v1/products?model_id={self._model_id}"
        headers = {
            "token": session.token,
        }

        thread = RequestThread(method="GET", url=url, headers=headers)
        session.threads.append(thread)
        thread.finished.connect(self._handle_get_model_data_response)
        thread.start()

    def _handle_get_model_data_response(self, response, thread):
        if thread in session.threads:
            session.threads.remove(thread)

        if isinstance(response, Exception):
            show_error_window()
            self._overlay.hide()
        else:
            response_dict = json.loads(response.text)
            if "success" in response_dict:
                if response_dict["success"]:
                    products = response_dict["data"]["products"]
                    self._data = normalize_item_page_data(products)
                    # Настраиваем элементы окна после успешного ответа от сервера
                    self._init_model_ui()
                else:
                    show_error_window()
            else:
                show_error_window()

        self._overlay.hide()

    def _init_model_ui(self):
        self.setWindowTitle(self._data["name"])
        self._category_label.setText(self._data["category"])
        self._title_label.setText(self._data["name"])
        self._description_label.setText(self._data["description"])

        for var_id in self._data["variations"]:
            widget = ModelVariationBtnWidget()
            widget.variation_id = var_id
            pixmap = QPixmap(get_absolute_path(__file__, f"../images/{var_id}.png"))
            widget.image.setPixmap(
                pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            )
            widget.setStyleSheet("border: 1px solid #dcdcdc")
            widget.clicked.connect(self._variation_btn_handler)
            self._variation_btns.append(widget)

        for i, widget in enumerate(self._variation_btns):
            row = i // 5
            column = i % 5
            self._colors_grid.addWidget(widget, row, column, alignment=Qt.AlignLeft)

        if len(self._variation_btns) < 5:
            self._colors_grid.setColumnStretch(len(self._variation_btns), 1)

        if self._curr_variation is None:
            self._curr_variation = self._variation_btns[0].variation_id

        self._update_variation_ui()
        self._add_btn.show()

    def _update_variation_ui(self):
        """
        Перерисовывает виджеты окна в зависимости от выбранной вариации товара.
        """
        clear_layout(self._colors_layout)
        for color in self._data["variations"][self._curr_variation]["colors"]:
            widget = QWidget()
            widget.setFixedSize(12, 12)
            widget.setStyleSheet(f"background-color: #{color}")
            add_class(widget, "color-circle")
            self._colors_layout.addWidget(widget, alignment=Qt.AlignCenter)

        colors_label = QLabel()
        add_class(colors_label, "bold-text")
        colors_label.setContentsMargins(3, 0, 0, 0)
        colors_label.setText(self._data["variations"][self._curr_variation]["name"])
        self._colors_layout.addWidget(colors_label)

        for widget in self._variation_btns:
            if widget.variation_id == self._curr_variation:
                widget.setStyleSheet("border: 1px solid #000000")
            else:
                widget.setStyleSheet("border: 1px solid #dcdcdc")

        clear_layout(self._sizes_grid)
        self._size_btns.clear()
        for size in self._data["variations"][self._curr_variation]["sizes"]:
            widget = ShoeSizeBtnWidget()
            widget.product_size_id = size["product_id"]
            widget.setText(size["value"])
            widget.clicked.connect(self._size_btn_handler)
            self._size_btns.append(widget)

        for i, widget in enumerate(self._size_btns):
            row = i // 5
            column = i % 5
            self._sizes_grid.addWidget(widget, row, column)

        if len(self._size_btns) < 5:
            self._sizes_grid.setColumnStretch(len(self._size_btns), 1)

        self._price_label.setText(
            self._data["variations"][self._curr_variation]["price"]
        )

        image_id = self._curr_variation
        pixmap = QPixmap(get_absolute_path(__file__, f"../images/{image_id}.png"))
        self._image_container.setPixmap(
            pixmap.scaled(390, 390, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

    def _variation_btn_handler(self):
        sender = self.sender()
        if sender.variation_id != self._curr_variation:
            self._curr_size = None
            self._curr_variation = sender.variation_id
            self._update_variation_ui()

    def _size_btn_handler(self):
        sender = self.sender()
        if self._curr_size is None and sender.isChecked():
            self._curr_size = sender
            self._add_btn.setDisabled(False)
        elif self._curr_size == sender and not sender.isChecked():
            self._curr_size = None
            self._add_btn.setDisabled(True)
        else:
            self._curr_size.setChecked(False)
            self._curr_size = sender
            
    def _start_product_adding(self):
        self._get_cart_data()

    def _get_cart_data(self):
        self._overlay.show()

        url = "http://127.0.0.1:8000/api/v1/order"
        headers = {
            "token": session.token,
        }

        thread = RequestThread(method="GET", url=url, headers=headers)
        session.threads.append(thread)
        thread.finished.connect(self._handle_get_cart_data_response)
        thread.start()

    def _handle_get_cart_data_response(self, response, thread):
        if thread in session.threads:
            session.threads.remove(thread)

        if isinstance(response, Exception):
            show_error_window()
            self._parent_window.hide_overlay()
        else:
            response_dict = json.loads(response.text)
            if "success" in response_dict:
                if response_dict["success"]:
                    added_products = normalize_order_data(response_dict["data"])[
                        "products"
                    ]
                    not_in_cart = True
                    for product_data in added_products:
                        if product_data["product_size_id"] == self._curr_size.product_size_id:
                            not_in_cart = False
                    if not_in_cart:
                        self._add_product()
                    else:
                        self._overlay.hide()
                        self._overlay_message.message.setFixedHeight(70)
                        self._overlay_message.message.setText(
                            "Вы уже добавили этот товар. Перейдите в корзину, чтобы изменить его количество."
                        )
                        self._overlay_message.show()
                else:
                    self._add_product()
            else:
                show_error_window()
                self._overlay.hide()

    def _add_product(self):
        url = "http://127.0.0.1:8000/api/v1/product"
        headers = {
            "token": session.token,
        }
        data = {
            "id": self._curr_size.product_size_id,
            "quantity": 1,
        }
        data_json = json.dumps(data)

        thread = RequestThread(method="POST", url=url, data=data_json, headers=headers)
        session.threads.append(thread)
        thread.finished.connect(self._handle_add_product_response)
        thread.start()

    def _handle_add_product_response(self, response, thread):
        if thread in session.threads:
            session.threads.remove(thread)

        if isinstance(response, Exception):
            show_error_window()
            self._overlay.hide()
        else:
            response_dict = json.loads(response.text)
            if "success" in response_dict:
                self._overlay.hide()
                self._overlay_message.message.setFixedHeight(50)
                self._overlay_message.message.setText(
                    "Товар успешно добавлен в корзину!"
                )
                self._overlay_message.show()
                session.curr_window.update_cart()
            else:
                show_error_window()

        self._overlay.hide()

    def _add_btn_handler(self):
        self._overlay_message.show()

    def closeEvent(self, event):
        if self in session.windows:
            session.windows.remove(self)

        super().closeEvent(event)
