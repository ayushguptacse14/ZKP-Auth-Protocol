import grpc
import zkp_auth_pb2 as zkp
import zkp_auth_pb2_grpc as zkp_grpc
import random
import constants
from decimal import Decimal, getcontext

# Set the precision to the maximum possible value
getcontext().prec = 999999999

class ZKPClientUtil:

    @staticmethod
    def register_user(stub, user_name, x):
        """
        Register a user with the server.

        Args:
            stub (zkp_grpc.AuthStub): gRPC stub for making remote procedure calls.
            user_name (str): User's name.
            x (str): User's private value 'x'.

        Returns:
            bool: True if registration is successful, False otherwise.
        """
        x = Decimal(x)
        y1 = Decimal(constants.G) ** x
        y2 = Decimal(constants.H) ** x
        try:
            req = zkp.RegisterRequest(user=user_name, y1=str(y1), y2=str(y2))
            stub.Register(req)
            print("\n User Registered:", req.user, "\n")
            return True
        except:
            print("\n Username already taken! \n")
            return False

    @staticmethod
    def login_user(stub, user_name, x):
        """
        Authenticate and log in a user.

        Args:
            stub (zkp_grpc.AuthStub): gRPC stub for making remote procedure calls.
            user_name (str): User's name.
            x (str): User's private value 'x'.

        Returns:
            None
        """
        x = Decimal(x)
        k = int(constants.LEFT_LIMIT) + random.randint(0, int(constants.RIGHT_LIMIT) - int(constants.LEFT_LIMIT))
        k = Decimal(k)
        r1 = Decimal(constants.G) ** k
        r2 = Decimal(constants.H) ** k
        authentication_challenge_request = zkp.AuthenticationChallengeRequest(
            user=user_name, r1=str(r1), r2=str(r2)
        )
        authentication_challenge_response = stub.CreateAuthenticationChallenge(authentication_challenge_request)
        c = Decimal(authentication_challenge_response.c)

        s = (k - (c * x))

        authentication_answer_request = zkp.AuthenticationAnswerRequest(
            auth_id=authentication_challenge_response.auth_id, s=str(s)
        )
        authentication_answer_response = stub.VerifyAuthentication(authentication_answer_request)
        if (authentication_answer_response.session_id == "INVALID"):
            print("\n Login Failed \n")
        else:
            print("\n Login Successful with Session Id:", authentication_answer_response.session_id,"\n")

def main():
    # Establish a connection to the gRPC server
    channel = grpc.insecure_channel("localhost:50051")
    stub = zkp_grpc.AuthStub(channel)

    default_user_name = "Alex"
    default_password = "123"

    while True:
        print("Choose an option:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            user_name = input(f"Enter desired username (default: {default_user_name}): ")
            if user_name == "":
                user_name = default_user_name

            password = input(f"Enter desired numeric password (x value, default: {default_password}): ")
            if password == "":
                password = default_password

            try:
                Decimal(password)
                ZKPClientUtil.register_user(stub, user_name, password)
            except:
                print("\n Invalid numeric password. Password should be a number. \n")
        
        elif choice == "2":
            user_name = input(f"Enter username (default: {default_user_name}): ")
            if user_name == "":
                user_name = default_user_name

            password = input(f"Enter numeric password (x value, default: {default_password}): ")
            if password == "":
                password = default_password

            try:
                Decimal(password)
                ZKPClientUtil.login_user(stub, user_name, password)
            except:
                print("\n Invalid numeric password. Password should be a number. \n")

        elif choice == "3":
            print(" \n Exiting the client. \n")
            break

        else:
            print("\n Invalid choice. Please choose a valid option. \n")


if __name__ == "__main__":
    main()
