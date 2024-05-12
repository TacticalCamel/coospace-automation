from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime

from coospace_automation.calendar import CalendarEvent
from coospace_automation.notification import Notification
from coospace_automation.auth import auth_user

# the url of the root page
COOSPACE_URL = 'https://www.coosp.etr.u-szeged.hu'


# prompt the user to log in
def prompt_login(browser):
    # create a wait object with a timeout of 5 seconds
    wait = WebDriverWait(browser, 5)

    # open the base url
    browser.get(COOSPACE_URL)

    # wait for the page to load
    wait.until(ec.presence_of_element_located((By.ID, 'username')))

    # find the username, password and login button elements
    username_field = browser.find_element(By.ID, 'username')
    password_field = browser.find_element(By.ID, 'password')
    login_button = browser.find_element(By.CSS_SELECTOR, 'input[type=submit]')

    # get the username and password from the user
    if not username_field or not password_field or not login_button:
        print('Could not identify login form elements.')
        browser.quit()
        exit(1)

    # do not skip loading credentials for the first time
    skip_credential_load = False

    # keep asking the user for the credentials until the login is successful
    while True:
        # get the username and password from the user
        username, password = auth_user(skip_credential_load)

        # fill in the username and password and click the login button
        username_field.clear()
        username_field.send_keys(username)

        password_field.clear()
        password_field.send_keys(password)

        login_button.click()

        print('Logging in...')

        try:
            # wait for the page to load
            wait.until(ec.invisibility_of_element_located((By.ID, 'username')))

        except:
            print('Login failed. Try again with the correct credentials.')

        else:
            # get username
            username = browser.find_element(By.CSS_SELECTOR, '.name > span')

            if username:
                print('Logged in as', username.text)

            break

        # skip the loading credentials from now on, since it did not work the first time
        skip_credential_load = True


# get all events from the calendar in ascending order
def fetch_calendar_events(browser):
    # create a wait object with a timeout of 5 seconds
    wait = WebDriverWait(browser, 5)

    # get the current date
    now = datetime.now()

    # get the current month and year
    current_month = now.month
    current_year = now.year

    # create an empty list to store the results
    events = []

    while True:
        # navigate to the current month
        browser.get(f'{COOSPACE_URL}/Calendar?currentDate={current_year}-{current_month:02d}-01&view=0')

        # wait for the calendar to load
        wait.until(ec.presence_of_element_located((By.ID, 'calendar_main')))

        # get the events in the current month
        event_elements = browser.find_elements(By.CSS_SELECTOR, '.calendarentry')

        # if there are no events, break the loop
        if len(event_elements) == 0:
            break

        # fetch the events
        for event_element in event_elements:
            try:
                # find event properties
                subject = event_element.find_element(By.CSS_SELECTOR, 'div:first-child').get_attribute('innerHTML')
                title = event_element.find_element(By.CLASS_NAME, 'entryinfo1').get_attribute('innerHTML')
                date = event_element.find_element(By.CLASS_NAME, 'entryinfo3').get_attribute('innerHTML')

                # format the date
                date = datetime.strptime(date.split('-')[0].strip(), '%Y. %m. %d. %H:%M')

                # do not include past events
                if now > date:
                    continue

                # create a CalendarEvent object
                event = CalendarEvent(
                    subject=subject,
                    title=title,
                    date=date,
                    url=f'{COOSPACE_URL}/Calendar?currentDate={date.year}-{date.month:02d}-{date.day:02d}&view=2'
                )

                # add the event to the list
                events.append(event)

            except Exception as e:
                print(f'Could not parse event, skipping: {e}')

        # advance to the next month
        current_month += 1

        if current_month > 12:
            current_month = 1
            current_year += 1

    # sort events by date
    return sorted(events, key=lambda x: x.date)


# display calendar events to the console in a readable format
def display_calendar_events(events):
    print()

    if len(events) == 0:
        print('You have no upcoming calendar events.')
        print()
        return

    print(f'You have {len(events)} upcoming calendar events:')

    for event in events:
        if not isinstance(event, CalendarEvent):
            continue

        print(f'    {event.date}: {event.subject}')
        print(f'    {event.title}')
        print(f'    [{event.url}]')
        print()


# get all notifications in descending order
def fetch_notifications(browser):
    # navigate to the notifications page
    browser.get(f'{COOSPACE_URL}/Events')

    # create an empty list to store the results
    notifications = []

    # find notifications
    notification_elements = browser.find_elements(By.CSS_SELECTOR, '.event-main')

    # fetch the notifications
    for n in notification_elements:
        try:
            # find notification properties
            title = n.find_element(By.CSS_SELECTOR, '.event-header-sentence').text
            date = n.find_element(By.CSS_SELECTOR, '.event-header-date > span').get_attribute('innerHTML')
            scene = n.find_element(By.CSS_SELECTOR, '.scene').get_attribute('innerHTML')
            tool = n.find_element(By.CSS_SELECTOR, '.tool').get_attribute('innerHTML')
            url = n.get_attribute('data-url')

            date = datetime.strptime(date, '%Y. %m. %d. %H:%M')

            # create a Notification object
            notification = Notification(
                title=title,
                date=date,
                scene=scene,
                tool=tool,
                url=f'{COOSPACE_URL}{url}'
            )

            # add the notification to the list
            notifications.append(notification)

        except Exception as e:
            print(f'Could not parse notification, skipping: {e}')

    # sort notifications by date from newest to oldest
    return sorted(notifications, key=lambda x: x.date, reverse=True)


# display notifications to the console in a readable format
def display_notifications(notifications):
    print()

    if len(notifications) == 0:
        print('You have no new notifications.')
        print()
        return

    print(f'You have {len(notifications)} new notifications:')

    for notification in notifications:
        if not isinstance(notification, Notification):
            continue

        print(f'    {notification.date}: {notification.title}')
        print(f'    {notification.scene} - {notification.tool}')
        print(f'    [{notification.url}]')
        print()


# download a file from the personal folder to the default download directory
def download_file(browser, coospace_path):
    # create a wait object with a timeout of 5 seconds
    wait = WebDriverWait(browser, 5)

    # the index of the last slash in the file path
    split_index = coospace_path.rfind('/')

    # get the folder name and the file name
    folder_name = coospace_path[:split_index]
    file_name = coospace_path[split_index + 1:]

    try:
        # navigate to the folder
        browser.get(f'{COOSPACE_URL}/My/Folder/Index/{folder_name}')

        # wait for the page to load
        wait.until(ec.presence_of_element_located((By.ID, 'items')))

        # find the file by its name
        file_link = browser.find_element(By.XPATH, f'//a[text()=\'{file_name}\']')

        # get the url of the file
        url = file_link.get_attribute("href")

        # download the file
        browser.get(url)

    except:
        print(f'Could not locate file "{coospace_path}"')
