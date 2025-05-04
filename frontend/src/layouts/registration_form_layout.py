from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QIcon

from enum import Enum

from ..utils import (
    get_absolute_path,
    add_class,
    remove_class,
    toggle_class,
    validate_registration_email,
    validate_registration_name,
    validate_registration_surname,
    validate_registration_phone,
    validate_registration_password,
    validate_registration_password2,
)
from ..widgets import ClickableWidget, OverlayWidget, PhoneInputWidget


class RegistrationFormLayout(QVBoxLayout):
    class InputName(Enum):
        EMAIL = 1
        NAME = 2
        SURNAME = 3
        PHONE = 4
        PASSWORD = 5
        PASSWORD2 = 6

    def __init__(
        self,
        success_registration_handler,
        back_btn_handler,
        show_window_overlay,
        hide_window_overlay,
    ):
        super().__init__()

        self.success_registration_handler = success_registration_handler
        self.back_btn_handler = back_btn_handler
        self.show_window_overlay = show_window_overlay
        self.hide_window_overlay = hide_window_overlay

        self.inputs = dict()
        self.errors = dict()
        self.inputs_validity = dict()
        self.toggle_btns = dict()

        for input_name in self.InputName:
            self.inputs[input_name] = QLineEdit()
            self.errors[input_name] = QLabel()
            self.inputs_validity[input_name] = None
        self.inputs[self.InputName.PHONE] = PhoneInputWidget()

        for input_name in [self.InputName.PASSWORD, self.InputName.PASSWORD2]:
            self.toggle_btns[input_name] = QPushButton()
            self.toggle_btns[input_name].setCheckable(True)

        self.validators = {
            self.InputName.EMAIL: validate_registration_email,
            self.InputName.NAME: validate_registration_name,
            self.InputName.SURNAME: validate_registration_surname,
            self.InputName.PHONE: validate_registration_phone,
            self.InputName.PASSWORD: validate_registration_password,
            self.InputName.PASSWORD2: validate_registration_password2,
        }

        self.back_btn = QPushButton()

        self.password_toggle_btn = QPushButton()
        self.password_toggle_btn.setCheckable(True)

        self.password2_toggle_btn = QPushButton()
        self.password2_toggle_btn.setCheckable(True)

        self.register_error = QLabel()
        self.register_btn = QPushButton()

        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        self.setSpacing(0)
        self.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Регистрация")
        add_class(title, "title-text")

        self.back_btn.setText("Вернуться")
        self.back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        add_class(self.back_btn, "small-btn")
        self.back_btn.setCursor(Qt.PointingHandCursor)

        back_btn_icon = QLabel("← ")
        back_btn_icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        back_btn_icon.setContentsMargins(0, 0, 0, 1)
        add_class(back_btn_icon, "small-text")

        back_btn_layout = QHBoxLayout()
        back_btn_layout.addWidget(back_btn_icon)
        back_btn_layout.addWidget(self.back_btn)
        back_btn_layout.addStretch(1)

        for input_name in self.InputName:
            add_class(self.inputs[input_name], "text-input")
            self.inputs[input_name].setFixedHeight(30)

            add_class(self.errors[input_name], "error-text")
            self.errors[input_name].setContentsMargins(0, 2, 0, 0)
            self.errors[input_name].hide()

        self.inputs[self.InputName.EMAIL].setPlaceholderText("Email")
        self.inputs[self.InputName.NAME].setPlaceholderText("Имя")
        self.inputs[self.InputName.SURNAME].setPlaceholderText("Фамилия")
        self.inputs[self.InputName.PHONE].setPlaceholderText("Телефон")
        self.inputs[self.InputName.PASSWORD].setPlaceholderText("Пароль")
        self.inputs[self.InputName.PASSWORD2].setPlaceholderText("Подтвердите пароль")

        self.inputs[self.InputName.PASSWORD].setEchoMode(QLineEdit.Password)
        self.inputs[self.InputName.PASSWORD2].setEchoMode(QLineEdit.Password)

        for input_name in [self.InputName.PASSWORD, self.InputName.PASSWORD2]:
            self.toggle_btns[input_name].setFixedHeight(30)
            self.toggle_btns[input_name].setFixedWidth(30)
            self.toggle_btns[input_name].setCursor(Qt.PointingHandCursor)
            self.toggle_btns[input_name].setIcon(
                QIcon(get_absolute_path(__file__, "../icons/password_closed.png"))
            )
            self.toggle_btns[input_name].setIconSize(QSize(20, 20))
            add_class(self.toggle_btns[input_name], "password-btn")
            self.toggle_btns[input_name].setStyleSheet("text-align: right")

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.inputs[self.InputName.PASSWORD])
        password_layout.addWidget(self.toggle_btns[self.InputName.PASSWORD])

        password2_layout = QHBoxLayout()
        password2_layout.addWidget(self.inputs[self.InputName.PASSWORD2])
        password2_layout.addWidget(self.toggle_btns[self.InputName.PASSWORD2])

        add_class(self.register_error, "error-text", "error-text_above")
        self.register_error.setContentsMargins(0, 0, 0, 7)
        self.register_error.hide()

        self.register_btn.setText("Зарегистрироваться")
        add_class(self.register_btn, "main-btn", "main-btn_solid")
        self.register_btn.setFixedHeight(40)
        self.register_btn.setContentsMargins(8, -1, 8, 0)
        self.register_btn.setCursor(Qt.PointingHandCursor)
        self.register_btn.setDisabled(True)

        self.addWidget(title)
        self.addLayout(back_btn_layout)
        self.addSpacing(16)
        for input_name in [
            self.InputName.EMAIL,
            self.InputName.NAME,
            self.InputName.SURNAME,
            self.InputName.PHONE,
        ]:
            self.addWidget(self.inputs[input_name])
            self.addWidget(self.errors[input_name])
            self.addSpacing(10)
        self.addLayout(password_layout)
        self.addWidget(self.errors[self.InputName.PASSWORD])
        self.addSpacing(10)
        self.addLayout(password2_layout)
        self.addWidget(self.errors[self.InputName.PASSWORD2])
        self.addSpacing(30)
        self.addWidget(self.register_error, alignment=Qt.AlignHCenter)
        self.addWidget(self.register_btn)

    def connect_signals(self):
        self.back_btn.clicked.connect(self.back_btn_handler)

        self.inputs[self.InputName.EMAIL].textChanged.connect(self.email_input_handler)
        self.inputs[self.InputName.NAME].textChanged.connect(self.name_input_handler)
        self.inputs[self.InputName.SURNAME].textChanged.connect(
            self.surname_input_handler
        )
        self.inputs[self.InputName.PHONE].textChanged.connect(self.phone_input_handler)
        self.inputs[self.InputName.PASSWORD].textChanged.connect(
            self.password_input_handler
        )
        self.inputs[self.InputName.PASSWORD2].textChanged.connect(
            self.password2_input_handler
        )

        self.toggle_btns[self.InputName.PASSWORD].clicked.connect(
            self.password_toggle_btn_handler
        )
        self.toggle_btns[self.InputName.PASSWORD2].clicked.connect(
            self.password2_toggle_btn_handler
        )

        self.register_btn.clicked.connect(self.register_btn_handler)

    def email_input_handler(self):
        self.validate_input(self.InputName.EMAIL)
        self.set_register_button_disability()

    def name_input_handler(self):
        self.validate_input(self.InputName.NAME)
        self.set_register_button_disability()

    def surname_input_handler(self):
        self.validate_input(self.InputName.SURNAME)
        self.set_register_button_disability()

    def phone_input_handler(self):
        self.validate_input(self.InputName.PHONE)
        self.set_register_button_disability()

    def password_input_handler(self):
        self.validate_input(self.InputName.PASSWORD)
        if len(self.inputs[self.InputName.PASSWORD2].text()) > 0:
            self.password2_input_handler()
        else:
            self.set_register_button_disability()

    def password2_input_handler(self):
        self.validate_input(self.InputName.PASSWORD2)

        if self.inputs_validity[self.InputName.PASSWORD2]:
            self.inputs_validity[self.InputName.PASSWORD2] = (
                self.inputs[self.InputName.PASSWORD].text()
                == self.inputs[self.InputName.PASSWORD2].text()
            )
            if self.inputs_validity[self.InputName.PASSWORD2]:
                self.errors[self.InputName.PASSWORD2].hide()
            else:
                self.errors[self.InputName.PASSWORD2].setText("Пароли должны совпадать")
                self.errors[self.InputName.PASSWORD2].show()

        self.set_register_button_disability()

    def register_btn_handler(self):
        self.register_error.hide()
        self.show_window_overlay()
        QTimer.singleShot(1000, self.show_register_error)

    def show_register_error(self):
        self.hide_window_overlay()
        self.register_error.setText("Что-то пошло не так")
        self.register_error.show()

    def validate_input(self, input_name):
        text = self.inputs[input_name].text()
        validation_result = self.validators[input_name](text)
        self.inputs_validity[input_name] = validation_result.is_valid

        if self.inputs_validity[input_name]:
            self.errors[input_name].hide()
        else:
            self.errors[input_name].setText(validation_result.message)
            self.errors[input_name].show()

    def password_toggle_btn_handler(self):
        self.toggle_password_visibility(self.InputName.PASSWORD)

    def password2_toggle_btn_handler(self):
        self.toggle_password_visibility(self.InputName.PASSWORD2)

    def toggle_password_visibility(self, input_name):
        if self.toggle_btns[input_name].isChecked():
            self.toggle_btns[input_name].setIcon(
                QIcon(get_absolute_path(__file__, "../icons/password_opened.png"))
            )
            self.inputs[input_name].setEchoMode(QLineEdit.Normal)
        else:
            self.toggle_btns[input_name].setIcon(
                QIcon(get_absolute_path(__file__, "../icons/password_closed.png"))
            )
            self.inputs[input_name].setEchoMode(QLineEdit.Password)

    def set_register_button_disability(self):
        self.register_error.hide()
        form_validity = all(self.inputs_validity.values())
        self.register_btn.setDisabled(not form_validity)
