from PyQt5.QtWidgets import QLineEdit
import re


class PhoneInputWidget(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.textChanged.connect(self._on_text_changed)

    # Перезапись поведения получения введённого текста из виджета
    # Возваращает только введённые цифры, а не весь отформатированный текст
    def text(self):
        original_text = super().text()
        digits_str = re.sub(r"\D", "", original_text)
        return digits_str

    def focusInEvent(self, event):
        if len(self.text()) == 0:
            self.setText("7")
        super().focusInEvent(event)

    # Перезапись поведения при вводе текста
    def _on_text_changed(self):
        # Запрет на ввод больше, чем 11 цифр
        # Проверка на цифры происходит в перезаписанном методе .text()
        digits_str = self.text()[:11]

        formatted_text = "+7"

        if len(digits_str) >= 2:
            formatted_text += " (" + digits_str[1:4]
        if len(digits_str) >= 5:
            formatted_text += ") " + digits_str[4:7]
        if len(digits_str) >= 8:
            formatted_text += "-" + digits_str[7:9]
        if len(digits_str) >= 10:
            formatted_text += "-" + digits_str[9:]

        # Отключение сигналов, чтобы не вызвать переформатирование
        self.blockSignals(True)
        self.setText(formatted_text)
        self.blockSignals(False)
