from datetime import datetime


def get_age(foundation_year=1920):
    now = datetime.now()
    return now.year - foundation_year


def get_correct_year_name(age):
    if age % 100 in [11, 12, 13, 14]:
        return 'лет'
    if age % 10 == 1:
        return 'год'
    if age % 10 in [2, 3, 4]:
        return 'года'
    return 'лет'
