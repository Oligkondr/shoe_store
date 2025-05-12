from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from ..utils import get_absolute_path, add_class

example = {
    "item_id": 10,
    "model_name": "Топовые тяги",
    "model_id": 2,
    "variation_name": "Закат твоей карьеры",
    "variation_id": 2,
    "size": "41",
    "amount": 1,
    "price": 1000,
}


class HistoryItemWidget(QWidget):
    def __init__(self, data=example, parent=None):
        super().__init__(parent)

        self._item_id = data["item_id"]
        self._item_model_name = data["model_name"]
        self._item_model_id = data["model_id"]
        self._item_variation_name = data["variation_name"]
        self._item_variation_id = data["variation_id"]
        self._item_size = data["size"]
        self._item_amount = data["amount"]
        self._item_price = data["price"]

        self._title_btn = QPushButton()

        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        self.setFixedHeight(64)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        image_container = QLabel()
        image_container.setFixedSize(64, 64)
        pixmap = QPixmap(
            get_absolute_path(__file__, f"../images/small/{self._item_variation_id}.jpg")
        )
        image_container.setPixmap(
            pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        self._title_btn.setText(self._item_model_name)
        add_class(self._title_btn, "catalog-item-price")
        self._title_btn.setCursor(Qt.PointingHandCursor)
        self._title_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

        desc = QLabel()
        desc.setText(
            f"{self._item_variation_name} • {self._item_size} • {self._item_amount} шт."
        )
        add_class(desc, "catalog-item-text")

        layout1 = QVBoxLayout()
        layout1.setContentsMargins(0, 7, 0, 0)
        layout1.setSpacing(0)
        layout1.addWidget(self._title_btn, alignment=Qt.AlignTop)
        layout1.addWidget(desc, alignment=Qt.AlignTop)

        layout.addWidget(image_container)
        layout.addLayout(layout1, 1)

        self.setLayout(layout)

    def _connect_signals(self):
        self._title_btn.clicked.connect(self._open_item_page)

    def _open_item_page(self):
        from ..windows import ItemWindow

        window = ItemWindow(self._item_model_id, self._item_variation_id)

        window.show()
