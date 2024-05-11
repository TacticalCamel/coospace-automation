import pwinput
import pathlib
import base64

# path to the file where the credentials are saved
credentials_file_path = pathlib.Path.home() / '.coospace-credentials'


# interactively attempt to authenticate the user
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


# load credentials from a file in the user home directory
def load_credentials():
    # try to open the file
    try:
        with open(credentials_file_path, 'r') as file:
            # read the username and password from the file
            username = file.readline().strip()
            password = base64.b64decode(file.readline().strip()).decode()

            return username, password
    except Exception:
        return None, None


# save credentials to a file in the user home directory
def save_credentials(username, password):
    # try to open the file
    try:
        with open(credentials_file_path, 'w') as file:
            # write the username and password to the file
            file.write(username + '\n')
            file.write(base64.b64encode(password.encode()).decode() + '\n')

    except Exception:
        print('Could not save credentials to file.')
