from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

import auth
from datetime import datetime

def login(browser, base_url):
    # create a wait object with a timeout of 5 seconds
    wait = WebDriverWait(browser, 5)

    # open the base url
    browser.get(base_url)

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
        username, password = auth.auth_user(skip_credential_load)

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

        except Exception as e:
            print('Login failed. Try again with the correct credentials.')

        else:
            # get username
            username = browser.find_element(By.CSS_SELECTOR, '.name > span')

            if username:
                print('Logged in as', username.text)

            break

        # skip the loading credentials from now on, since it did not work the first time
        skip_credential_load = True

def get_calendar_events(browser, base_url):
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
        browser.get(f'{base_url}/Calendar?currentDate={current_year}-{current_month:02d}-01&view=0')

        # wait for the calendar to load
        wait.until(ec.presence_of_element_located((By.ID, 'calendar_main')))

        # get the events in the current month
        events = browser.find_elements(By.CSS_SELECTOR, '.calendarentry_popup')

        # if there are no events, break the loop
        if len(events) == 0:
            break

        # fetch the events
        for event in events:
            try:
                subject = event.find_element(By.CSS_SELECTOR, 'div:first-child').get_attribute('innerHTML')
                title = event.find_element(By.CLASS_NAME, 'entryinfo1').get_attribute('innerHTML')
                location = event.find_element(By.CLASS_NAME, 'entryinfo2').get_attribute('innerHTML')
                date = event.find_element(By.CLASS_NAME, 'entryinfo3').get_attribute('innerHTML')

                date = datetime.strptime(date, '%Y. %m. %d. %H:%M')

                if now > date:
                    continue

                results.append({
                    'subject': subject,
                    'title': title,
                    'location': None if location == '' else location,
                    'date': date.isoformat()
                })

            except Exception as e:
                print('Could not parse event:', e)

        # increase the month and year for the next iteration
        current_month += 1

        if current_month > 12:
            current_month = 1
            current_year += 1

    return sorted(results, key=lambda x: x['date'])

def get_new_notifications(browser, base_url):
    # navigate to the notifications page
    browser.get(f'{base_url}/Events')

    return
