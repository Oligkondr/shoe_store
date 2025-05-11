from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import Qt

from ..utils import add_class


class ShoeSizeBtnWidget(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Для внешних операций
        self.product_size_id = None

        self.setCheckable(True)
        self.setFixedSize(60, 32)
        add_class(self, "shoe-size-btn")
        self.setCursor(Qt.PointingHandCursor)
