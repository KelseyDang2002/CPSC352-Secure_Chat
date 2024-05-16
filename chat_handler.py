from message_utils import send_message, receive_message


# This function sends the message to all users in the chat room.
def broadcast(message, clients, chat_room):
    for alias in chat_room:
        client = clients[alias]
        send_message(client, message.encode('utf-8'))

# This function listens for incoming messages then broadcasts.
def handle_chat(client, alias, clients, chat_room):
    broadcast(f'{alias} has joined the chat room!', clients, chat_room)
    while True:
        try:
            message = receive_message(client)
            if message:
                broadcast(message.decode('utf-8'), clients, chat_room)
            else:
                raise Exception("Client disconnected")
        except:
            if alias in clients:
                del clients[alias]
                client.close()
                chat_room.remove(alias)
                broadcast(f'{alias} has left the chat room!', clients, chat_room)
            break
