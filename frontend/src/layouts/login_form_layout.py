from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt

from ..utils import (
    add_class,
    remove_class,
    toggle_class,
    validate_login_email,
    validate_login_password,
)


class LoginFormLayout(QVBoxLayout):
    def __init__(self, success_login_handler, show_register_form_handler):
        super().__init__()

        self.inputs = {
            "email": QLineEdit(),
            "password": QLineEdit(),
        }
        for name, widget in self.inputs.items():
            widget.setObjectName(name)

        self.inputs_validity = {
            "email": None,
            "password": None,
        }
        self.validators = {
            "email": validate_login_email,
            "password": validate_login_password,
        }
        self.errors = {
            "email": QLabel(),
            "password": QLabel(),
        }

        self.success_registration_handler = success_login_handler
        self.show_register_form_handler = show_register_form_handler

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

        title = QLabel("Вход")
        add_class(title, "title-text")

        label = QLabel("Ещё не зарегистрированы?")
        add_class(label, "small-text")

        self.register_btn.setText("Создать аккаунт")
        self.register_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        add_class(self.register_btn, "small-btn")
        self.register_btn.setCursor(Qt.PointingHandCursor)

        self.inputs["email"].setPlaceholderText("Email")
        add_class(self.inputs["email"], "text-input")
        self.inputs["email"].setFixedHeight(30)

        add_class(self.errors["email"], "error-text")
        self.errors["email"].hide()

        self.inputs["password"].setPlaceholderText("Пароль")
        self.inputs["password"].setEchoMode(QLineEdit.Password)
        add_class(self.inputs["password"], "text-input")
        self.inputs["password"].setFixedHeight(30)

        self.password_toggle_btn.setFixedHeight(30)
        self.password_toggle_btn.setFixedWidth(30)
        add_class(self.password_toggle_btn, "password-btn")

        add_class(self.errors["password"], "error-text")
        self.errors["password"].hide()

        password_layout = QHBoxLayout()
        password_layout.addWidget(self.inputs["password"])
        password_layout.addWidget(self.password_toggle_btn)

        add_class(self.login_error, "error-text", "error-text_above")
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
        self.addWidget(self.register_btn)
        self.addSpacing(16)
        self.addWidget(self.inputs["email"])
        self.addWidget(self.errors["email"])
        self.addSpacing(10)
        self.addLayout(password_layout)
        self.addWidget(self.errors["password"])
        self.addSpacing(30)
        self.addWidget(self.login_error)
        self.addWidget(self.login_btn)
        self.addSpacing(6)
        self.addWidget(self.employee_login_btn, alignment=Qt.AlignHCenter)

    def connect_signals(self):
        for widget in self.inputs.values():
            widget.textChanged.connect(self.validate_input)
        self.password_toggle_btn.clicked.connect(self.toggle_password_visibility)
        self.register_btn.clicked.connect(self.show_register_form_handler)

    def validate_input(self):
        input_field = self.sender()
        text = input_field.text()
        field_name = input_field.objectName()
        validation_result = self.validators[field_name](text)

        if validation_result.is_valid:
            self.inputs_validity[field_name] = True
            self.errors[field_name].hide()
        else:
            self.inputs_validity[field_name] = False
            self.errors[field_name].setText(validation_result.message)
            self.errors[field_name].show()
        self.set_login_buttons_disability()

    def toggle_password_visibility(self):
        if self.password_toggle_btn.isChecked():
            self.inputs["password"].setEchoMode(QLineEdit.Normal)
        else:
            self.inputs["password"].setEchoMode(QLineEdit.Password)

    def set_login_buttons_disability(self):
        form_validity = all(self.inputs_validity.values())
        self.login_btn.setDisabled(not form_validity)
        self.employee_login_btn.setDisabled(not form_validity)
