import sys
sys.path.append("..")
import unittest
from journal_encryption import *
from Crypto.PublicKey import RSA
import os
import glob


class EntriesEncryptionTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.path = 'testData/'
        cls.file_name = 'encryped_entry'
        cls.journal_name = ".journal"

        new_key = RSA.generate(1024)
        cls.public_key = new_key.publickey()
        cls.private_key = new_key

        cls.encryptor = JournalEncryptor(cls.public_key)
        cls.decryptor = JournalDecryptor(cls.private_key)
        cls.journal = Journal("Journal", None)

        cls.entry = Entry("Some random text", None, cls.journal.identifier)

        if not os.path.exists(cls.path):
            os.mkdir(cls.path)


    @classmethod
    def tearDownClass(cls):
        os.remove(cls.path + cls.file_name)
        os.remove(cls.path + cls.journal_name)
        os.chdir(cls.path)
        for file in glob.glob("*.entry"):
            os.remove(file)
        os.chdir('..')

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

    def test_file_name_should_be_generated(self):
        file_name = self.encryptor.encrypt_entry_to_file(self.entry, self.path)
        assert True, os.path.isfile(self.path + file_name)

    def test_journal_encryption_should_be_loseless(self):
        encrypted_journal = self.encryptor.encrypt_journal(self.journal)
        assert encrypted_journal, self.decryptor.decrypt_journal(encrypted_journal)

    def test_journal_should_be_loseless_after_reading_from_file(self):
        self.encryptor.encrypt_journal_to_file(self.journal, self.path)
        decrypted_journal = self.decryptor.decrypt_journal_from_file(self.path)
        assert decrypted_journal, self.journal

if __name__  == '__main__':
    unittest.main()
