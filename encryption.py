import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import Crypto.Util.number

def encrypt_file(rsa, input, output):
    block_size = 16
    # Generate secret key
    secret_key = os.urandom(block_size)

    # Padding 
    plaintext_length = (Crypto.Util.number.size(rsa.n) - 2) / 8
    padding = '\xff' + os.urandom(block_size)
    padding += '\0' * (plaintext_length - len(padding) - len(secret_key))

    # Encrypt the secret key with RSA
    encrypted_secret_key = rsa.encrypt(padding + secret_key, None)[0]

    # Write out the encrypted secret key, preceded by a length indication
    output.write(str(len(encrypted_secret_key)) + "\n")
    output.write(encrypted_secret_key)

    # Encrypt the file
    iv = '\x00' * 16
    aes_engine = AES.new(secret_key, AES.MODE_CBC, iv)

    data = input.read()
    output.write(aes_engine.encrypt(data + '\0' * (0 if len(data) % block_size == 0 else block_size - len(data) % block_size)))

