import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import Crypto.Util.number

BLOCK_SIZE = 16
IV = '\x00' * 16

def encrypt_file(rsa, input, output):
    # Generate secret key
    secret_key = os.urandom(BLOCK_SIZE)
    
    # Padding 
    plaintext_length = (Crypto.Util.number.size(rsa.n) - 2) / 8
    padding = '\xff' + os.urandom(BLOCK_SIZE)
    padding += '\0' * (plaintext_length - len(padding) - len(secret_key))

    # Encrypt the secret key with RSA
    encrypted_secret_key = rsa.encrypt(padding + secret_key, None)[0]

    # Write out the encrypted secret key, preceded by a length indication
    output.write(str(len(encrypted_secret_key)) + "\n")
    output.write(encrypted_secret_key)

    # Encrypt the file
    aes_engine = AES.new(secret_key, AES.MODE_CBC, IV)

    data = input.read()
    output.write(aes_engine.encrypt(data + '\0' * (0 if len(data) % BLOCK_SIZE == 0 else BLOCK_SIZE - len(data) % BLOCK_SIZE)))


def decrypt_file(rsa, input):
    key_lenght = input.readline()
    encrypted_key = input.read(int(key_lenght))
    ciphertext = input.read()
    padded_key = rsa.decrypt(encrypted_key)

    padded_key_list = list(padded_key)
    key_start_point = None

    if padded_key_list[0] == '\xff':
        for i in range (1 + BLOCK_SIZE, len(padded_key_list)):
            if padded_key_list[i] != '\0':
                key_start_point = i
                break;
    
    key = padded_key[key_start_point:]
    aes_engine = AES.new(key, AES.MODE_CBC, IV)
    return aes_engine.decrypt(ciphertext)
        
