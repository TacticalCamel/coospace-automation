class CalendarEvent:
    def __init__(self, subject, title, date, url):
        self._subject = subject
        self._title = title
        self._date = date
        self._url = url

    @property
    def subject(self):
        return self._subject

    @property
    def title(self):
        return self._title

    @property
    def date(self):
        return self._date

    @property
    def url(self):
        return self._url
