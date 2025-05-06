from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QSize, QTimer, QByteArray, QUrl
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply

from enum import Enum
import requests
import json

from session import session

from ..utils import (
    get_absolute_path,
    add_class,
    remove_class,
    toggle_class,
    validate_login_email,
    validate_login_password,
    show_error_window,
)
from ..widgets import ClickableWidget, OverlayWidget


class LoginFormLayout(QVBoxLayout):
    class _InputName(Enum):
        EMAIL = 1
        PASSWORD = 2

    def __init__(self, parent_window):
        super().__init__()

        self._parent_window = parent_window

        self._inputs = dict()
        self._errors = dict()
        self._inputs_validity = dict()

        for input_name in self._InputName:
            self._inputs[input_name] = QLineEdit()
            self._errors[input_name] = QLabel()
            self._inputs_validity[input_name] = None

        self._validators = {
            self._InputName.EMAIL: validate_login_email,
            self._InputName.PASSWORD: validate_login_password,
        }

        self._register_btn = QPushButton()

        self._password_toggle_btn = QPushButton()
        self._password_toggle_btn.setCheckable(True)

        self._login_error = QLabel()
        self._login_btn = QPushButton()
        self._employee_login_btn = QPushButton()

        self._init_ui()
        self._connect_signals()
        
        if session.login_email is not None:
            self._inputs[self._InputName.EMAIL].setText(session.login_email)

    def _init_ui(self):
        self.setSpacing(0)
        self.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Вход")
        add_class(title, "title-text")

        label = QLabel("Ещё не зарегистрированы?")
        add_class(label, "small-text")

        self._register_btn.setText("Создать аккаунт")
        self._register_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        add_class(self._register_btn, "small-btn")
        self._register_btn.setCursor(Qt.PointingHandCursor)

        register_btn_icon = QLabel(" →")
        register_btn_icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        register_btn_icon.setContentsMargins(0, 0, 0, 1)
        add_class(register_btn_icon, "small-text")

        register_btn_layout = QHBoxLayout()
        register_btn_layout.addWidget(self._register_btn)
        register_btn_layout.addWidget(register_btn_icon)
        register_btn_layout.addStretch(1)

        for input_name in self._InputName:
            add_class(self._inputs[input_name], "text-input")
            self._inputs[input_name].setFixedHeight(30)

            add_class(self._errors[input_name], "error-text")
            self._errors[input_name].setContentsMargins(0, 2, 0, 0)
            self._errors[input_name].setWordWrap(True)
            self._errors[input_name].hide()

        self._inputs[self._InputName.EMAIL].setPlaceholderText("Email")
        self._inputs[self._InputName.PASSWORD].setPlaceholderText("Пароль")
        self._inputs[self._InputName.PASSWORD].setEchoMode(QLineEdit.Password)

        self._password_toggle_btn.setFixedHeight(30)
        self._password_toggle_btn.setFixedWidth(30)
        self._password_toggle_btn.setCursor(Qt.PointingHandCursor)
        self._password_toggle_btn.setIcon(
            QIcon(get_absolute_path(__file__, "../icons/password_closed.png"))
        )
        self._password_toggle_btn.setIconSize(QSize(20, 20))
        add_class(self._password_toggle_btn, "password-btn")
        self._password_toggle_btn.setStyleSheet("text-align: right")

        password_layout = QHBoxLayout()
        password_layout.addWidget(self._inputs[self._InputName.PASSWORD])
        password_layout.addWidget(self._password_toggle_btn)

        add_class(self._login_error, "error-text")
        self._login_error.setContentsMargins(0, 0, 0, 7)
        self._login_error.setWordWrap(True)
        self._login_error.hide()

        self._login_btn.setText("Войти")
        add_class(self._login_btn, "main-btn", "main-btn_solid")
        self._login_btn.setFixedHeight(40)
        self._login_btn.setContentsMargins(8, -1, 8, 0)
        self._login_btn.setCursor(Qt.PointingHandCursor)
        self._login_btn.setDisabled(True)

        self._employee_login_btn.setText("Войти как сотрудник")
        self._employee_login_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        add_class(self._employee_login_btn, "small-btn")
        self._employee_login_btn.setCursor(Qt.PointingHandCursor)
        self._employee_login_btn.setDisabled(True)

        self.addWidget(title)
        self.addSpacing(8)
        self.addWidget(label)
        self.addLayout(register_btn_layout)
        self.addSpacing(16)
        self.addWidget(self._inputs[self._InputName.EMAIL])
        self.addWidget(self._errors[self._InputName.EMAIL])
        self.addSpacing(10)
        self.addLayout(password_layout)
        self.addWidget(self._errors[self._InputName.PASSWORD])
        self.addSpacing(30)
        self.addWidget(self._login_error, alignment=Qt.AlignHCenter)
        self.addWidget(self._login_btn)
        # self.addSpacing(6)
        # self.addWidget(self._employee_login_btn, alignment=Qt.AlignHCenter)

    def _connect_signals(self):
        self._inputs[self._InputName.EMAIL].textChanged.connect(
            self._email_input_handler
        )
        self._inputs[self._InputName.PASSWORD].textChanged.connect(
            self._password_input_handler
        )

        self._password_toggle_btn.clicked.connect(self._toggle_password_visibility)

        self._login_btn.clicked.connect(self._login_btn_handler)
        self._employee_login_btn.clicked.connect(self._login_btn_handler)

        self._register_btn.clicked.connect(self._parent_window.show_registration_form)

    def _email_input_handler(self):
        self._validate_input(self._InputName.EMAIL)
        self._set_login_buttons_disability()

    def _password_input_handler(self):
        self._validate_input(self._InputName.PASSWORD)
        self._set_login_buttons_disability()

    def _login_btn_handler(self):
        self._login_error.hide()
        self._parent_window.show_overlay()

        url = "http://127.0.0.1:8000/api/v1/login"
        data = {
            "email": self._inputs[self._InputName.EMAIL].text(),
            "password": self._inputs[self._InputName.PASSWORD].text(),
        }
        data_json = json.dumps(data)

        try:
            response = requests.post(url, data=data_json)

            if response.status_code == 200:
                data = json.loads(response.text)
                session.token = data["token"]
                self._parent_window.show_main_window()
            elif response.status_code == 401:
                data = json.loads(response.text)
                self._show_login_error(data["detail"])
                self._parent_window.hide_overlay()
            else:
                show_error_window()
                self._parent_window.hide_overlay()
        except Exception as error:
            print(error)
            show_error_window()
            self._parent_window.hide_overlay()

    def _show_login_error(self, error_text):
        self._parent_window.hide_overlay()
        self._login_error.setText(error_text)
        self._login_error.show()

    def _validate_input(self, input_name):
        text = self._inputs[input_name].text()
        validation_result = self._validators[input_name](text)
        self._inputs_validity[input_name] = validation_result.is_valid

        if self._inputs_validity[input_name]:
            self._errors[input_name].hide()
        else:
            self._errors[input_name].setText(validation_result.message)
            self._errors[input_name].show()

    def _toggle_password_visibility(self):
        if self._password_toggle_btn.isChecked():
            self._password_toggle_btn.setIcon(
                QIcon(get_absolute_path(__file__, "../icons/password_opened.png"))
            )
            self._inputs[self._InputName.PASSWORD].setEchoMode(QLineEdit.Normal)
        else:
            self._password_toggle_btn.setIcon(
                QIcon(get_absolute_path(__file__, "../icons/password_closed.png"))
            )
            self._inputs[self._InputName.PASSWORD].setEchoMode(QLineEdit.Password)

    def _set_login_buttons_disability(self):
        self._login_error.hide()
        form_validity = all(self._inputs_validity.values())
        self._login_btn.setDisabled(not form_validity)
        self._employee_login_btn.setDisabled(not form_validity)
