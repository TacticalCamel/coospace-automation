import pwinput
import pathlib
import base64

def auth_user(skip_load=False):
    # use the saved credentials, if any
    if not skip_load:
        # try to load the credentials from the file
        username, password = load_credentials()

        # if the credentials are found, return them
        if username and password:
            return username, password

        # if the credentials are not found, ask the user to enter them
        print('No credentials found. Please enter your username and password.')

    # get the username and password from the user
    username = input('username: ')
    password = pwinput.pwinput(prompt='password: ', mask='')

    # save the credentials to the file
    save_credentials(username, password)

    # return the credentials
    return username, password

def load_credentials():
    # get the home directory
    home = pathlib.Path.home()

    # try to open the file
    try:
        with open(home / '.coospace-credentials', 'r') as file:
            # read the username and password from the file
            username = file.readline().strip()
            password = base64.b64decode(file.readline().strip()).decode()

            return username, password
    except Exception:
        return None, None

def save_credentials(username, password):
    # get the home directory
    home = pathlib.Path.home()

    # try to open the file
    try:
        with open(home / '.coospace-credentials', 'w') as file:
            # write the username and password to the file
            file.write(username + '\n')
            file.write(base64.b64encode(password.encode()).decode() + '\n')
    except Exception:
        print('Could not save credentials to file.')
