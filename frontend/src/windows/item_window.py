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

from ..widgets import OverlayWidget, ShoeSizeBtnWidget, ModelVariationBtnWidget, OverlayMessageWidget
from ..utils import get_absolute_path, show_error_window, add_class, clear_layout, normalize_item_page_data
from ..classes import RequestThread
import json
from session import session

example = {
    "id": 0,
    "name": "Топовые тяги",
    "category": "Кроссовки",
    "description": "Топ за свои деньги. Чел, такой бич, как ты, всё равно ничего лучше позволить не сможет.",
    "variations": {
        0: {
            "name": "Закат твоей карьеры",
            "price": "1 000 Р",
            "colors": ["ffffff", "000000"],
            "sizes": [
                {"product_id": 0, "value": "36"},
                {"product_id": 2, "value": "39"},
                {"product_id": 12, "value": "40"},
            ],
        },
        4: {
            "name": "Она просто хотела денег",
            "price": "2 000 Р",
            "colors": ["ffff00", "ff0000", "ffffff"],
            "sizes": [
                {"product_id": 0, "value": "35"},
                {"product_id": 2, "value": "37"},
            ],
        },
    },
}


class ItemWindow(QWidget):
    def __init__(self, model_id=0):
        super().__init__()

        # Добавляем окно в отслеживаемые
        session.windows.append(self)

        self._model_id = model_id
        self._data = None
        self._curr_variation = None
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
        self._image_container.setStyleSheet("background-color: black")

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
        self._add_btn.clicked.connect(self._add_btn_handler)

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
                    self._init_model_ui()
                else:
                    show_error_window()
            else:
                show_error_window()

        self._overlay.hide()

    def _init_model_ui(self):
        self._category_label.setText(self._data["category"])
        self._title_label.setText(self._data["name"])
        self._description_label.setText(self._data["description"])

        for var_id in self._data["variations"]:
            widget = ModelVariationBtnWidget()
            widget.variation_id = var_id
            # !!!
            # Добавить картинку для виджета
            # !!!
            widget.setStyleSheet("border: 1px solid #dcdcdc")
            widget.clicked.connect(self._variation_btn_handler)
            self._variation_btns.append(widget)

        for i, widget in enumerate(self._variation_btns):
            row = i // 5
            column = i % 5
            self._colors_grid.addWidget(widget, row, column, alignment=Qt.AlignLeft)

        if len(self._variation_btns) < 5:
            self._colors_grid.setColumnStretch(len(self._variation_btns), 1)

        self._curr_variation = self._variation_btns[0].variation_id

        self._update_variation_ui()

    def _update_variation_ui(self):
        clear_layout(self._colors_layout)
        for color in self._data["variations"][self._curr_variation]["colors"]:
            widget = QWidget()
            widget.setFixedSize(12, 12)
            widget.setStyleSheet(f"background-color: #{color}")
            add_class(widget, "color-circle")
            self._colors_layout.addWidget(widget, alignment=Qt.AlignCenter)

        colors_label = QLabel()
        add_class(colors_label, "bold-text")
        colors_label.setContentsMargins(3, 0, 0, 2)
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
            widget.item_id = size["product_id"]
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

    def _add_btn_handler(self):
        self._overlay_message.show()

    def closeEvent(self, event):
        if self in session.windows:
            session.windows.remove(self)

        super().closeEvent(event)
