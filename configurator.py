import ConfigParser


class Configurator(object):

    def __init__(self, path, section):
        self.path = path
        self.section = section

    def get_keys_paths(self):
        config = ConfigParser.ConfigParser()
        config.read(self.path)
        private_key_path = config.get(self.section, 'private_key')
        public_key_path = config.get(self.section, 'public_key')

        return private_key_path, public_key_path