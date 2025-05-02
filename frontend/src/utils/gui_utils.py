# Рекурсивное удаление всех дочерних элементов Layout'а
def clear_layout(layout):
    if layout is not None:
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                clear_layout(child.layout())


# Имитация работы с СSS-классами, как в JS
def add_class(widget, *classes_to_add):
    curr_class_str = widget.property("class")
    if curr_class_str is None:
        curr_class_str = ""
    curr_classes = curr_class_str.strip().split(" ")
    new_classes = set(curr_classes) | set(classes_to_add)
    widget.setProperty("class", " ".join(new_classes))


def remove_class(widget, *classes_to_remove):
    curr_class_str = widget.property("class")
    if curr_class_str is None:
        curr_class_str = ""
    curr_classes = curr_class_str.strip().split(" ")
    new_classes = set(curr_classes) - set(classes_to_remove)
    widget.setProperty("class", " ".join(new_classes))


def toggle_class(widget, class_to_toggle, force=None):
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
