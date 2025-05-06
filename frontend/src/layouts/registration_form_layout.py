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
import requests
import json
from session import session

from ..utils import (
    get_absolute_path,
    add_class,
    remove_class,
    toggle_class,
    show_error_window,
    validate_registration_email,
    validate_registration_name,
    validate_registration_surname,
    validate_registration_phone,
    validate_registration_password,
    validate_registration_password2,
)
from ..widgets import ClickableWidget, OverlayWidget, PhoneInputWidget
from ..classes import RequestThread


class RegistrationFormLayout(QVBoxLayout):
    class _InputName(Enum):
        EMAIL = 1
        NAME = 2
        SURNAME = 3
        PHONE = 4
        PASSWORD = 5
        PASSWORD2 = 6

    def __init__(self, parent_window):
        super().__init__()

        self._parent_window = parent_window

        self._inputs = dict()
        self._errors = dict()
        self._inputs_validity = dict()
        self._toggle_btns = dict()

        for input_name in self._InputName:
            self._inputs[input_name] = QLineEdit()
            self._errors[input_name] = QLabel()
            self._inputs_validity[input_name] = None
        self._inputs[self._InputName.PHONE] = PhoneInputWidget()

        for input_name in [self._InputName.PASSWORD, self._InputName.PASSWORD2]:
            self._toggle_btns[input_name] = QPushButton()
            self._toggle_btns[input_name].setCheckable(True)

        self._validators = {
            self._InputName.EMAIL: validate_registration_email,
            self._InputName.NAME: validate_registration_name,
            self._InputName.SURNAME: validate_registration_surname,
            self._InputName.PHONE: validate_registration_phone,
            self._InputName.PASSWORD: validate_registration_password,
            self._InputName.PASSWORD2: validate_registration_password2,
        }

        self._back_btn = QPushButton()

        self._password_toggle_btn = QPushButton()
        self._password_toggle_btn.setCheckable(True)

        self._password2_toggle_btn = QPushButton()
        self._password2_toggle_btn.setCheckable(True)

        self._register_error = QLabel()
        self._register_btn = QPushButton()

        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        self.setSpacing(0)
        self.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Регистрация")
        add_class(title, "title-text")

        self._back_btn.setText("Вернуться")
        self._back_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        add_class(self._back_btn, "small-btn")
        self._back_btn.setCursor(Qt.PointingHandCursor)

        back_btn_icon = QLabel("← ")
        back_btn_icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        back_btn_icon.setContentsMargins(0, 0, 0, 1)
        add_class(back_btn_icon, "small-text")

        back_btn_layout = QHBoxLayout()
        back_btn_layout.addWidget(back_btn_icon)
        back_btn_layout.addWidget(self._back_btn)
        back_btn_layout.addStretch(1)

        for input_name in self._InputName:
            add_class(self._inputs[input_name], "text-input")
            self._inputs[input_name].setFixedHeight(30)

            add_class(self._errors[input_name], "error-text")
            self._errors[input_name].setContentsMargins(0, 2, 0, 0)
            self._errors[input_name].setWordWrap(True)
            self._errors[input_name].hide()

        self._inputs[self._InputName.EMAIL].setPlaceholderText("Email")
        self._inputs[self._InputName.NAME].setPlaceholderText("Имя")
        self._inputs[self._InputName.SURNAME].setPlaceholderText("Фамилия")
        self._inputs[self._InputName.PHONE].setPlaceholderText("Телефон")
        self._inputs[self._InputName.PASSWORD].setPlaceholderText("Пароль")
        self._inputs[self._InputName.PASSWORD2].setPlaceholderText("Подтвердите пароль")

        self._inputs[self._InputName.PASSWORD].setEchoMode(QLineEdit.Password)
        self._inputs[self._InputName.PASSWORD2].setEchoMode(QLineEdit.Password)

        for input_name in [self._InputName.PASSWORD, self._InputName.PASSWORD2]:
            self._toggle_btns[input_name].setFixedHeight(30)
            self._toggle_btns[input_name].setFixedWidth(30)
            self._toggle_btns[input_name].setCursor(Qt.PointingHandCursor)
            self._toggle_btns[input_name].setIcon(
                QIcon(get_absolute_path(__file__, "../icons/password_closed.png"))
            )
            self._toggle_btns[input_name].setIconSize(QSize(20, 20))
            add_class(self._toggle_btns[input_name], "password-btn")
            self._toggle_btns[input_name].setStyleSheet("text-align: right")

        password_layout = QHBoxLayout()
        password_layout.addWidget(self._inputs[self._InputName.PASSWORD])
        password_layout.addWidget(self._toggle_btns[self._InputName.PASSWORD])

        password2_layout = QHBoxLayout()
        password2_layout.addWidget(self._inputs[self._InputName.PASSWORD2])
        password2_layout.addWidget(self._toggle_btns[self._InputName.PASSWORD2])

        add_class(self._register_error, "error-text", "error-text_above")
        self._register_error.setContentsMargins(0, 0, 0, 7)
        self._register_error.setWordWrap(True)
        self._register_error.hide()

        self._register_btn.setText("Зарегистрироваться")
        add_class(self._register_btn, "main-btn", "main-btn_solid")
        self._register_btn.setFixedHeight(40)
        self._register_btn.setContentsMargins(8, -1, 8, 0)
        self._register_btn.setCursor(Qt.PointingHandCursor)
        self._register_btn.setDisabled(True)

        self.addWidget(title)
        self.addLayout(back_btn_layout)
        self.addSpacing(16)
        for input_name in [
            self._InputName.EMAIL,
            self._InputName.NAME,
            self._InputName.SURNAME,
            self._InputName.PHONE,
        ]:
            self.addWidget(self._inputs[input_name])
            self.addWidget(self._errors[input_name])
            self.addSpacing(10)
        self.addLayout(password_layout)
        self.addWidget(self._errors[self._InputName.PASSWORD])
        self.addSpacing(10)
        self.addLayout(password2_layout)
        self.addWidget(self._errors[self._InputName.PASSWORD2])
        self.addSpacing(30)
        self.addWidget(self._register_error, alignment=Qt.AlignHCenter)
        self.addWidget(self._register_btn)

    def _connect_signals(self):
        self._back_btn.clicked.connect(self._parent_window.show_login_form)

        self._inputs[self._InputName.EMAIL].textChanged.connect(
            self._email_input_handler
        )
        self._inputs[self._InputName.NAME].textChanged.connect(self._name_input_handler)
        self._inputs[self._InputName.SURNAME].textChanged.connect(
            self._surname_input_handler
        )
        self._inputs[self._InputName.PHONE].textChanged.connect(
            self._phone_input_handler
        )
        self._inputs[self._InputName.PASSWORD].textChanged.connect(
            self._password_input_handler
        )
        self._inputs[self._InputName.PASSWORD2].textChanged.connect(
            self._password2_input_handler
        )

        self._toggle_btns[self._InputName.PASSWORD].clicked.connect(
            self._password_toggle_btn_handler
        )
        self._toggle_btns[self._InputName.PASSWORD2].clicked.connect(
            self._password2_toggle_btn_handler
        )

        self._register_btn.clicked.connect(self._register_btn_handler)

    def _email_input_handler(self):
        self._validate_input(self._InputName.EMAIL)
        self._set_register_button_disability()

    def _name_input_handler(self):
        self._validate_input(self._InputName.NAME)
        self._set_register_button_disability()

    def _surname_input_handler(self):
        self._validate_input(self._InputName.SURNAME)
        self._set_register_button_disability()

    def _phone_input_handler(self):
        self._validate_input(self._InputName.PHONE)
        self._set_register_button_disability()

    def _password_input_handler(self):
        self._validate_input(self._InputName.PASSWORD)
        if len(self._inputs[self._InputName.PASSWORD2].text()) > 0:
            self._password2_input_handler()
        else:
            self._set_register_button_disability()

    def _password2_input_handler(self):
        self._validate_input(self._InputName.PASSWORD2)

        if self._inputs_validity[self._InputName.PASSWORD2]:
            self._inputs_validity[self._InputName.PASSWORD2] = (
                self._inputs[self._InputName.PASSWORD].text()
                == self._inputs[self._InputName.PASSWORD2].text()
            )
            if self._inputs_validity[self._InputName.PASSWORD2]:
                self._errors[self._InputName.PASSWORD2].hide()
            else:
                self._errors[self._InputName.PASSWORD2].setText(
                    "Пароли должны совпадать"
                )
                self._errors[self._InputName.PASSWORD2].show()

        self._set_register_button_disability()

    def _register_btn_handler(self):
        self._register_error.hide()
        self._parent_window.show_overlay()

        url = "http://127.0.0.1:8000/api/v1/register"
        data = {
            "email": self._inputs[self._InputName.EMAIL].text().strip(),
            "password": self._inputs[self._InputName.PASSWORD].text(),
            "phone": self._inputs[self._InputName.PHONE].text()[1:],
            "name": self._inputs[self._InputName.NAME].text().strip(),
            "surname": self._inputs[self._InputName.SURNAME].text().strip(),
        }
        data_json = json.dumps(data)

        thread = session.new_thread(
            RequestThread(method="POST", url=url, data=data_json)
        )
        thread.finished.connect(self._handle_registration_response)
        thread.start()

    def _handle_registration_response(self, response, thread):
        session.delete_thread(thread)

        if isinstance(response, Exception):
            print(response)
            show_error_window()
        else:
            data = json.loads(response.text)
            if response.status_code == 200:
                session.login_email = data["email"]
                session.registration_name = data["name"]
                self._parent_window.show_success_registration_message()
            elif response.status_code == 401:
                self._show_register_error(data["detail"])
            else:
                show_error_window()

        self._parent_window.hide_overlay()

    def _show_register_error(self, error_text):
        self._register_error.setText(error_text)
        self._register_error.show()

    def _validate_input(self, input_name):
        text = self._inputs[input_name].text()
        validation_result = self._validators[input_name](text)
        self._inputs_validity[input_name] = validation_result.is_valid

        if self._inputs_validity[input_name]:
            self._errors[input_name].hide()
        else:
            self._errors[input_name].setText(validation_result.message)
            self._errors[input_name].show()

    def _password_toggle_btn_handler(self):
        self._toggle_password_visibility(self._InputName.PASSWORD)

    def _password2_toggle_btn_handler(self):
        self._toggle_password_visibility(self._InputName.PASSWORD2)

    def _toggle_password_visibility(self, input_name):
        if self._toggle_btns[input_name].isChecked():
            self._toggle_btns[input_name].setIcon(
                QIcon(get_absolute_path(__file__, "../icons/password_opened.png"))
            )
            self._inputs[input_name].setEchoMode(QLineEdit.Normal)
        else:
            self._toggle_btns[input_name].setIcon(
                QIcon(get_absolute_path(__file__, "../icons/password_closed.png"))
            )
            self._inputs[input_name].setEchoMode(QLineEdit.Password)

    def _set_register_button_disability(self):
        self._register_error.hide()
        form_validity = all(self._inputs_validity.values())
        self._register_btn.setDisabled(not form_validity)
