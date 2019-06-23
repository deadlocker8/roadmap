from datetime import datetime, date


class DateFormatter:
    DEFAULT_DATE = date(2000, 1, 1)
    FORMAT = "%d.%m.%Y"

    @staticmethod
    def format(dateObject):
        if dateObject == DateFormatter.DEFAULT_DATE:
            return "-"
        return datetime.strftime(dateObject, DateFormatter.FORMAT)
