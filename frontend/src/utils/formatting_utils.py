from datetime import datetime


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


def format_time_string(str):
    month_dict = {
        "01": "января",
        "02": "февраля",
        "03": "марта",
        "04": "апреля",
        "05": "мая",
        "06": "июня",
        "07": "июля",
        "08": "августа",
        "09": "сентября",
        "10": "октября",
        "11": "ноября",
        "12": "декабря",
    }
    date_time = datetime.strptime(str, "%Y-%m-%dT%H:%M:%S.%f")
    formatted_parts = date_time.strftime("%d %m %Y %H:%M").split(" ")
    formatted_parts[1] = month_dict[formatted_parts[1]]
    return " ".join(formatted_parts)
