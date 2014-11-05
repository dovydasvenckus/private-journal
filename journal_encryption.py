from encryption import *
from entry import *

class JournalEncryptor(Encryptor):
    def encrypt_entry(self, entry):
        return self.encrypt('' + entry.created_at.strftime("%Y-%m-%d %H:%M:%S.%f") + '\n' + entry.body)

    def encrypt_entry_to_file(self, entry, path='', name=None):
        if name is None:
            name = os.urandom(16).encode('hex') + '.entry'

        file = open(path + name, 'w')
        file.write(self.encrypt_entry(entry))
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
