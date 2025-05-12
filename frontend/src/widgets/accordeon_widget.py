from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize

from ..widgets import ClickableWidget
from ..utils import get_absolute_path, add_class, format_price


class AccordeonWidget(QWidget):
    def __init__(self, data):
        super().__init__()

        self._is_opened = False

        self._order_id = data["id"]
        self._order_time = data["approved_at"]
        self._order_price = data["price"]
        self._order_items = data["products"]

        self._header = ClickableWidget()
        self._header.clicked.connect(self._toggle_content)
        self._arrow_icon = QPushButton()

        self._init_ui()

    def _init_ui(self):
        self.setFixedWidth(600)
        self.setContentsMargins(1, 1, 1, 1)

        title = QLabel()
        title.setText(f"Заказ #{self._order_id}")
        add_class(title, "title-text")

        order_info = QLabel()
        order_info.setText(
            f"{format_price(self._order_price, self._order_price)} • {self._order_time}"
        )
        add_class(order_info, "small-text")

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(0)
        text_layout.setAlignment(Qt.AlignTop)

        text_layout.addWidget(title, alignment=Qt.AlignTop)
        text_layout.addWidget(order_info, alignment=Qt.AlignTop)

        self._arrow_icon.setIcon(
            QIcon(get_absolute_path(__file__, "../icons/down.png"))
        )
        self._arrow_icon.setIconSize(QSize(20, 20))
        self._arrow_icon.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)
        header_layout.addLayout(text_layout, 1)
        header_layout.addWidget(self._arrow_icon, alignment=Qt.AlignVCenter)

        self._header.setLayout(header_layout)

        items_layout = QVBoxLayout()
        items_layout.setContentsMargins(20, 20, 20, 20)
        items_layout.setSpacing(10)
        items_layout.setAlignment(Qt.AlignTop)

        from ..widgets import HistoryItemWidget

        for item_data in self._order_items:
            widget = HistoryItemWidget(item_data)
            widget.setFixedWidth(340)
            items_layout.addWidget(widget, alignment=Qt.AlignTop)
        items_layout.addStretch(1)

        self._body = QWidget()
        self._body.setLayout(items_layout)
        n = len(self._order_items)
        self._body.setFixedHeight(64 * n + 10 * (n - 1) + 42)
        add_class(self._body, "gray-border")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addSpacing(0)
        layout.setAlignment(Qt.AlignTop)

        layout.addWidget(self._header)
        layout.addSpacing(10)
        layout.addWidget(self._body, 1)

        self.setLayout(layout)

        self._body.hide()

    def _toggle_content(self):
        self._is_opened = not self._is_opened
        if self._is_opened:
            self._arrow_icon.setIcon(
                QIcon(get_absolute_path(__file__, "../icons/up.png"))
            )
            self._body.show()
        else:
            self._arrow_icon.setIcon(
                QIcon(get_absolute_path(__file__, "../icons/down.png"))
            )
            self._body.hide()
