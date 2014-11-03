from encryption import *
from entry import *

class JournalEncryptor(Encryptor):
    def encrypt_entry(self, entry):
        return self.encrypt('' + entry.created_at.strftime("%Y-%m-%d %H:%M:%S.%f") + '\n' + entry.body)


class JournalDecryptor(Decryptor):
    def decrypt_entry(self, encrypted_entry):
        plain_text = self.decrypt(encrypted_entry)
        stream = StringIO.StringIO(plain_text)
        date = stream.readline().rstrip()
        text = stream.read()

        return Entry(text, datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f"))
