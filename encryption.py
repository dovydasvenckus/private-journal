import os
from Crypto.Cipher import AES
import Crypto.Util.number
import StringIO

BLOCK_SIZE = 16
IV = '\x00' * 16


class Encryptor(object):
    def __init__(self, rsa_public_key):
        self.rsa_public_key = rsa_public_key

    def encrypt(self, data):
        secret_key = os.urandom(BLOCK_SIZE)
        padding = self.generate_padding(secret_key)
        encrypted_secret_key = self.rsa_public_key.encrypt(padding + secret_key, None)[0]

        return self.generate_encrypted_header(encrypted_secret_key) + self.encrypt_data(data, secret_key)

    def generate_padding(self, key):
        plaintext_length = (Crypto.Util.number.size(self.rsa_public_key.n) - 2) / 8
        padding = '\xff' + os.urandom(BLOCK_SIZE)
        padding += '\0' * (plaintext_length - len(padding) - len(key))

        return padding

    def encrypt_data(self, data, key):
        aes_engine = AES.new(key, AES.MODE_CBC, IV)
        return aes_engine.encrypt(data + '\0' * (0 if len(data) % BLOCK_SIZE == 0 else BLOCK_SIZE - len(data) % BLOCK_SIZE))

    def generate_encrypted_header(self, encrypted_key):
        return str(len(encrypted_key)) + "\n" + encrypted_key


class Decryptor(object):
    def __init__(self, rsa_private_key):
        self.rsa_private_key = rsa_private_key

    def decrypt(self, encrypted_msg):
        key_lenght, encrypted_key, ciphertext = self.parse_encrypted_message(encrypted_msg)
        padded_key = self.rsa_private_key.decrypt(encrypted_key)
        key = self.remove_padding(padded_key)
        aes_engine = AES.new(key, AES.MODE_CBC, IV)

        return aes_engine.decrypt(ciphertext).rstrip('\0')

    def parse_encrypted_message(self, encrypted_msg):
        input = StringIO.StringIO(encrypted_msg)

        key_lenght = input.readline()
        encrypted_key = input.read(int(key_lenght))
        ciphertext = input.read()

        return key_lenght, encrypted_key, ciphertext

    def remove_padding(self, padded_key):
        padded_key_list = list(padded_key)
        key_start_point = None

        if padded_key_list[0] == '\xff':
            for i in range(1 + BLOCK_SIZE, len(padded_key_list)):
                if padded_key_list[i] != '\0':
                    key_start_point = i
                    break

        return padded_key[key_start_point:]