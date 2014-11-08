from encryption import *
from entry import *
from journal import *
import hashlib
import uuid

FILE_EXTENSION = '.entry'
JOURNAL_FILE_NAME = '.journal'


class JournalEncryptor(Encryptor):
    def encrypt_entry(self, entry):
        return self.encrypt('' + entry.created_at.strftime("%Y-%m-%d %H:%M:%S.%f") + '\n' + entry.body)

    def encrypt_entry_to_file(self, entry, path='', name=None):
        if name is None:
            salt = uuid.uuid4().hex
            name = hashlib.sha256(
                entry.created_at.strftime("%Y-%m-%d %H:%M:%S.%f") + salt).hexdigest() + FILE_EXTENSION

        file = open(path + name, 'w')
        file.write(self.encrypt_entry(entry))
        file.close()

        return name

    def encrypt_journal(self, journal):
        return self.encrypt(journal.name + '\n' + journal.identifier)

    def encrypt_journal_to_file(self, journal, path='', name=None):
        if name is None:
            name = JOURNAL_FILE_NAME

        file = open(path + name, 'w')
        file.write(self.encrypt_journal(journal))
        file.close()

        return name


class JournalDecryptor(Decryptor):
    def decrypt_entry(self, encrypted_entry):
        plain_text = self.decrypt(encrypted_entry)
        stream = StringIO.StringIO(plain_text)
        date = stream.readline().rstrip()
        text = stream.read()

        return Entry(text, datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f"))

    def decrypt_entry_from_file(self, path, name):
        encrypted_message = open(path + name).read()

        return self.decrypt_entry(encrypted_message)

    def decrypt_journal(self, encrypted_journal):
        plain_text = self.decrypt(encrypted_journal)
        stream = StringIO.StringIO(plain_text)
        name = stream.readline().rstrip()
        identifier = stream.read()

        return Journal(name, None, identifier)

    def decrypt_journal_from_file(self, path='', name=JOURNAL_FILE_NAME):
        encrypted_message = open(path + name).read()

        return self.decrypt_journal(encrypted_message)
