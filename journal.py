import hashlib
import uuid
from operator import attrgetter
from Colors import Colors


class Journal(object):
    def __init__(self, name, entries=[], identifier=None):
        self.name = name
        self.entries = entries

        if identifier is None:
            salt = uuid.uuid4().hex
            self.identifier = hashlib.sha256(name + salt).hexdigest()
        else:
            self.identifier = identifier

    def add_entry(self, entry):
        if self.entries is None:
            self.entries = []

        self.entries.append(entry)

    def __eq__(self, other):
        return self.name == other.name and self.identifier == other.identifier

    def __str__(self):
        message = ""
        self.entries = sorted(self.entries, key=attrgetter('created_at'))

        for entry in self.entries:
            message += Colors.BLUE + entry.created_at.strftime("%Y-%m-%d %H:%M:%S.%f") + Colors.ENDC + '\n' + \
                       entry.body.splitlines()[0][0:80] + '\n\n'
        return message