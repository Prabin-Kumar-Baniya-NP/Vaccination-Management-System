from datetime import date


def calculate_age(birth_date):
    """
    Returns the age from given birth date
    """
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
