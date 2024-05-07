from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from auth import auth_user
from datetime import datetime

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
    results = []

    while True:
        # navigate to the current month
        browser.get(f'{COOSPACE_URL}/Calendar?currentDate={current_year}-{current_month:02d}-01&view=0')

        # wait for the calendar to load
        wait.until(ec.presence_of_element_located((By.ID, 'calendar_main')))

        # get the events in the current month
        events = browser.find_elements(By.CSS_SELECTOR, '.calendarentry')

        # if there are no events, break the loop
        if len(events) == 0:
            break

        # fetch the events
        for event in events:
            try:

                # find event properties
                subject = event.find_element(By.CSS_SELECTOR, 'div:first-child').get_attribute('innerHTML')
                title = event.find_element(By.CLASS_NAME, 'entryinfo1').get_attribute('innerHTML')
                date = event.find_element(By.CLASS_NAME, 'entryinfo3').get_attribute('innerHTML')

                # format the date
                date = datetime.strptime(date.split('-')[0].strip(), '%Y. %m. %d. %H:%M')

                # do not include past events
                if now > date:
                    continue

                # add the event to the results
                results.append({
                    'subject': subject,
                    'title': title,
                    'date': datetime.strftime(date, '%Y.%m.%d. %H:%M'),
                    'url': f'{COOSPACE_URL}/Calendar?currentDate={current_year}-{current_month:02d}-01&view=2'
                })

            except Exception as e:
                print('Could not parse event:', e)

        # increase the month and year for the next iteration
        current_month += 1

        if current_month > 12:
            current_month = 1
            current_year += 1

    return sorted(results, key=lambda x: x['date'])


# print a list of calendar events to the console in a readable format
def print_calendar_events(events):
    print()

    if len(events) == 0:
        print('You have no upcoming calendar events.')
        print()
        return

    print(f'You have {len(events)} upcoming calendar events:')

    for event in events:
        print(f'    {event["date"]}: {event["subject"]}')
        print(f'    {event["title"]}')
        print(f'    [{event["url"]}]')

        print()


# get all notifications in descending order
def fetch_notifications(browser):
    # navigate to the notifications page
    browser.get(f'{COOSPACE_URL}/Events')

    # create an empty list to store the results
    results = []

    # find notifications
    events = browser.find_elements(By.CSS_SELECTOR, '.event-main')

    # fetch the notifications
    for event in events:
        try:
            title = event.find_element(By.CSS_SELECTOR, '.event-header-sentence').text
            date = event.find_element(By.CSS_SELECTOR, '.event-header-date > span').get_attribute('innerHTML')
            scene = event.find_element(By.CSS_SELECTOR, '.scene').get_attribute('innerHTML')
            tool = event.find_element(By.CSS_SELECTOR, '.tool').get_attribute('innerHTML')
            url = event.get_attribute('data-url')

            date = datetime.strptime(date, '%Y. %m. %d. %H:%M')

            results.append({
                'title': title,
                'date': datetime.strftime(date, '%Y.%m.%d. %H:%M'),
                'scene': scene,
                'tool': tool,
                'url': f'{COOSPACE_URL}{url}'
            })

        except Exception as e:
            print('Could not parse notification:', e)

    return sorted(results, key=lambda x: x['date'], reverse=True)


# print a list of notifications to the console in a readable format
def print_notifications(notifications):
    print()

    if len(notifications) == 0:
        print('You have no new notifications.')
        print()
        return

    print(f'You have {len(notifications)} new notifications:')

    for notification in notifications:
        print(f'    {notification["date"]}: {notification["title"]}')
        print(f'    {notification["scene"]} - {notification["tool"]}')
        print(f'    [{notification["url"]}]')
        print()
