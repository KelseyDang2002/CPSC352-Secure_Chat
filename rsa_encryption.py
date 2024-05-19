from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


def rsa_encrypt_data(data, puKey):
    cipher = PKCS1_v1_5.new(puKey)
    ciphertext = cipher.encrypt(data.encode())
    print("Ciphertext: ", ciphertext)

def rsa_decrypt_data(data, prKey):
    cipher = PKCS1_v1_5.new(prKey)
    plaintext = cipher.decrypt(data, 1000)
    print("Decrypted: ", plaintext)