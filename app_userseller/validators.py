from django.core.exceptions import ValidationError
import re

def validate_password_strength(value):
    common_passwords = [
        '123456', 'password', '123456789', '12345678', '12345', 
        '1234567', '1234567890', '123123', 'abc123', 'qwerty', 
        'monkey', 'letmein', 'trustno1', 'dragon', 'baseball'
    ]
    if ' ' in value:
        raise ValidationError("Пароль не должен содержать пробелы")
    # Проверка длины пароля
    if len(value) < 8:
        raise ValidationError(
            ("Password must be at least 8 characters long."),
            code='password_too_short',
        )
    
    # Проверка наличия пароля в списке общих паролей
    if value.lower() in common_passwords:
        raise ValidationError(
            ("This password is too common."),
            code='password_too_common',
        )
    
    # Проверка на простоту пароля (например, пароль состоит только из цифр)
    if value.isdigit():
        raise ValidationError(
            ("This password is too simple."),
            code='password_too_simple',
        )


def validate_email_domain(value):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
        raise ValidationError("Введите правильный адрес электронной почты")
    domain = value.split('@')[1]
    allowed_domains = [
        'gmail.com',
        'mail.ru'
    ]
    if domain not in allowed_domains:
        raise ValidationError("Электронная почта должна быть с доменом @gmail.com или @mail.ru")
