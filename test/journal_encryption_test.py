import sys
sys.path.append("..")
import unittest
from journal_encryption import *
from Crypto.PublicKey import RSA

class EntriesEncryptionTests(unittest.TestCase):
    def setUp(self):
        new_key = RSA.generate(1024)
        self.public_key = new_key.publickey()
        self.private_key = new_key

        self.encryptor = JournalEncryptor(self.public_key)
        self.decryptor = JournalDecryptor(self.private_key)
        self.entry = Entry("Some random text")

    def test_encryption_should_be_loseless(self):
        chipertext = self.encryptor.encrypt_entry(self.entry)
        decrypted_entry = self.decryptor.decrypt_entry(chipertext)
        print decrypted_entry
        assert self.entry, decrypted_entry