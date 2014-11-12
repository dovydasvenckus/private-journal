import ConfigParser


class Configurator(object):
    def __init__(self, path, section):
        self.path = path
        self.section = section
        config = ConfigParser.ConfigParser()
        config.read(self.path)
        self.private_key_path = config.get(self.section, 'private_key')
        self.public_key_path = config.get(self.section, 'public_key')
        self.default_journal_path = config.get(self.section, 'default_journal_path')