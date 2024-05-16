import bcrypt
from message_utils import send_message, receive_message

# Predefined users with bcrypt hashed passwords
users = {
    'user1': bcrypt.hashpw('password1'.encode('utf-8'), bcrypt.gensalt()),
    'user2': bcrypt.hashpw('password2'.encode('utf-8'), bcrypt.gensalt()),
    'user3': bcrypt.hashpw('password3'.encode('utf-8'), bcrypt.gensalt()),
    'user4': bcrypt.hashpw('password4'.encode('utf-8'), bcrypt.gensalt()),
    'user5': bcrypt.hashpw('password5'.encode('utf-8'), bcrypt.gensalt()),
}

def authenticate(client):
    while True:
        send_message(client, 'credentials?'.encode('utf-8'))
        credentials = receive_message(client).decode('utf-8')
        username, password = credentials.split(':')
        if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username]):
            return username
        else:
            send_message(client, 'Invalid credentials. Try again.'.encode('utf-8'))
