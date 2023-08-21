import unittest
from unittest.mock import Mock
from server import AuthServicer
from zkp_auth_pb2 import RegisterRequest, AuthenticationChallengeRequest, AuthenticationAnswerRequest
import constants
from decimal import Decimal, getcontext

# Set the precision to the maximum possible value
getcontext().prec = 999999999

class TestAuthServicer(unittest.TestCase):
    def setUp(self):
        self.servicer = AuthServicer()
        

    def test_register_existing_user(self):
        # Add a user to the userDBMap
        self.servicer.userDBMap["existing_user"] = Mock()

        # Create a mock context
        context = Mock()

        # Create a request with an existing username
        request = RegisterRequest(user="existing_user")

        # Call the Register method
        response = self.servicer.Register(request, context)

        # Check if the response has an error code
        self.assertEqual(context.set_code.call_args[0][0], constants.Duplicate)  

    def test_register_new_user(self):
        # Create a mock context
        context = Mock()

        # Create a request with a new username
        request = RegisterRequest(user="new_user", y1="0.5", y2="0.7")

        # Call the Register method
        response = self.servicer.Register(request, context)

        # Check if the response doesn't have an error code
        self.assertEqual(context.set_code.call_count, 0)

        # Check if the user was added to the userDBMap
        self.assertEqual(self.servicer.userDBMap["new_user"].userName, "new_user")
        self.assertEqual(str(self.servicer.userDBMap["new_user"].y1), "0.5")
        self.assertEqual(str(self.servicer.userDBMap["new_user"].y2), "0.7")

    def test_create_authentication_challenge(self):
        # Create a mock context
        context = Mock()

        # Add a user to the userDBMap
        self.servicer.userDBMap["test_user"] = Mock(userName="test_user", y1="0.5", y2="0.7")

        # Create a request for authentication challenge
        request = AuthenticationChallengeRequest(user="test_user", r1="0.456", r2="0.789")

        # Call the CreateAuthenticationChallenge method
        response = self.servicer.CreateAuthenticationChallenge(request, context)

        # Check if the response contains valid auth_id and c values
        self.assertEqual(len(response.auth_id), 36)  # UUID format
        self.assertTrue(response.c)


if __name__ == '__main__':
    unittest.main()
