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

from ..widgets import ClickableWidget, OverlayWidget
from ..utils import get_absolute_path, add_class, format_price
from session import session

example = {
    "item_id": 10,
    "model": "Топовые тяги",
    "color": "Закат твтоей карьеры",
    "variation_id": 5,
    "size": "41",
    "amount": 1,
    "price": 1000,
}


class CartItemWidget(QWidget):
    def __init__(self, data=example, parent=None):
        super().__init__(parent)

        self._item_id = data["item_id"]
        self._item_model = data["model"]
        self._item_color = data["color"]
        self._item_variation = data["variation_id"]
        self._item_size = data["size"]
        self._item_amount = data["amount"]
        self._item_price = data["price"]

        self._title_btn = QPushButton()
        self._plus_btn = QPushButton()
        self._minus_btn = QPushButton()
        self._amount_label = QLabel()
        self._delete_btn = QPushButton()
        self._price_label = QLabel()
        
        self._overlay = OverlayWidget()

        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        self.setFixedSize(520, 150)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 20, 0)
        layout.setSpacing(20)

        image_container = QLabel()
        image_container.setFixedSize(150, 150)
        pixmap = QPixmap(get_absolute_path(__file__, "../images/item_placeholder.png"))
        image_container.setPixmap(
            pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        )

        self._title_btn.setText(self._item_model)
        add_class(self._title_btn, "catalog-item-price")
        self._title_btn.setCursor(Qt.PointingHandCursor)

        color = QLabel()
        color.setText(self._item_color)
        add_class(color, "catalog-item-text")

        size = QLabel()
        size.setText(f"Размер: {self._item_size}")
        add_class(size, "catalog-item-text")

        amount_input = QWidget()
        amount_input.setFixedSize(110, 32)

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

        amount_input.setLayout(amount_input_layout)

        layout1 = QVBoxLayout()
        layout1.setContentsMargins(0, 12, 0, 20)
        layout1.setSpacing(0)
        layout1.setAlignment(Qt.AlignLeft)
        layout1.addWidget(self._title_btn)
        layout1.addWidget(color)
        layout1.addWidget(size)
        layout1.addStretch(1)
        layout1.addWidget(amount_input)


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
        
        self._overlay.setParent(self)
        self._overlay.resize()

        self._update_ui()

    def _connect_signals(self):
        self._plus_btn.clicked.connect(self._plus_btn_handler)
        self._minus_btn.clicked.connect(self._minus_btn_handler)
        self._delete_btn.clicked.connect(self._delete_btn_handler)
        
    def _update_ui(self):
        new_price = self._item_amount * self._item_price
        self._price_label.setText(format_price(new_price, new_price))
        self._amount_label.setText(str(self._item_amount))
        self._update_btns()
    
    def _plus_btn_handler(self):
        self._item_amount += 1
        self._update_ui()
        # !!!
        # Отправляем запрос
        # !!!
        
    def _minus_btn_handler(self):
        self._item_amount -= 1
        self._update_ui()
        # !!!
        # Отправляем запрос
        # !!!
    
    def _delete_btn_handler(self):
        self._overlay.show()

    def _update_btns(self):
        if self._item_amount == 1:
            self._minus_btn.setDisabled(True)
            self._minus_btn.setIcon(QIcon(get_absolute_path(__file__, "../icons/minus_grey.png")))
        elif self._item_amount == 10:
            self._plus_btn.setDisabled(True)
            self._plus_btn.setIcon(QIcon(get_absolute_path(__file__, "../icons/plus_grey.png")))
        else:
            self._minus_btn.setDisabled(False)
            self._minus_btn.setIcon(QIcon(get_absolute_path(__file__, "../icons/minus.png")))
            self._plus_btn.setDisabled(False)
            self._plus_btn.setIcon(QIcon(get_absolute_path(__file__, "../icons/plus.png")))