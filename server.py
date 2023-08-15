from concurrent import futures
import grpc
import logging
import zkp_auth_pb2 as zkp
import zkp_auth_pb2_grpc as zkp_grpc
import random
import uuid
import constants
from decimal import Decimal, getcontext

# Set the precision to the maximum possible value
getcontext().prec = 999999999

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ActiveAuthSessionsDB:
    """
    Class to represent an active authentication session in the server.
    """
    def __init__(self):
        self.authId = ""
        self.sessionId = ""
        self.userName = ""
        self.c = Decimal(0)
        self.r1 = Decimal(0)
        self.r2 = Decimal(0)

class UserDB:
    """
    Class to represent user data stored in the server.
    """
    def __init__(self):
        self.userName = ""
        self.y1 = Decimal(0)
        self.y2 = Decimal(0)

class AuthServicer(zkp_grpc.AuthServicer):
    """
    gRPC service implementation for authentication operations.
    """
    def __init__(self):
        self.userDBMap = {}
        self.activeAuthSessionsDBMap = {}

    def isEqual(a, b, percentage=Decimal(0.01)):
        """
        Check if two values are approximately equal within a specified percentage.

        Args:
            a (Decimal): First value.
            b (Decimal): Second value.
            percentage (Decimal): Allowed relative difference (default is 0.01).

        Returns:
            bool: True if values are approximately equal, False otherwise.
        """
        difference = abs(a - b)
        avg = (abs(a) + abs(b)) / Decimal(2.0)
        relative_difference = difference / avg
        return relative_difference <= percentage

    def Register(self, request, context):
        """
        Handle user registration request.

        Args:
            request (zkp.RegisterRequest): User registration request.
            context (grpc.ServicerContext): gRPC context for handling the request.

        Returns:
            zkp.RegisterResponse: Response indicating registration status.
        """
        logger.info(f"Received registration request for user '{request.user}'")

        user = UserDB()
        if request.user in self.userDBMap:
            context.set_code(constants.Duplicate)
            context.set_details("Username already taken!")
            logger.info("Username already taken!")
            return  zkp.RegisterResponse()
        user.userName = request.user
        user.y1 = Decimal(request.y1)
        user.y2 = Decimal(request.y2)
        self.userDBMap[request.user] = user
        return zkp.RegisterResponse()

    def CreateAuthenticationChallenge(self, request, context):
        """
        Handle authentication challenge creation request.

        Args:
            request (zkp.AuthenticationChallengeRequest): Authentication challenge request.
            context (grpc.ServicerContext): gRPC context for handling the request.

        Returns:
            zkp.AuthenticationChallengeResponse: Response containing authentication challenge.
        """
        logger.info(f"Received authentication challenge request for user '{request.user}'")
        
        if request.user not in self.userDBMap:
            context.set_code(constants.NotFound)
            context.set_details("User does not exist!")
            logger.info("User does not exist!")
            return zkp.AuthenticationChallengeResponse()


        auth_id = str(uuid.uuid4())
        session_id = str(uuid.uuid4())
        c = Decimal(random.randint(int(constants.LEFT_LIMIT), int(constants.RIGHT_LIMIT)))

        auth_session = ActiveAuthSessionsDB()
        auth_session.authId = auth_id
        auth_session.sessionId = session_id
        auth_session.userName = request.user
        auth_session.c = c
        auth_session.r1 = Decimal(request.r1)
        auth_session.r2 = Decimal(request.r2)
        self.activeAuthSessionsDBMap[auth_id] = auth_session

        return zkp.AuthenticationChallengeResponse(auth_id=auth_id, c=str(c))

    def VerifyAuthentication(self, request, context):
        """
        Handle authentication verification request.

        Args:
            request (zkp.AuthenticationAnswerRequest): Authentication answer request.
            context (grpc.ServicerContext): gRPC context for handling the request.

        Returns:
            zkp.AuthenticationAnswerResponse: Response indicating authentication status.
        """
        logger.info(f"Received authentication answer request for request {request}")

        auth_id = request.auth_id
        auth_session = self.activeAuthSessionsDBMap.get(auth_id)
        user = self.userDBMap.get(auth_session.userName)
        s = Decimal(request.s)

        if s >= 0:
            exp1 = ((Decimal(constants.G) ** s) * (user.y1 ** auth_session.c))
            exp2 = ((Decimal(constants.H) ** s) * (user.y2 ** auth_session.c))
        else:
            exp1 = ((user.y1 ** auth_session.c) / (Decimal(constants.G) ** abs(s)))
            exp2 = ((user.y2 ** auth_session.c) / (Decimal(constants.H) ** abs(s)))

        if AuthServicer.isEqual(exp1,auth_session.r1) and AuthServicer.isEqual(exp2, auth_session.r2):
            return zkp.AuthenticationAnswerResponse(session_id=auth_session.sessionId)
        else:
            return zkp.AuthenticationAnswerResponse(session_id="INVALID")

def serve():
    """
    Start the gRPC server and serve authentication operations.
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    zkp_grpc.add_AuthServicer_to_server(AuthServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
