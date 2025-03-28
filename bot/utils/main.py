import locale
import re

locale.setlocale(locale.LC_ALL, '') 

def format_currency(amount):
    return f"{int(amount):,}"


def validate_phone_number(value):
    pattern = r"^\+?\d{9,15}$"  # Allows numbers with or without a '+' and 9-15 digits
    if not re.match(pattern, value):
        return False
    return True


def validate_uzbek_car_plate(value):
    pattern = r"^(?:\d{2}[A-Z]\d{3}[A-Z]{2}|\d{2}\d{3}[A-Z]{2,3})$"
    if not re.match(pattern, value, re.IGNORECASE):
        return False
    return True
