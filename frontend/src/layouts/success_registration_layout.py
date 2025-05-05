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
)
from ..widgets import ClickableWidget, OverlayWidget


class SuccessRegistrationLayout(QVBoxLayout):
    def __init__(self, show_login_form):
        super().__init__()

        self._show_login_form = show_login_form
        self._login_btn = QPushButton()

        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        self.setSpacing(0)
        self.setContentsMargins(30, 30, 30, 30)

        title = QLabel(
            str(session.registration_name)[0].upper()
            + str(session.registration_name)[1:]
            + ","
        )
        add_class(title, "title-text")
        title.setWordWrap(True)

        label = QLabel("ваш аккаунт успешно создан!")
        add_class(label, "small-text")
        label.setWordWrap(True)

        self._login_btn.setText("Войти")
        self._login_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        add_class(self._login_btn, "small-btn")
        self._login_btn.setCursor(Qt.PointingHandCursor)

        login_btn_icon = QLabel(" →")
        login_btn_icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        login_btn_icon.setContentsMargins(0, 0, 0, 1)
        add_class(login_btn_icon, "small-text")

        login_btn_layout = QHBoxLayout()
        login_btn_layout.addWidget(self._login_btn)
        login_btn_layout.addWidget(login_btn_icon)
        login_btn_layout.addStretch(1)

        self.addWidget(title)
        self.addWidget(label)
        self.addSpacing(18)
        self.addLayout(login_btn_layout)

    def _connect_signals(self):
        self._login_btn.clicked.connect(self._login_btn_handler)

    def _login_btn_handler(self):
        session.registration_name = None
        self._show_login_form()
