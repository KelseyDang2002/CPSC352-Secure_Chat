# Secure Chat

## Members

- Michael Carey
- Alejandro Guerrero
- Kyle Chan
- Eric Licea
- Samir Shivji
- Michael Rojas
- Kelsey Dang

## Requirements

pip3 install bcrypt

pip3 install cryptodomex

## Project Instructions

In this project you are to implement a system which enables a group of users to chat securely. All users are registered with the chat server. When the user wants to chat with another registered user, he first connects to the chat server and enters his/her user name and password. The server verifies the user name and password, and if correct, the user’s status is changed to “online“. Next, the user may enter the user ids of users with whom he wishes to chat (could be more then one). At any given time the user should be able to check what other users are online and invite them to the ongoing conversation.

Once the user specifies the users with whom he wishes to chat, the server generates a symmetric key, and securely distributes it to all the specified users and the user who initiated the chat. To achieve secure key distribution you must encrypt the symmetric key using the public keys of the respective users (you may assume that server knows the public keys of all users). If one of the specified users is not online, the requesting user is notified about this.

After the encrypted symmetric key has been distributed to all users, the users decrypt the symmetric key using their private keys, and the chat session may begin. All messages exchanged during the chat must be encrypted using the symmetric key provided by the server and must be delivered to all users participating in the chat. Any user may choose to leave the conversation. If the user disconnects from the chat server, his status should be changed to “offline“. All users who are connected to the server, must have a way to check whether a given user is online. You do not need to support multiple chat sessions.

