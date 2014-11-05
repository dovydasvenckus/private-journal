import sys
sys.path.append("..")
import unittest
from journal_encryption import *
from Crypto.PublicKey import RSA
import os


class EntriesEncryptionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path = 'test/'
        cls.file_name = 'encryped_entry'

        new_key = RSA.generate(1024)
        cls.public_key = new_key.publickey()
        cls.private_key = new_key

        cls.encryptor = JournalEncryptor(cls.public_key)
        cls.decryptor = JournalDecryptor(cls.private_key)
        cls.entry = Entry("Some random text")

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.path + cls.file_name)

    def test_encryption_should_be_lossless(self):
        chipertext = self.encryptor.encrypt_entry(self.entry)
        decrypted_entry = self.decryptor.decrypt_entry(chipertext)
        assert self.entry, decrypted_entry

    def test_encrypted_file_should_be_created(self):
        self.encryptor.encrypt_entry_to_file(self.entry, self.path, self.file_name)
        assert True, os.path.isfile(self.path + self.file_name)

    def test_file_encryption_should_be_losseless(self):
        self.encryptor.encrypt_entry_to_file(self.entry, self.path, self.file_name)
        decryped_entry = self.decryptor.decrypt_entry_from_file(self.path, self.file_name)
        assert decryped_entry, self.entry