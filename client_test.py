import unittest
from unittest.mock import Mock
from client import ZKPClientUtil

class TestClientMethods(unittest.TestCase):
    
    def setUp(self):
        self.stub = Mock()
        self.client = ZKPClientUtil
    
    def test_register_user(self):
        user_name = "testUser"
        secret_x = "12345"
        self.client.register_user(self.stub, user_name, secret_x)
        self.stub.Register.assert_called()

    
    def test_register_user_success(self):
        self.stub.Register.return_value = True  # Mocking the return value for Register RPC call
        result = self.client.register_user(self.stub, "testUser", "123")
        self.assertTrue(result)

    def test_register_user_failure(self):
        self.stub.Register.side_effect = Exception("Username already taken!")  # Mocking an exception for Register RPC call
        result = self.client.register_user(self.stub, "testUser", "123")
        self.assertFalse(result)

    def test_decimal_conversion_invalid_input(self):
        """ Test if invalid password (non-numeric) raises the appropriate exception """
        password = "invalid_password"
        with self.assertRaises(Exception):  # Expecting a conversion error
            self.client.login_user(self.stub, "testUser", password)


if __name__ == "__main__":
    unittest.main()
