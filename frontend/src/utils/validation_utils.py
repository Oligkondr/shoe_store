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
