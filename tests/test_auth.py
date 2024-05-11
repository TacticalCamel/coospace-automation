import unittest

import auth


class TestAuth(unittest.TestCase):
    def test_save_then_load(self):
        # tests data
        username = 'tests.user'
        password = 'tests.pwd'

        # save the credentials
        auth.save_credentials(username, password)

        # load the credentials
        loaded_username, loaded_password = auth.load_credentials()

        # check if the loaded credentials are correct
        self.assertEqual(loaded_username, username)
        self.assertEqual(loaded_password, password)

        # remove the credentials file
        auth.credentials_file_path.unlink()

    def test_load_none(self):
        if auth.credentials_file_path.exists():
            # remove the credentials file
            auth.credentials_file_path.unlink()

        # load the credentials
        loaded_username, loaded_password = auth.load_credentials()

        # check if the loaded credentials are none
        self.assertIsNone(loaded_username)
        self.assertIsNone(loaded_password)
