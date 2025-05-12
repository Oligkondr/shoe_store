from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QScrollArea,
)
from PyQt5.QtCore import Qt

from ..widgets import HistoryItemWidget
from ..utils import get_absolute_path, add_class, format_price
from session import session


class OrderWindow(QWidget):
    def __init__(self, data):
        super().__init__()

        # Добавляем окно в отслеживаемые
        session.windows.append(self)

        self._order_id = data["id"]
        self._order_time = data["approved_at"]
        self._order_price = data["price"]
        self._order_items = data["products"]

        self.setWindowTitle(f"Информация о заказе #{self._order_id}")

        self._init_ui()

    def _init_ui(self):
        # Подключение файла стилей
        style_file_path = get_absolute_path(__file__, "../styles/main_style.qss")
        with open(style_file_path, "r") as file:
            style = file.read()
            self.setStyleSheet(style)

        self.setFixedWidth(380)
        self.setMinimumHeight(180)
        n = len(self._order_items)
        self.resize(380, min(400, 94 + 64 * n + 10 * (n - 1) + 30))

        title = QLabel()
        title.setText(f"Заказ #{self._order_id}")
        add_class(title, "title-text")

        order_info = QLabel()
        order_info.setText(
            f"{format_price(self._order_price, self._order_price)} • {self._order_time}"
        )
        add_class(order_info, "small-text")

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(30, 21, 30, 10)
        text_layout.setSpacing(0)
        text_layout.setAlignment(Qt.AlignTop)

        text_layout.addWidget(title, alignment=Qt.AlignTop)
        text_layout.addWidget(order_info, alignment=Qt.AlignTop)

        items_layout = QVBoxLayout()
        items_layout.setContentsMargins(30, 0, 30, 30)
        items_layout.setSpacing(10)
        items_layout.setAlignment(Qt.AlignTop)

        for item_data in self._order_items:
            widget = HistoryItemWidget(item_data)
            widget.setFixedWidth(370)
            items_layout.addWidget(widget, alignment=Qt.AlignTop)
        items_layout.addStretch(1)

        items_container = QWidget()
        items_container.setLayout(items_layout)

        scroll_area = QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(items_container)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        layout.addLayout(text_layout)
        layout.addWidget(scroll_area, 1)

        self.setLayout(layout)

    def closeEvent(self, event):
        if self in session.windows:
            session.windows.remove(self)

        super().closeEvent(event)
