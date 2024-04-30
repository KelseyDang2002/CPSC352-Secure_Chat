import ast
from sendReceive import sendData, recvAll
import bcrypt

# Dictionary to store user credentials
USER_CREDENTIALS = {}

# Create user credentials and store the hashed passwords
count = 1
while count < 6:
    password = "password" + str(count)
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    USER_CREDENTIALS["user" + str(count)] = bcrypt.hashpw(bytes, salt)
    count += count

# Dictionary to store user online status
USER_STATUS = {}

# Dictionary to store user sockets
USER_SOCKETS = {}


# Client side user authentication function
def clientAuthenticateUser(servSock):
    authenticated = False

    print("Please login to access the Secure Chat server...\n")
    username = input("username: ")
    password = input("password: ")
    user_pass = username + " " + password
    sendData(servSock, user_pass)

    resSize = recvAll(servSock, 10)
    response = recvAll(servSock, int(resSize.decode()))
    response = response.decode()

    authenticated = ast.literal_eval(response)

    if not authenticated:
        print("\nInvalid username or password. Please try again.\n")

    return authenticated, username


# Server side user authentication function
def serverAuthenticateUser(cliSock):
    authenticated_user = False
    dataSize = str()
    username = str()
    password = str()
    user_pass = str()

    dataSize = recvAll(cliSock, 10)
    user_pass = recvAll(cliSock, int(dataSize.decode())).decode("utf-8")

    user_pass = user_pass.split()
    username = user_pass[0]
    password = user_pass[1]

    passBytes = password.encode("utf-8")

    if username in USER_CREDENTIALS.keys():
        if bcrypt.checkpw(passBytes, USER_CREDENTIALS.get(username)):
            authenticated_user = True

            USER_STATUS[username] = "online"
            USER_SOCKETS[username] = cliSock

    sendData(cliSock, authenticated_user)

    return authenticated_user, username
