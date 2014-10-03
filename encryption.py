import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import Crypto.Util.number

BLOCK_SIZE = 16
IV = '\x00' * 16

class Encryptor(object):
    def __init__(self, rsa):
        self.rsa = rsa

    def encrypt(self, data, output):
                
        self.secret_key = os.urandom(BLOCK_SIZE)

        self.padding = self.generate_padding()

        self.encrypted_secret_key = self.rsa.encrypt(self.padding + self.secret_key, None)[0]

        self.write_encrypted_key(output)

        output.write(self.encrypt_data(data))

    def generate_padding(self):
        plaintext_length = (Crypto.Util.number.size(self.rsa.n) - 2) / 8
        padding = '\xff' + os.urandom(BLOCK_SIZE)
        padding += '\0' * (plaintext_length - len(padding) - len(self.secret_key))
        return padding

    def encrypt_data(self, data):
        aes_engine = AES.new(self.secret_key, AES.MODE_CBC, IV)
        return aes_engine.encrypt(data + '\0' * (0 if len(data) % BLOCK_SIZE == 0 else BLOCK_SIZE - len(data) % BLOCK_SIZE))

    def write_encrypted_key(self, output):
        # Write out the encrypted secret key, preceded by a length indication
        output.write(str(len(self.encrypted_secret_key)) + "\n")
        output.write(self.encrypted_secret_key)

class Decryptor(object):
    def decrypt_file(self, rsa, input):
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
        return aes_engine.decrypt(ciphertext).rstrip()

