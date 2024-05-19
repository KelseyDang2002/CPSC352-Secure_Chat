from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def rsa_decrypt_data(data, prKey):
    cipher = PKCS1_v1_5.new(prKey)
    plaintext = cipher.decrypt(data, 1000)
    print("Decrypted: ", plaintext)

if __name__ == "__main__":
    data = input("Please enter the data you would like to decrypt: ")
    username = input("Please input your username: ")
    filename = "private_" + username + ".pem"
    print(type(filename))
    print (filename)
    with open (filename, "rb") as pub_file:
        contents = pub_file.read()
        puKey = RSA.importKey(contents)

    rsa_decrypt_data(data, puKey)
