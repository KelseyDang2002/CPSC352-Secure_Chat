from authentication import authenticate
from chat_handler import handle_chat
from message_utils import send_message, receive_message
from rsa_encryption import rsa_encrypt_data
import os

# First it authenticates the user.
# Once authenticated, adds user to the clients dictionary {user : socket}
# Once loop starts, it checks for commands. 
# Chat checks if possible to that withh users. If successfull the user will enter the chat room.
# Currently no way to escape the chat room.

def handle_commands(client, address, clients, chat_room):
    # Generate a key
    key = os.urandom(16)
    alias = authenticate(client)
    if alias:
        clients[alias] = client
        print(f'The alias of this client is {alias}')
        while True:
            send_message(client, 'Enter a command '.encode('utf-8'))
            command = receive_message(client).decode('utf-8').strip()

            if command.startswith('chat '):
                users_to_invite = command.split(' ')[1:]
                users_online = [user for user in users_to_invite if user in clients]
                users_offline = [user for user in users_to_invite if user not in clients]

                if users_offline:
                    send_message(client, f'These users are not online: {", ".join(users_offline)}'.encode('utf-8'))
                else:
                    rsa_key = str(rsa_encrypt_data(key, alias))
                    send_message(client, rsa_key.encode('utf-8'))
                    key_response = receive_message(client).decode('utf-8')
                    if key_response == key:
                        chat_room.append(alias)
                        send_message(client, 'Entering chat room...'.encode('utf-8'))
                        for user in users_online:
                            send_message(clients[user], f'\n{alias} has invited you to the chat room. Type "join" to join'.encode('utf-8'))
                        handle_chat(client, alias, clients, chat_room)
                        break
                
            elif command == 'join':
                if alias not in chat_room:
                    

                    chat_room.append(alias)
                    send_message(client, 'Joining chat room...'.encode('utf-8'))
                    handle_chat(client, alias, clients, chat_room)
                    break
                else:
                    send_message(client, 'You are already in the chat room.'.encode('utf-8'))
            elif command.startswith('status '):
                target_user = command.split(' ')[1]
                if target_user in clients:
                    send_message(client, f'{target_user} is online.'.encode('utf-8'))
                else:
                    send_message(client, f'{target_user} is not online.'.encode('utf-8'))
            elif command == 'all':
                online_users = ', '.join(clients.keys())
                send_message(client, f'Online users: {online_users}'.encode('utf-8'))
            elif command == 'quit':
                client.close()
                break  # Exit the loop after closing the client socket
            else:
                send_message(client, 'Invalid command. Try again.'.encode('utf-8'))
