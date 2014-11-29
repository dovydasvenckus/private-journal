import datetime


class Entry(object):
    def __init__(self, body, date=None, journal_identifier=''):

        if date is not None:
            self.created_at = date
        else:
            self.created_at = datetime.datetime.now()
        self.body = body
        self.journal_identifier = journal_identifier

    def __str__(self):
        return "CreatedAt: %s\nBody:\n%s" % (self.created_at, self.body)

    def __eq__(self, other):
        return self.body == other.body and self.created_at == other.created_at \
               and self.journal_identifier == other.journal_identifier