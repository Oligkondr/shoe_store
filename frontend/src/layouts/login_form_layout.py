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
    validate_login_email,
    validate_login_password,
)
from ..widgets import ClickableWidget, OverlayWidget


class LoginFormLayout(QVBoxLayout):
    class InputName(Enum):
        EMAIL = 1
        PASSWORD = 2

    def __init__(
        self,
        success_login_handler,
        show_register_form_handler,
        show_window_overlay,
        hide_window_overlay,
    ):
        super().__init__()

        self.success_login_handler = success_login_handler
        self.show_register_form_handler = show_register_form_handler
        self.show_window_overlay = show_window_overlay
        self.hide_window_overlay = hide_window_overlay

        self.inputs = dict()
        self.errors = dict()
        self.inputs_validity = dict()

        for input_name in self.InputName:
            self.inputs[input_name] = QLineEdit()
            self.errors[input_name] = QLabel()
            self.inputs_validity[input_name] = None

        self.validators = {
            self.InputName.EMAIL: validate_login_email,
            self.InputName.PASSWORD: validate_login_password,
        }

        self.register_btn = QPushButton()

        self.password_toggle_btn = QPushButton()
        self.password_toggle_btn.setCheckable(True)

        self.login_error = QLabel()
        self.login_btn = QPushButton()
        self.employee_login_btn = QPushButton()

        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        self.setSpacing(0)
        self.setContentsMargins(30, 30, 30, 30)

        title = QLabel("Вход")
        add_class(title, "title-text")

        label = QLabel("Ещё не зарегистрированы?")
        add_class(label, "small-text")

        self.register_btn.setText("Создать аккаунт")
        self.register_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        add_class(self.register_btn, "small-btn")
        self.register_btn.setCursor(Qt.PointingHandCursor)

        register_btn_icon = QLabel(" →")
        register_btn_icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        register_btn_icon.setContentsMargins(0, 0, 0, 1)
        add_class(register_btn_icon, "small-text")

        register_btn_layout = QHBoxLayout()
        register_btn_layout.addWidget(self.register_btn)
        register_btn_layout.addWidget(register_btn_icon)
        register_btn_layout.addStretch(1)

        for input_name in self.InputName:
            add_class(self.inputs[input_name], "text-input")
            self.inputs[input_name].setFixedHeight(30)

            add_class(self.errors[input_name], "error-text")
            self.errors[input_name].setContentsMargins(0, 2, 0, 0)
            self.errors[input_name].hide()

        self.inputs[self.InputName.EMAIL].setPlaceholderText("Email")
        self.inputs[self.InputName.PASSWORD].setPlaceholderText("Пароль")
        self.inputs[self.InputName.PASSWORD].setEchoMode(QLineEdit.Password)

        self.password_toggle_btn.setFixedHeight(30)
        self.password_toggle_btn.setFixedWidth(30)
        self.password_toggle_btn.setCursor(Qt.PointingHandCursor)
        self.password_toggle_btn.setIcon(
            QIcon(get_absolute_path(__file__, "../icons/password_closed.png"))
        )
        self.password_toggle_btn.setIconSize(QSize(20, 20))
        add_class(self.password_toggle_btn, "password-btn")
        self.password_toggle_btn.setStyleSheet("text-align: right")

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.inputs[self.InputName.PASSWORD])
        password_layout.addWidget(self.password_toggle_btn)

        add_class(self.login_error, "error-text")
        self.login_error.setContentsMargins(0, 0, 0, 7)
        self.login_error.hide()

        self.login_btn.setText("Войти")
        add_class(self.login_btn, "main-btn", "main-btn_solid")
        self.login_btn.setFixedHeight(40)
        self.login_btn.setContentsMargins(8, -1, 8, 0)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setDisabled(True)

        self.employee_login_btn.setText("Войти как сотрудник")
        self.employee_login_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        add_class(self.employee_login_btn, "small-btn")
        self.employee_login_btn.setCursor(Qt.PointingHandCursor)
        self.employee_login_btn.setDisabled(True)

        self.addWidget(title)
        self.addSpacing(8)
        self.addWidget(label)
        self.addLayout(register_btn_layout)
        self.addSpacing(16)
        self.addWidget(self.inputs[self.InputName.EMAIL])
        self.addWidget(self.errors[self.InputName.EMAIL])
        self.addSpacing(10)
        self.addLayout(password_layout)
        self.addWidget(self.errors[self.InputName.PASSWORD])
        self.addSpacing(30)
        self.addWidget(self.login_error, alignment=Qt.AlignHCenter)
        self.addWidget(self.login_btn)
        self.addSpacing(6)
        self.addWidget(self.employee_login_btn, alignment=Qt.AlignHCenter)

    def connect_signals(self):
        self.inputs[self.InputName.EMAIL].textChanged.connect(self.email_input_handler)
        self.inputs[self.InputName.PASSWORD].textChanged.connect(
            self.password_input_handler
        )

        self.password_toggle_btn.clicked.connect(self.toggle_password_visibility)

        self.login_btn.clicked.connect(self.login_btn_handler)
        self.employee_login_btn.clicked.connect(self.login_btn_handler)

        self.register_btn.clicked.connect(self.show_register_form_handler)

    def email_input_handler(self):
        self.validate_input(self.InputName.EMAIL)
        self.set_login_buttons_disability()

    def password_input_handler(self):
        self.validate_input(self.InputName.PASSWORD)
        self.set_login_buttons_disability()

    def login_btn_handler(self):
        self.login_error.hide()
        self.show_window_overlay()
        QTimer.singleShot(1000, self.show_login_error)

    def show_login_error(self):
        self.hide_window_overlay()
        self.login_error.setText("Неверный логин или пароль")
        self.login_error.show()

    def validate_input(self, input_name):
        text = self.inputs[input_name].text()
        validation_result = self.validators[input_name](text)
        self.inputs_validity[input_name] = validation_result.is_valid

        if self.inputs_validity[input_name]:
            self.errors[input_name].hide()
        else:
            self.errors[input_name].setText(validation_result.message)
            self.errors[input_name].show()

    def toggle_password_visibility(self):
        if self.password_toggle_btn.isChecked():
            self.password_toggle_btn.setIcon(
                QIcon(get_absolute_path(__file__, "../icons/password_opened.png"))
            )
            self.inputs[self.InputName.PASSWORD].setEchoMode(QLineEdit.Normal)
        else:
            self.password_toggle_btn.setIcon(
                QIcon(get_absolute_path(__file__, "../icons/password_closed.png"))
            )
            self.inputs[self.InputName.PASSWORD].setEchoMode(QLineEdit.Password)

    def set_login_buttons_disability(self):
        self.login_error.hide()
        form_validity = all(self.inputs_validity.values())
        self.login_btn.setDisabled(not form_validity)
        self.employee_login_btn.setDisabled(not form_validity)
