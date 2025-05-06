from PyQt5.QtWidgets import QWidget, QLayout, QMessageBox
from typing import Optional


def delete_layout(layout: Optional[QLayout]):
    """
    Рекурсивно удаляет все дочерние элементы QLayout'а
    и сам QLayout после этого.
    """
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            delete_layout(child.layout())
    QWidget().setLayout(layout)


def delete_widget(widget: QWidget):
    """
    Удаляет виджет.
    """
    layout = widget.layout()
    if layout is not None:
        delete_layout(layout)
    widget.setParent(None)
    widget.deleteLater()


def replace_widget_in_layout(layout: QLayout, old_widget: QWidget, new_widget: QWidget):
    """
    Заменяет виджет в QLayout'е.
    
    [ВАЖНО]
        old_widget должен находиться непосредственно в layout'е,
        иначе замены не произойдёт.
    """
    index = layout.indexOf(old_widget)
    if index == -1:
        return

    item = layout.takeAt(index)
    widget = item.widget()
    if widget is not None:
        delete_widget(widget)

    layout.insertWidget(index, new_widget)

def show_error_window():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText("Упс, что-то пошло не так...\nПожалуйста, повторите операцию. \n\nВ случае повторной ошибки\nперезагрузите приложение.")
    msg.setWindowTitle("Ошибка")
    msg.setStandardButtons(QMessageBox.Ok) 
    button = msg.button(QMessageBox.Ok)
    button.setText("Понятно")
    msg.exec_()
    

# Имитация работы с СSS-классами, как в JS
def add_class(widget: QWidget, *classes_to_add: str):
    curr_class_str = widget.property("class")
    if curr_class_str is None:
        curr_class_str = ""
    curr_classes = curr_class_str.strip().split(" ")
    new_classes = set(curr_classes) | set(classes_to_add)
    widget.setProperty("class", " ".join(new_classes))


def remove_class(widget: QWidget, *classes_to_remove: str):
    curr_class_str = widget.property("class")
    if curr_class_str is None:
        curr_class_str = ""
    curr_classes = curr_class_str.strip().split(" ")
    new_classes = set(curr_classes) - set(classes_to_remove)
    widget.setProperty("class", " ".join(new_classes))


def toggle_class(widget: QWidget, class_to_toggle: str, force: Optional[bool] = None):
    curr_class_str = widget.property("class")
    if curr_class_str is None:
        curr_class_str = ""
    new_classes = set(curr_class_str.strip().split(" "))
    if force is None:
        if class_to_toggle in new_classes:
            new_classes.discard(class_to_toggle)
        else:
            new_classes.add(class_to_toggle)
    elif force:
        new_classes.add(class_to_toggle)
    else:
        new_classes.discard(class_to_toggle)
    widget.setProperty("class", " ".join(new_classes))
