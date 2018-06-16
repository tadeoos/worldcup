import dateutil.parser
from tzlocal import get_localzone


def iso_to_datetime(s):
    return dateutil.parser.parse(s)


def get_nice_date(date):
    return iso_to_datetime(date).astimezone(get_localzone()).strftime("%A, %d. %B %Y %I:%M%p")
