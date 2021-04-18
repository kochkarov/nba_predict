import datetime


class DateConverter:
    regex = '[0-9]{8}'

    def to_python(self, value):
        return datetime.datetime.strptime(value, '%Y%m%d')

    def to_url(self, value):
        return datetime.datetime.strftime(value, '%Y%m%d')
