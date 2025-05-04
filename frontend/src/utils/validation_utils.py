from ..classes import ValidationResult


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
    if len(str.strip()) == 0:
        return ValidationResult(False, "Заполните поле")
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
    elif len(str) < 6:
        return ValidationResult(False, "Минимальная длина — 6 символов")
    else:
        return ValidationResult(True)

def validate_registration_password2(str):
    if len(str.strip()) == 0:
        return ValidationResult(False, "Заполните поле")
    else:
        return ValidationResult(True)