import unittest
import mock

from coospace_automation import auth


# tests for the auth module
class TestAuth(unittest.TestCase):
    # test username and password
    username = 'TestUsername'
    pwd = 'TestPwd123'

    # remove the credentials file before a test is run, if it exists
    def setUp(self):
        if auth.credentials_file_path.exists():
            auth.credentials_file_path.unlink()

    # remove the credentials file after a test is run, if it exists
    def tearDown(self):
        if auth.credentials_file_path.exists():
            auth.credentials_file_path.unlink()

    # test saving then loading the credentials
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

    # test loading the credentials when there is no credentials file
    def test_load_none(self):
        # load the credentials
        loaded_username, loaded_password = auth.load_credentials()

        # check if the loaded credentials are none
        self.assertIsNone(loaded_username)
        self.assertIsNone(loaded_password)

    # test saving the credentials with incorrect parameters
    def test_save_error(self):
        # attempt to save the credentials
        auth.save_credentials(1, 3233)

        # check that the credentials file does not exist
        self.assertFalse(auth.credentials_file_path.exists())

    # test authenticating the user by loading saved credentials
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

    # test authenticating the user by manually entering the credentials
    @mock.patch("builtins.input", return_value=username)
    @mock.patch("pwinput.pwinput", return_value=pwd)
    def test_auth_user_without_save(self, _, __):
        # authenticate the user
        loaded_username, loaded_password = auth.auth_user()

        # check if the loaded credentials are correct
        self.assertEqual(loaded_username, TestAuth.username)
        self.assertEqual(loaded_password, TestAuth.pwd)