Your implementation must provide both confidentiality and digital signature. For digital signature you must provide the user with a choice of using RSA or Digital Signature Algorithm (DSA; https://bit.ly/2TvvGSt). Both must digital signature schemes must be supported.

## How To Use Secure Chat 

### Running The Server

1. Navigate to the "/CPSC352-Secure_Chat" directory.
2. Type the following command in the terminal to run the server:
```console
python3 server.py
```

### Connecting As Client(s)

1. Open a separate terminal for the desired number of clients/users (at least 2 for communication).
2. Navigate to the "/CPSC352-Secure_Chat" directory.
3. Type the following command in the terminal to connect client to the server:
```console
python3 client.py
```
4. After the client establishes a connection, they are prompted with the following:
```console
Enter your username:
```
5. Enter the username of a registered user and the corresponding password.
```console
Enter your username: user1
Enter your password: password1
```

#### List Of Registered Users

```console
Username:       Password:
-------------------------
user1           password1
user2           password2
user3           password3
user4           password4
user5           password5
```
6. After successful authentication, the user is greeted with the client menu.

### Client Menu

1. After successful authentication, the user is greeted with the client menu.
```console
Menu:
	1. chat <users> - Start a chat and invite specified users (e.g., chat user2 user3)
	2. status <username> - Check if a user is online (e.g., status user1)
	3. all - List all online users
	4. join - Join the chat room
	5. quit - Quit the application

Enter your choice: 
```
2. From the menu, the user can choose the following commands:

#### "chat" Command
The "chat" command starts a chat room invites one other specified user.
Command line example:
```console
Enter your choice: chat user2
```
RSA Encryption/Decryption:
1. Before joining the chat room, the user is prompted to decrpyt a message using their private key and enter the decrypted key.
```console
Decrypt the following message using your private key:
b'C\xda\xd4\x00\xaf\x14/`|\x0b\xc0\x92*GOug\xd6\x91\xc1\x066\xc8\xe2c\xacA\x85!\xc1\x9c\xe2\xe5\x15\xe6\xf2)\x17\x88\x9b&M\x08S\xcb\x9c\xb0\xea\xb04\x18\x84\xb4ond;N\x0c\xcd\xb2q\x13\xfd\x92\xf2\xb5\x7f\xab\t!\\\xfb\x12\xd0.\x91\xc9\x0f\xcf7\x01+\xb2\x87\xa7\xdf\xe6\xb1\x02\x85\xab+6@\xac\xed\x1d\x04\x03\xf5h%*\x94}\x93V\x83\xd44\xe2\x1ar\xed\xc7{\xdc\xe9\xca\xe18\xe9\xcbH\x87\x17\x11'
Please enter the decrypted key:
```
2. To decrypt, open another terminal and navigate to "/CPSC352-Secure_Chat/user_keys" directory.
3. Type the following command in the terminal to run RSA decryption:
```console
python3 rsa_decryption.py
```
4. The user should be prompted with the following:
```console
Please enter the data you would like to decrypt:
```
5. Enter the encrypted data provided in the client terminal by copying and pasting.
```console
Please enter the data you would like to decrypt: b'C\xda\xd4\x00\xaf\x14/`|\x0b\xc0\x92*GOug\xd6\x91\xc1\x066\xc8\xe2c\xacA\x85!\xc1\x9c\xe2\xe5\x15\xe6\xf2)\x17\x88\x9b&M\x08S\xcb\x9c\xb0\xea\xb04\x18\x84\xb4ond;N\x0c\xcd\xb2q\x13\xfd\x92\xf2\xb5\x7f\xab\t!\\\xfb\x12\xd0.\x91\xc9\x0f\xcf7\x01+\xb2\x87\xa7\xdf\xe6\xb1\x02\x85\xab+6@\xac\xed\x1d\x04\x03\xf5h%*\x94}\x93V\x83\xd44\xe2\x1ar\xed\xc7{\xdc\xe9\xca\xe18\xe9\xcbH\x87\x17\x11'
Please input your username:
```
6. Then enter the username of the user to receive the decrypted key.
```console
Please enter the data you would like to decrypt: b'C\xda\xd4\x00\xaf\x14/`|\x0b\xc0\x92*GOug\xd6\x91\xc1\x066\xc8\xe2c\xacA\x85!\xc1\x9c\xe2\xe5\x15\xe6\xf2)\x17\x88\x9b&M\x08S\xcb\x9c\xb0\xea\xb04\x18\x84\xb4ond;N\x0c\xcd\xb2q\x13\xfd\x92\xf2\xb5\x7f\xab\t!\\\xfb\x12\xd0.\x91\xc9\x0f\xcf7\x01+\xb2\x87\xa7\xdf\xe6\xb1\x02\x85\xab+6@\xac\xed\x1d\x04\x03\xf5h%*\x94}\x93V\x83\xd44\xe2\x1ar\xed\xc7{\xdc\xe9\xca\xe18\xe9\xcbH\x87\x17\x11'
Please input your username: user1
Decrypted:
b'i\xb0\x00\xd8\x89\x88\x93MI\xcc\xeb\x1cI>\xf1\x9e'
```
7. Return to the client terminal.
8. Copy and paste the decrypted key to finally gain access to to join the caht room.
```console
Decrypt the following message using your private key:
b'C\xda\xd4\x00\xaf\x14/`|\x0b\xc0\x92*GOug\xd6\x91\xc1\x066\xc8\xe2c\xacA\x85!\xc1\x9c\xe2\xe5\x15\xe6\xf2)\x17\x88\x9b&M\x08S\xcb\x9c\xb0\xea\xb04\x18\x84\xb4ond;N\x0c\xcd\xb2q\x13\xfd\x92\xf2\xb5\x7f\xab\t!\\\xfb\x12\xd0.\x91\xc9\x0f\xcf7\x01+\xb2\x87\xa7\xdf\xe6\xb1\x02\x85\xab+6@\xac\xed\x1d\x04\x03\xf5h%*\x94}\x93V\x83\xd44\xe2\x1ar\xed\xc7{\xdc\xe9\xca\xe18\xe9\xcbH\x87\x17\x11'
Please enter the decrypted key: b'i\xb0\x00\xd8\x89\x88\x93MI\xcc\xeb\x1cI>\xf1\x9e'
Entering chat room...
Joining chat room...
user1 has joined the chat room!

```

#### "status" Command
The "status" command checks if a specified user is online.
Command line example:
```console
Enter your choice: status user3
```

#### "all" Command
The "all" command lists all online users that are connected to the server.
Command line example:
```console
Enter your choice: all
```

#### "join" Command
The "join" command allows the user to join the chat room if there are other users in it or create a chat room if there isn't already one.
Command line example:
```console
Enter your choice: join
```
RSA Encryption/Decryption:
1. Before joining the chat room, the user is prompted to decrpyt a message using their private key and enter the decrypted key.
```console
Decrypt the following message using your private key:
b'C\xda\xd4\x00\xaf\x14/`|\x0b\xc0\x92*GOug\xd6\x91\xc1\x066\xc8\xe2c\xacA\x85!\xc1\x9c\xe2\xe5\x15\xe6\xf2)\x17\x88\x9b&M\x08S\xcb\x9c\xb0\xea\xb04\x18\x84\xb4ond;N\x0c\xcd\xb2q\x13\xfd\x92\xf2\xb5\x7f\xab\t!\\\xfb\x12\xd0.\x91\xc9\x0f\xcf7\x01+\xb2\x87\xa7\xdf\xe6\xb1\x02\x85\xab+6@\xac\xed\x1d\x04\x03\xf5h%*\x94}\x93V\x83\xd44\xe2\x1ar\xed\xc7{\xdc\xe9\xca\xe18\xe9\xcbH\x87\x17\x11'
Please enter the decrypted key:
```
2. To decrypt, open another terminal and navigate to "/CPSC352-Secure_Chat/user_keys" directory.
3. Type the following command in the terminal to run RSA decryption:
```console
python3 rsa_decryption.py
```
4. The user should be prompted with the following:
```console
Please enter the data you would like to decrypt:
```
5. Enter the encrypted data provided in the client terminal by copying and pasting.
```console
Please enter the data you would like to decrypt: b'C\xda\xd4\x00\xaf\x14/`|\x0b\xc0\x92*GOug\xd6\x91\xc1\x066\xc8\xe2c\xacA\x85!\xc1\x9c\xe2\xe5\x15\xe6\xf2)\x17\x88\x9b&M\x08S\xcb\x9c\xb0\xea\xb04\x18\x84\xb4ond;N\x0c\xcd\xb2q\x13\xfd\x92\xf2\xb5\x7f\xab\t!\\\xfb\x12\xd0.\x91\xc9\x0f\xcf7\x01+\xb2\x87\xa7\xdf\xe6\xb1\x02\x85\xab+6@\xac\xed\x1d\x04\x03\xf5h%*\x94}\x93V\x83\xd44\xe2\x1ar\xed\xc7{\xdc\xe9\xca\xe18\xe9\xcbH\x87\x17\x11'
Please input your username:
```
6. Then enter the username of the user to receive the decrypted key.
```console
Please enter the data you would like to decrypt: b'C\xda\xd4\x00\xaf\x14/`|\x0b\xc0\x92*GOug\xd6\x91\xc1\x066\xc8\xe2c\xacA\x85!\xc1\x9c\xe2\xe5\x15\xe6\xf2)\x17\x88\x9b&M\x08S\xcb\x9c\xb0\xea\xb04\x18\x84\xb4ond;N\x0c\xcd\xb2q\x13\xfd\x92\xf2\xb5\x7f\xab\t!\\\xfb\x12\xd0.\x91\xc9\x0f\xcf7\x01+\xb2\x87\xa7\xdf\xe6\xb1\x02\x85\xab+6@\xac\xed\x1d\x04\x03\xf5h%*\x94}\x93V\x83\xd44\xe2\x1ar\xed\xc7{\xdc\xe9\xca\xe18\xe9\xcbH\x87\x17\x11'
Please input your username: user1
Decrypted:
b'i\xb0\x00\xd8\x89\x88\x93MI\xcc\xeb\x1cI>\xf1\x9e'
```
7. Return to the client terminal.
8. Copy and paste the decrypted key to finally gain access to to join the caht room.
```console
Decrypt the following message using your private key:
b'C\xda\xd4\x00\xaf\x14/`|\x0b\xc0\x92*GOug\xd6\x91\xc1\x066\xc8\xe2c\xacA\x85!\xc1\x9c\xe2\xe5\x15\xe6\xf2)\x17\x88\x9b&M\x08S\xcb\x9c\xb0\xea\xb04\x18\x84\xb4ond;N\x0c\xcd\xb2q\x13\xfd\x92\xf2\xb5\x7f\xab\t!\\\xfb\x12\xd0.\x91\xc9\x0f\xcf7\x01+\xb2\x87\xa7\xdf\xe6\xb1\x02\x85\xab+6@\xac\xed\x1d\x04\x03\xf5h%*\x94}\x93V\x83\xd44\xe2\x1ar\xed\xc7{\xdc\xe9\xca\xe18\xe9\xcbH\x87\x17\x11'
Please enter the decrypted key: b'i\xb0\x00\xd8\x89\x88\x93MI\xcc\xeb\x1cI>\xf1\x9e'
Entering chat room...
Joining chat room...
user1 has joined the chat room!

```

#### "quit" Command
The "quit" command 
Command line example:
```console
Enter your choice: quit 
```
