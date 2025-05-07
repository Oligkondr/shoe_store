from ..classes import ValidationResult
import re


def validate_login_email(str):
    if len(str.strip()) == 0:
        return ValidationResult(False, "Заполните поле")
    else:
        return ValidationResult(True)


def validate_login_password(str):
    if len(str) == 0:
        return ValidationResult(False, "Заполните поле")
    else:
        return ValidationResult(True)


def validate_registration_email(str):
    stripped_str = str.strip()
    if len(stripped_str) == 0:
        return ValidationResult(False, "Заполните поле")
    elif re.match(r"^[^@]+@[^@]+$", stripped_str) is None:
        return ValidationResult(False, "Неверный формат email")
    else:
        return ValidationResult(True)
        
            


def validate_registration_name(str):
    if len(str.strip()) == 0:
        return ValidationResult(False, "Заполните поле")
    else:
        return ValidationResult(True)


def validate_registration_surname(str):
    if len(str.strip()) == 0:
        return ValidationResult(False, "Заполните поле")
    else:
        return ValidationResult(True)


def validate_registration_phone(str):
    if len(str) == 0:
        return ValidationResult(False, "Заполните поле")
    elif len(str) != 11:
        return ValidationResult(False, "Номер должен содержать 11 цифр")
    else:
        return ValidationResult(True)


def validate_registration_password(str):
    if len(str) == 0:
        return ValidationResult(False, "Заполните поле")
    elif len(str) < 6 or len(str) > 12:
        return ValidationResult(False, "Пароль должен содержать от 6 до 12 символов")
    elif not any(c.isupper() for c in str):
        return ValidationResult(
            False, "Пароль должен содержать хотя бы одну заглавную букву"
        )
    elif not any(c.islower() for c in str):
        return ValidationResult(
            False, "Пароль должен содержать хотя бы одну строчную букву"
        )
    elif not any(c.isdigit() for c in str):
        return ValidationResult(False, "Пароль должен содержать хотя бы одну цифру")
    elif not any (c in " !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~" for c in str):
        return ValidationResult(False, "Пароль должен содержать хотя бы один специальный символ")
    else:
        return ValidationResult(True)


def validate_registration_password2(str):
    if len(str.strip()) == 0:
        return ValidationResult(False, "Заполните поле")
    else:
        return ValidationResult(True)
