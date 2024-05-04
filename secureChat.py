import threading
from sendReceive import sendData, recvAll
from getUserName import getUserName
from encryption import encrypt_data, decrypt_data
from users import USER_STATUS, USER_SOCKETS

chat_room_socks = []
chat_room_users = []


# Client Side
def client_receive(sock):
    while True:
        try:
            messageSize = recvAll(sock, 10)
            message = recvAll(sock, int(messageSize.decode()))
            message = message.decode('utf-8')
            print(message)
        except:
            print('Error!')
            sock.close()
            break


def client_send(sock):
    while True:
        message = f'{input("_>")}'
        sendData(sock, message)


def clientSecureChat(connSock, userName):
    sendData(connSock, "chat")
    sendData(connSock, userName)
    
    # Receive initial response from the server about availability
    dataSize = recvAll(connSock, 10)
    data = recvAll(connSock, int(dataSize.decode()))
    data = data.decode("utf-8")
    print(f"\n{data}\n")

    if "possible" in data:
        userResponse = input("Do you want to start a chat session? (Y/N): ")
        sendData(connSock, userResponse)  # Send response back to server
        
        # Await server response to start chat
        dataSize = recvAll(connSock, 10)
        data = recvAll(connSock, int(dataSize.decode()))
        data = data.decode("utf-8")
        print(f"\n{data}\n")

        if "Starting" in data:
            # Here, you can add code to handle the ongoing chat session
            print("Chat session has started. Type 'quit' to exit.")

            client_receive_thread = threading.Thread(target=client_receive, args=(connSock,))
            client_receive_thread.start()

            client_send_thread = threading.Thread(target=client_receive, args=(connSock,))
            client_send_thread.start()




# Server Side
def broadcast(message):
    for sock in chat_room_socks:
        sendData(sock, message)


def handle_chat(sock):
    while True:
        try:
            messageSize = recvAll(sock, 10)
            message = recvAll(sock, int(messageSize.decode()))
            message = message.decode('utf-8')
            broadcast(message)
        except:
            index = chat_room_socks.index(sock)
            chat_room_socks.remove(sock)
            sock.close()
            user = chat_room_users[index]
            broadcast(f'{user} has left the chat room!'.encode('utf-8'))
            chat_room_users.remove(user)
            break


def serverSecureChat(clientSock, addr):
    userName = getUserName(clientSock)

    if userName in USER_STATUS and USER_STATUS[userName] == 'online':
        print(f'Chatting possible with {userName}.')
        data = f"Chatting with {userName} is possible"
    else:
        print(f"User {userName} is not online.")
        data = 'User is not Online.'
    
    sendData(clientSock, data)

    # Wait for client's response
    responseSize = recvAll(clientSock, 10)
    response = recvAll(clientSock, int(responseSize.decode()))
    response = response.decode("utf-8")

    # Check client's response
    if response.upper() == 'Y':
        print("Starting chat session.")
        sendData(clientSock, "Starting chat session.")
        chat_room_socks.append(clientSock)

        for username, user_sock in USER_SOCKETS.items():
            if user_sock == clientSock:
                chat_room_users.append(username)

        serverChat_thread = threading.Thread(target=handle_chat, args=(clientSock,))
        serverChat_thread.start()
    else:
        print("Chat session canceled by client.")
        sendData(clientSock, "Chat session canceled.")
