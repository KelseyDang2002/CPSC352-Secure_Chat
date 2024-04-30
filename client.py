import socket
import sys
from sendReceive import sendData
from users import clientAuthenticateUser
from secureChat import clientSecureChat
from userStatus import clientUserStatus, clientUserStatusAll


# Main function, called at the end
def main():
    if len(sys.argv) < 3:
        print(
            "\nCorrect format: python3",
            sys.argv[0],
            "<server hostname> <server port>\n",
        )
        print("Default format: python3", sys.argv[0], "127.0.0.1 1235\n")
    else:
        host = sys.argv[1]
        port = int(sys.argv[2])
        connSock = controlCONN(host, port)

    # Log in User
    authenticated = False
    while not authenticated:
        authenticated, username = clientAuthenticateUser(connSock)

    print("\nUser authenticated. Welcome ", username)

    # Show menu
    menuCMD()

    # User terminal command handling
    while True:
        userInput = input("\nSecChat> ").split()
        if len(userInput) > 1:
            command = userInput[0]
            userName = userInput[1]
        elif len(userInput) == 1:
            command = userInput[0]
        else:
            print("\nPlease provide a command.")
            print("Type 'menu' for a list of appropriate commands")
            continue
        if command == "menu":
            menuCMD()
        elif command == "chat":
            if len(userInput) == 2:
                clientSecureChat(connSock, userName)
            else:
                print("invalid input: please provide a username")
        elif command == "status":
            if len(userInput) == 2:
                clientUserStatus(connSock, userName)
            else:
                print("invalid input: please provide a username")
        elif command == "all":
            clientUserStatusAll(connSock)
        elif command == "quit":
            quit(connSock)
            break
        else:
            print("\nInvalid command.")
            print("Type 'menu' for a list of appropriate commands")

    connSock.close()
    print("Control connection to the Secure Chat server closed.\n")
    print("Bye :D\n")
    return


# Control connection function
def controlCONN(host, port):
    connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(f"\nConnecting to the Secure Chat server: ({host}, {port})\n")
    connSock.connect((host, port))
    print("Control connection to the Secure Chat server successful.")
    return connSock


# Send quit command to server to let server know contoll connection has ended
def quit(connSock):
    sendData(connSock, "quit")
    return


# Function controlling menu command
def menuCMD():
    print("\nClient Main Menu:\n")
    print("menu - list commands")
    print("chat <username> - initiate secure chat with provided user")
    print("status <username> - check if provided user is online")
    print("all - list status of all registered users")
    print("quit - exit the connection")
    return


main()
