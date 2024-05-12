import unittest

from coospace_automation.calendar import CalendarEvent


class TestCalendar(unittest.TestCase):
    def test_properties(self):
        # test data
        subject = 'TestSubject'
        title = 'TestTitle'
        date = '2024.05.12'
        url = 'http://test.url'

        # create a calendar event
        event = CalendarEvent(subject, title, date, url)

        # check the properties
        self.assertEqual(event.subject, subject)
        self.assertEqual(event.title, title)
        self.assertEqual(event.date, date)
        self.assertEqual(event.url, url)
