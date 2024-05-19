from Cryptodome.Cipher import AES
import os

# Function to encrypt the data
def encrypt_data(data, key):
    data = pad(data)
    encCipher = AES.new(key, AES.MODE_ECB)
    cipherText = encCipher.encrypt(data)
    
    return cipherText

# Function to decrypt the data
def decrypt_data(cipherText, key):
    decCipher = AES.new(key, AES.MODE_ECB)
    plainText = decCipher.decrypt(cipherText)
    plainText = unpad(plainText)
    
    return plainText

# Function to pad data to make its length a multiple of 16
def pad(data):
    padding = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([padding] * padding)

# Function to remove padding from data
def unpad(data):
    padding = data[-1]
    return data[:-padding]

def generateKey():
    key = os.urandom(16)
    return key
