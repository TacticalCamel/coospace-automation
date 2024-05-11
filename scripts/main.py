from selenium import webdriver
from coospace_automation import coospace

# create an options object
options = webdriver.ChromeOptions()

# run the browser in headless mode
options.add_argument('--headless=new')

with webdriver.Chrome(options) as browser:
    # try to log in
    coospace.prompt_login(browser)

    # get the calendar events
    events = coospace.fetch_calendar_events(browser)

    # print the events
    coospace.display_calendar_events(events)

    # get the new notifications
    notifications = coospace.fetch_notifications(browser)

    # print the notifications
    coospace.display_notifications(notifications)

    # get file from personal folder
    coospace.download_file(browser, 'folder/what.txt')
