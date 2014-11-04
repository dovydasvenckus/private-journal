import sys
sys.path.append("..")
import unittest
from journal_encryption import *
from Crypto.PublicKey import RSA
import os


class EntriesEncryptionTests(unittest.TestCase):

    def setUp(self):
        new_key = RSA.generate(1024)
        self.public_key = new_key.publickey()
        self.private_key = new_key

        self.encryptor = JournalEncryptor(self.public_key)
        self.decryptor = JournalDecryptor(self.private_key)
        self.entry = Entry("Some random text")

        self.path = 'test/'
        self.file_name = 'encryped_entry'

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