import sys
sys.path.append("..")
import unittest
from encryption import *
from Crypto.PublicKey import RSA


class EncryptionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.new_key = RSA.generate(1024)
        cls.public_key = cls.new_key.publickey()
        cls.private_key = cls.new_key
        
        cls.encryptor = Encryptor(cls.public_key)
        cls.decryptor = Decryptor(cls.private_key)
        cls.plain = 'Random text'

        cls.path = 'test/'
        cls.public_key_name = 'public_key'
        cls.private_key_name = 'private_key'

        open(cls.path + cls.public_key_name, 'w').write(cls.public_key.exportKey())
        open(cls.path + cls.private_key_name, 'w').write(cls.private_key.exportKey())

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.path + cls.public_key_name)
        os.remove(cls.path + cls.private_key_name)

    def test_cipther_text_differs_from_plain(self):
        ciphertext = self.encryptor.encrypt(self.plain)
        self.assertNotEqual(self.plain, ciphertext) 

    def test_encryption_should_be_lossless(self):
        ciphertext = self.encryptor.encrypt(self.plain)
        decrypted_text = self.decryptor.decrypt(ciphertext)
        self.assertEqual(self.plain, decrypted_text)

    def test_read_public_key_from_file(self):
        public_key = self.encryptor.read_public_key(self.path + self.public_key_name)
        assert self.public_key, public_key

    def test_read_private_key_from_file(self):
        private_key = self.decryptor.read_private_key(self.path + self.private_key_name)
        assert self.private_key, private_key