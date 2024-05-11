import unittest
import mock

import auth


class TestAuth(unittest.TestCase):
    username = 'test.user'
    pwd = 'test.pwd'

    def test_save_then_load(self):
        # tests data
        # save the credentials
        auth.save_credentials(TestAuth.username, TestAuth.pwd)

        # load the credentials
        loaded_username, loaded_password = auth.load_credentials()

        # check if the loaded credentials are correct
        self.assertEqual(loaded_username, TestAuth.username)
        self.assertEqual(loaded_password, TestAuth.pwd)

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

    def test_save_error(self):
        if auth.credentials_file_path.exists():
            # remove the credentials file
            auth.credentials_file_path.unlink()

        # attempt to save the credentials
        auth.save_credentials(1, 3233)

        # check that the credentials file does not exist
        self.assertFalse(auth.credentials_file_path.exists())

    def test_auth_user_with_save(self):
        # test data
        username = 'test.user'
        password = 'test.pwd'

        # save the credentials
        auth.save_credentials(username, password)

        # authenticate the user
        loaded_username, loaded_password = auth.auth_user()

        # check if the loaded credentials are correct
        self.assertEqual(loaded_username, username)
        self.assertEqual(loaded_password, password)

        # remove the credentials file
        auth.credentials_file_path.unlink()

    @mock.patch("builtins.input", return_value=username)
    @mock.patch("pwinput.pwinput", return_value=pwd)
    def test_auth_user_without_save(self, _, __):
        if auth.credentials_file_path.exists():
            # remove the credentials file
            auth.credentials_file_path.unlink()

        # authenticate the user
        loaded_username, loaded_password = auth.auth_user()

        # check if the loaded credentials are correct
        self.assertEqual(loaded_username, TestAuth.username)
        self.assertEqual(loaded_password, TestAuth.pwd)
