from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import os

def rsa_decrypt_data(data, prv_file):
    cipher = PKCS1_v1_5.new(prv_file)
    plaintext = cipher.decrypt(eval(data), 1000)
    print("Decrypted:")
    print(plaintext)

if __name__ == "__main__":
    data = input("Please enter the data you would like to decrypt: ")
    username = input("Please input your username: ")
    filename = "private_" + username + ".pem"
    file_path = os.path.join("user_keys", filename)
    with open (file_path, "rb") as prv_file:
        contents = prv_file.read()
        prv_file = RSA.importKey(contents)

    rsa_decrypt_data(data, prv_file)
