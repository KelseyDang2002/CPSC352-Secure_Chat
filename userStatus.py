from sendReceive import sendData, recvAll
from getUserName import getUserName
from users import USER_STATUS

# Client-side function to check a user's status
def clientUserStatus(connSock, userName):
    sendData(connSock, "status")
    sendData(connSock, userName)
    data = str()
    dataSize = str()
    dataSize = recvAll(connSock, 10)
    data = recvAll(connSock, int(dataSize.decode()))
    data = data.decode("utf-8")
    print(f"\n{data}\n")
    return


# Client-side function to list out all registered users statuses
def clientUserStatusAll(connSock):
    sendData(connSock, "all")
    data = str()
    dataSize = str()
    dataSize = recvAll(connSock, 10)
    data = recvAll(connSock, int(dataSize.decode()))
    data = data.decode("utf-8")
    print(f"\n{data}\n")
    return


# Server-side function to check status of a user
def serverUserStatus(clientSock, addr):
    userName = getUserName(clientSock)
    data = USER_STATUS.get(userName, "offline")
    sendData(clientSock, data)
    print(f"Sent status '{data}' to client {addr} for user '{userName}'\n")
    return


# Server-side function to check status of all registered users
def serverUserStatusAll(clientSock, addr):
    data = str(USER_STATUS)
    sendData(clientSock, data)
    print(f"Sent all user statuses to client {addr}\n")
    return
