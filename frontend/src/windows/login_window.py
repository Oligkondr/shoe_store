from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedWidget,
    QFormLayout,
    QVBoxLayout,
    QSpacerItem,
    QHBoxLayout,
    QGraphicsDropShadowEffect,
)
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QColor, QIcon, QResizeEvent

from ..utils import get_absolute_path, clear_layout
from ..layouts import LoginFormLayout, RegistrationFormLayout, SuccessRegistrationLayout
from ..widgets import OverlayWidget

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self._form_container = QWidget()
        self._close_button = QPushButton()
        self._overlay = OverlayWidget()

        # Cохранение позиции для перемещения
        self._old_window_pos = None

        self._init_ui()
        self.show_login_form()

    def _init_ui(self):
        # Подключение файла стилей
        style_file_path = get_absolute_path(__file__, "../styles/login_style.qss")
        with open(style_file_path, "r") as file:
            style = file.read()
            self.setStyleSheet(style)

        # Настройка и расположение элементов окна
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        window_layout = QHBoxLayout()
        window_layout.setSpacing(0)
        window_layout.setContentsMargins(20, 20, 20, 20)

        shadow = QGraphicsDropShadowEffect()
        shadow.setOffset(0, 0)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 125))

        shadow_container = QWidget()
        shadow_container.setGraphicsEffect(shadow)
        shadow_container.setFixedHeight(530)

        shadow_container_layout = QHBoxLayout()
        shadow_container_layout.setSpacing(0)
        shadow_container_layout.setContentsMargins(0, 0, 0, 0)

        image_container = QWidget()
        image_container.setObjectName("login-image")
        image_container.setFixedWidth(350)

        ui_container = QWidget()
        ui_container.setFixedWidth(350)

        ui_container_layout = QVBoxLayout()
        ui_container_layout.setContentsMargins(0, 0, 0, 0)

        ui_container_layout.addStretch(1)
        ui_container_layout.addWidget(self._form_container)
        ui_container_layout.addStretch(1)
        ui_container.setLayout(ui_container_layout)

        shadow_container_layout.addWidget(image_container, 1)
        shadow_container_layout.addWidget(ui_container, 1)
        shadow_container.setLayout(shadow_container_layout)

        window_layout.addWidget(shadow_container)
        self.setLayout(window_layout)

        self._overlay.setParent(ui_container)

        self._close_button.setObjectName("close-window-btn")
        self._close_button.setParent(ui_container)
        self._close_button.setGeometry(302, 28, 20, 20)
        self._close_button.setIcon(
            QIcon(get_absolute_path(__file__, "../icons/close1.png"))
        )
        self._close_button.setIconSize(QSize(16, 16))
        self._close_button.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self._close_button.setCursor(Qt.PointingHandCursor)
        self._close_button.clicked.connect(self.close)

    def _render_form_layout(self, new_layout):
        curr_layout = self._form_container.layout()
        if curr_layout is not None:
            clear_layout(curr_layout)
            QWidget().setLayout(curr_layout)
        self._form_container.setLayout(new_layout)

    def show_registration_form(self):
        self._render_form_layout(RegistrationFormLayout(self))

    def show_login_form(self):
        self._render_form_layout(LoginFormLayout(self))

    def show_success_registration_message(self):
        self._render_form_layout(SuccessRegistrationLayout(self))

    def show_overlay(self):
        self._overlay.resize()
        self._overlay.show()

    def hide_overlay(self):
        self._overlay.hide()
    
    def show_main_window(self):
        from ..windows import MainWindow
        MainWindow().show()
        self.close()
        

    # Перемещение окна
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._old_window_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self._old_window_pos:
            delta = event.globalPos() - self._old_window_pos
            self.move(self.pos() + delta)
            self._old_window_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self._old_window_pos = None
