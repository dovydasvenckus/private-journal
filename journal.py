import hashlib
import uuid


class Journal(object):
    def __init__(self, name, entries=None, identifier=None):
        self.name = name
        self.entries = entries

        if identifier is None:
            salt = uuid.uuid4().hex
            self.identifier = hashlib.sha256(name + salt).hexdigest()

    def __eq__(self, other):
        return self.name == other.name and self.identifier == other.identifier