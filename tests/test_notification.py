import unittest

from coospace_automation.notification import Notification


class TestNotification(unittest.TestCase):
    def test_properties(self):
        # test data
        title = 'TestTitle'
        date = '2024.05.12'
        scene = 'TestScene'
        tool = 'TestTool'
        url = 'http://test.url'

        # create a notification
        notification = Notification(title, date, scene, tool, url)

        # check the properties
        self.assertEqual(notification.title, title)
        self.assertEqual(notification.date, date)
        self.assertEqual(notification.scene, scene)
        self.assertEqual(notification.tool, tool)
        self.assertEqual(notification.url, url)
