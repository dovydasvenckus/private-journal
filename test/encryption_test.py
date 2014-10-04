import sys
sys.path.append("..")
import unittest
from encryption import *
from Crypto.PublicKey import RSA

class EncryptionTests(unittest.TestCase):

    def setUp(self):
        new_key = RSA.generate(1024) 
        self.public_key = new_key.publickey() 
        self.private_key = new_key 
        
        self.encryptor = Encryptor(self.public_key)
        self.decryptor = Decryptor(self.private_key)
        self.plain = 'Random text'

    def test_cipther_text_differs_from_plain(self):
        ciphertext = self.encryptor.encrypt(self.plain)
        self.assertNotEqual(self.plain, ciphertext) 

    def test_encryption_should_be_loseless(self):
        ciphertext = self.encryptor.encrypt(self.plain)
        decrypted_text = self.decryptor.decrypt(ciphertext)
        self.assertEqual(self.plain, decrypted_text)
        
if __name__ == '__main__':
        unittest.main()
