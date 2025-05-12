from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from ..utils import get_absolute_path, add_class
from ..layouts import CatalogLayout, CartLayout, HistoryLayout
from ..widgets import OverlayWidget
from session import session


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self._logo_btn = QPushButton()
        self._catalog_btn = QPushButton()
        self._search_btn = QPushButton()
        self._cart_btn = QPushButton()
        self._logout_btn = QPushButton()

        self._catalog_container = QWidget()
        self._cart_container = QWidget()
        self._history_container = QWidget()

        self._curr_page = None

        self._overlay = OverlayWidget()

        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        # Подключение файла стилей
        style_file_path = get_absolute_path(__file__, "../styles/main_style.qss")
        with open(style_file_path, "r") as file:
            style = file.read()
            self.setStyleSheet(style)

        window_layout = QVBoxLayout()
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.setSpacing(0)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        self._logo_btn.setFixedWidth(59)
        self._logo_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # self._logo_btn.setCursor(Qt.PointingHandCursor)
        self._logo_btn.setIcon(
            QIcon(get_absolute_path(__file__, "../icons/logo_small.png"))
        )
        self._logo_btn.setIconSize(QSize(19, 16))

        self._catalog_btn.setText("Каталог")
        self._catalog_btn.setFixedHeight(50)
        self._catalog_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._catalog_btn.setContentsMargins(0, -1, 0, 0)
        add_class(self._catalog_btn, "header-btn")
        self._catalog_btn.setCursor(Qt.PointingHandCursor)

        self._cart_btn.setText("[0]")
        self._cart_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        add_class(self._cart_btn, "header-btn")
        self._cart_btn.setCursor(Qt.PointingHandCursor)
        self._cart_btn.setIcon(QIcon(get_absolute_path(__file__, "../icons/cart.png")))
        self._cart_btn.setIconSize(QSize(18, 18))

        self._logout_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self._logout_btn.setCursor(Qt.PointingHandCursor)
        self._logout_btn.setIcon(
            QIcon(get_absolute_path(__file__, "../icons/exit.png"))
        )
        self._logout_btn.setIconSize(QSize(16, 16))

        separators = []
        for i in range(2):
            separators.append(QWidget())
            separators[-1].setFixedWidth(1)
            separators[-1].setStyleSheet("background-color: #dcdcdc")
            separators[-1].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        header_layout.addWidget(self._logo_btn)
        header_layout.addWidget(separators[0])
        header_layout.addSpacing(20)
        header_layout.addWidget(self._catalog_btn)
        header_layout.addStretch(1)
        header_layout.addWidget(separators[1])
        header_layout.addSpacing(20)
        header_layout.addWidget(self._cart_btn)
        header_layout.addSpacing(20)
        header_layout.addWidget(self._logout_btn)
        header_layout.addSpacing(20)

        header = QWidget()
        header.setFixedHeight(50)
        header.setLayout(header_layout)

        header_upperline = QWidget()
        header_underline = QWidget()
        for widget in [header_upperline, header_underline]:
            widget.setFixedHeight(1)
            widget.setStyleSheet("background-color: #dcdcdc")
            widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        window_layout.addWidget(header_upperline, alignment=Qt.AlignTop)
        window_layout.addWidget(header, alignment=Qt.AlignTop)
        window_layout.addWidget(header_underline, alignment=Qt.AlignTop)
        window_layout.addWidget(self._catalog_container)
        window_layout.addWidget(self._cart_container)
        window_layout.addWidget(self._history_container)

        self.setLayout(window_layout)
        self.setMinimumSize(700, 400)
        self.resize(910, 600)

        self._overlay.setParent(self)

        self._cart_container.hide()
        self._history_container.hide()
        self._catalog_container.hide()

        self._catalog_container.setLayout(CatalogLayout(self))
        self._cart_container.setLayout(CartLayout(self))
        self.show_catalog()

    def _connect_signals(self):
        self._catalog_btn.clicked.connect(self.show_catalog)
        self._cart_btn.clicked.connect(self.show_cart)
        self._logout_btn.clicked.connect(self._logout)

    def show_catalog(self):
        self._curr_page = self._catalog_container
        self._show_curr_page()
        if self._catalog_container.layout() is None:
            self._catalog_container.setLayout(CatalogLayout(self))
        # Перераспределяем элементы, если в процессе работы в другой вкладке
        # был изменён размер окна
        self._catalog_container.layout().resize_catalog()
        self.setWindowTitle("Каталог")

    def show_cart(self):
        self._curr_page = self._cart_container
        self._show_curr_page()
        if self._cart_container.layout() is None:
            self._cart_container.setLayout(CartLayout(self))
        else:
            self._cart_container.layout().full_ui_update()
        self.setWindowTitle("Корзина")

    def show_history(self):
        self._curr_page = self._history_container
        self._show_curr_page()
        if self._history_container.layout() is None:
            self._history_container.setLayout(HistoryLayout(self))
        self._history_container.layout().ui_update()
        self.setWindowTitle("История заказов")

    # Для возможности внешнего доступа
    def set_cart_number(self, number):
        self._cart_btn.setText(f"[{number}]")

    # Для обновления корзиныпри добавлении товара изокна
    def update_cart(self):
        if self._curr_page == self._cart_container:
            self._cart_container.layout().full_ui_update()
        else:
            self._cart_container.layout().cart_number_update()

    def _show_curr_page(self):
        for page in [
            self._catalog_container,
            self._cart_container,
            self._history_container,
        ]:
            if page == self._curr_page:
                page.show()
            else:
                page.hide()
    
    def _logout(self):
        session.token = None
        from ..windows import LoginWindow

        session.curr_window = LoginWindow()
        session.curr_window.show()
        self.close()

    def show_overlay(self):
        self._overlay.resize()
        self._overlay.show()

    def hide_overlay(self):
        self._overlay.hide()

    def resizeEvent(self, event):
        self._overlay.resize()
        # Применяем перераспределение элементов только когда видно каталог
        if self._curr_page == self._catalog_container:
            self._catalog_container.layout().resize_catalog()
        super().resizeEvent(event)

    def closeEvent(self, event):
        session.windows.clear()
        super().closeEvent(event)
