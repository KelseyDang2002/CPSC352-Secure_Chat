from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import os


def rsa_encrypt_data(data, alias):   
    filename = "public_" + alias + ".pem"
    file_path = os.path.join("server_keys", filename)
    with open (file_path, "rb") as pub_file:
        contents = pub_file.read()
        puKey = RSA.importKey(contents)
    cipher = PKCS1_v1_5.new(puKey)
    ciphertext = cipher.encrypt(data)
    return ciphertext


if __name__ == "__main__":
    data = input("Please enter the data you would like to decrypt: ")
    username = input("Please input your username: ")

    rsa_encrypt_data(data, username)