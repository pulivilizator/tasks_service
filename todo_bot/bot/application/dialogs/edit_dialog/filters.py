from datetime import datetime


def filter_end_time(text):
    datetime.strptime(text, "%d.%m.%Y %H:%M")
    return text