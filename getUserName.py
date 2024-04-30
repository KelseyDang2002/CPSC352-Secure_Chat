from sendReceive import recvAll


# Get username from client
def getUserName(clientSock):
    userName = str()
    userNameSize = str()
    userNameSize = recvAll(clientSock, 10)
    userName = recvAll(clientSock, int(userNameSize.decode())).decode()
    return userName
