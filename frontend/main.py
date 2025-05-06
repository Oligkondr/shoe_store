import sys
from os import path, listdir
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

from src.utils import get_absolute_path
from src.windows import LoginWindow
from session import session

if __name__ == "__main__":
    # Инициализация приложения
    app = QApplication(sys.argv)

    # Загрузка шрифтов
    font_dir_path = get_absolute_path(__file__, "src/fonts")
    for file in listdir(font_dir_path):
        QFontDatabase.addApplicationFont(path.join(font_dir_path, file))

    session.curr_window = LoginWindow()
    session.curr_window.show()
    sys.exit(app.exec_())
