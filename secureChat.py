from sendReceive import sendData, recvAll
from getUserName import getUserName


# Client-side function to create the secure chat between users
def clientSecureChat(connSock, userName):
    sendData(connSock, "chat")
    sendData(connSock, userName)
    data = str()
    dataSize = str()
    dataSize = recvAll(connSock, 10)
    data = recvAll(connSock, int(dataSize.decode()))
    data = data.decode("utf-8")
    print(f"\n{data}\n")
    return


# Server-side function to setup secure chat
def serverSecureChat(clientSock, addr):
    userName = getUserName(clientSock)
    data = "Secure Chat functionality under construction"
    sendData(clientSock, data)
    print("Secure Chat functionality under construction.\n")
    return
