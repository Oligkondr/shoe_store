from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout
import re


class AmountInputWidget(QWidget):
    def __init__(self, parent=None, **params):
        super().__init__(parent)

        # Не делаем приватными, поскольку вешаем дополнительные события снаружи
        self._min_value = params.get("min")
        self._max_value = params.get("max")

        self.input = QLineEdit()
        self.plus_btn = QPushButton()
        self.minus_btn = QPushButton()

        self._unit_ui()
        self._connect_signals()

    def _init_ui(self):
        layout = QHBoxLayout()

        self.plus_btn.setText("+")
        self.plus_btn.setFixedWidth(15)

        self.minus_btn.setText("-")
        self.minus_btn.setFixedWidth(15)

        layout.addWidget(self.minus_btn)
        layout.addWidget(self.input, 1)
        layout.addWidget(self.plus_btn)

        self.setLayout(layout)

    def _connect_signals(self):
        pass

    def _input_handler(self):
        digits_str = re.sub(r"\D", "", self._input.text())
        int_value = int(digits_str)
