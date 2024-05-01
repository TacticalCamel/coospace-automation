from selenium import webdriver
from tasks import login, get_calendar_events, get_new_notifications
import json

# the url of the root page
base_url = 'https://www.coosp.etr.u-szeged.hu'

with webdriver.Chrome() as browser:
    # try to log in
    login(browser, base_url)

    # get the calendar events
    events = get_calendar_events(browser, base_url)

    # get the new notifications
    get_new_notifications(browser, base_url)

    print(json.dumps(events, indent=2))

    input()
