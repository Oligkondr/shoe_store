def get_color_word_form(count):
    if 11 <= count % 100 <= 14:
        return f"{count} цветов"
    last_digit = count % 10
    if last_digit == 1:
        return f"{count} цвет"
    elif 2 <= last_digit <= 4:
        return f"{count} цвета"
    else:
        return f"{count} цветов"
