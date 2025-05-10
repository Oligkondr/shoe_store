def format_price(num1, num2):
    if num1 == num2:
        return f"{num1:,} ₽".replace(",", " ")
    else:
        return f"{num1:,} – {num2:,} ₽".replace(",", " ")


def format_colors_amount(count):
    if 11 <= count % 100 <= 14:
        return f"{count} цветов"
    last_digit = count % 10
    if last_digit == 1:
        return f"{count} цвет"
    elif 2 <= last_digit <= 4:
        return f"{count} цвета"
    else:
        return f"{count} цветов"
