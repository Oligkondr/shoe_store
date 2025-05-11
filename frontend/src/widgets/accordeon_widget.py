from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize

from ..widgets import ClickableWidget
from ..utils import get_absolute_path, add_class
from session import session

example = {
    "title": "Заказ #2222",
    "decription": "1 000 Р",
}

class AccordeonWidget(QWidget):
    def __init__(self, header_data, body_widget):
        super().__init__
        
        self._is_opened = False
        
        self._body = body_widget
        
        self.setFixedWidth(500)
        
        title = QLabel()
        title.setText(header_data["title"])
        add_class(title, "title-text")
        
        desc = QLabel()
        desc.setText(header_data["description"])
        add_class(desc, "small-text")
        
        header_text_layout = QVBoxLayout()
        header_text_layout.setContentsMargins(0,0,0,0)
        header_text_layout.setSpacing(0)
        header_text_layout.setAlignment(Qt.AlignLeft)
        
        header_text = QWidget()
        header_text.setLayout(header_text_layout)
        
        self._arrow_icon = QPushButton()
        self._arrow_icon.setFixedSize(20, 20)
        self._arrow_icon.setIcon(
            QIcon(get_absolute_path(__file__, "../icons/down.png"))
        )
        self._arrow_icon.setIconSize(QSize(20, 20))
        self._arrow_icon.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0,0,0,0)
        header_layout.setSpacing(0)
        header_layout.addWidget(header_text, 1)
        header_layout.addWidget(self._arrow_icon, alignment=Qt.AlignCenter)
        
        header_container = ClickableWidget()
        header_container.setLayout(header_layout)
        header_container.clicked.connect(self._toggle_content)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(header_container)
        layout.addWidget(self._body)
        
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