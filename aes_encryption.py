from Cryptodome.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad


# Function to encrypt the data
def aes_encrypt_data(data, key):
    encCipher = AES.new(key, AES.MODE_ECB)
    msgBytes = data.encode('utf-8')
    paddedMsg = pad(msgBytes, AES.block_size)
    cipherText = encCipher.encrypt(paddedMsg)

    return cipherText

# Function to decrypt the data
def aes_decrypt_data(cipherText, key):
    decCipher = AES.new(key, AES.MODE_ECB)
    plainText = decCipher.decrypt(cipherText)
    plainText = unpad(plainText, AES.block_size)
    plainText = plainText.decode('utf-8')
    
    return plainText