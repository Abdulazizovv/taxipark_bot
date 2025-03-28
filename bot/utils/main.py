import locale

locale.setlocale(locale.LC_ALL, '') 

def format_currency(amount):
    return f"{int(amount):,}"
