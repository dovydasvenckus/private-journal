import sys
sys.path.append("..")
import unittest
from encryption import *
from Crypto.PublicKey import RSA


class EncryptionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        new_key = RSA.generate(1024) 
        cls.public_key = new_key.publickey()
        cls.private_key = new_key
        
        cls.encryptor = Encryptor(cls.public_key)
        cls.decryptor = Decryptor(cls.private_key)
        cls.plain = 'Random text'

    def test_cipther_text_differs_from_plain(self):
        ciphertext = self.encryptor.encrypt(self.plain)
        self.assertNotEqual(self.plain, ciphertext) 

    def test_encryption_should_be_lossless(self):
        ciphertext = self.encryptor.encrypt(self.plain)
        decrypted_text = self.decryptor.decrypt(ciphertext)
        self.assertEqual(self.plain, decrypted_text)

