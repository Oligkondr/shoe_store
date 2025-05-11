from os import path


def get_absolute_path(file_path, relative_path):
    """
    Формирует абсолютный путь к файлу на основе текущего положения файлла
    и кастомного относительного пути.
    """
    absolute_path = path.dirname(file_path)
    path_parts = relative_path.split("/")
    for part in path_parts:
        if part == "..":
            absolute_path = path.dirname(absolute_path)
        elif part not in [".", ""]:
            absolute_path = path.join(absolute_path, part)
    return absolute_path
