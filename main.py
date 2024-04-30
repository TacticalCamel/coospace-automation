from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import auth

def try_login():
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
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        print('Logging in...')

        # wait for the page to load
        wait = WebDriverWait(browser, 5)
        wait.until(EC.invisibility_of_element_located((By.ID, 'username')))

        # if the url has not changed, the login was unsuccessful
        if browser.current_url == base_url:
            print('Login failed. Try again with the correct credentials.')
        else:
            # get username
            username = browser.find_element(By.CSS_SELECTOR, '.name > span')

            if username:
                print('Logged in as', username.text)

            break

        # skip the loading credentials from now on, since it did not work the first time
        skip_credential_load = True

# the url of the root page
base_url = 'https://www.coosp.etr.u-szeged.hu/'

# create a new Chrome browser and open the coospace login page
browser = webdriver.Chrome()
browser.get(base_url)

# try to log in
try_login()

input()

browser.quit()
