from PyQt5.QtWidgets import QLabel
from ..widgets import ClickableWidget


class ModelVariationBtnWidget(ClickableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Для внешних операций
        self.variation_id = None
        
        self.setFixedSize(60, 60)

        self.image = QLabel(self)
        self.image.setFixedSize(60, 60)

