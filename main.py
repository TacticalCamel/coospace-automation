from selenium import webdriver
import coospace

with webdriver.Chrome() as browser:
    # try to log in
    coospace.prompt_login(browser)

    # get the calendar events
    events = coospace.fetch_calendar_events(browser)

    # print the events
    coospace.print_calendar_events(events)

    # get the new notifications
    notifications = coospace.fetch_notifications(browser)

    # print the notifications
    coospace.print_notifications(notifications)
