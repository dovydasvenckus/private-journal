from journal import *
from entry import *
from journal_encryption import *
from sys import argv
import getpass
import editor
import os
import glob
import ConfigParser
from configurator import Configurator


CONFIG_FILE = '.config'
CONFIG_SECTION = 'config'


def first_init():
    config = ConfigParser.ConfigParser()
    os.system('clear')
    print '*' * 8, 'First time setup', '*' * 8
    config.add_section(CONFIG_SECTION)
    private_path_valid = False
    public_path_valid = False 
    
    while not private_path_valid or not public_path_valid:
        
        try:
            if not private_path_valid:
                private_path = raw_input('Please enter valid private key path: ')
                key = open(private_path, "r").read() 
                private_path_valid = True 

            if not public_path_valid and private_path_valid:
                public_path = raw_input ('Please enter valid public key path:')
                key = open(public_path, "r").read()
                public_path_valid = True
        except IOError:
            print "File do not exist"

    config.set(CONFIG_FILE, 'private_key', private_path)
    config.set(CONFIG_FILE, 'public_key', public_path)
    config.set(CONFIG_FILE, 'default_journal', 'journal')
    
    if not os.path.exists('journal'):
        os.makedirs('journal')

    with open(CONFIG_FILE, 'wb') as configfile:
        config.write(configfile)


def main():
    halt = False
    while not halt:
        print argv

        if os.path.exists(CONFIG_FILE):
            configurator = Configurator(CONFIG_FILE, CONFIG_SECTION)
            private_key_path = configurator.private_key_path

            if len(argv) == 3:
                if argv[1] == "list":
                    list(argv[2])
            halt = True

        else:
            first_init()


def list(path):
    configurator = Configurator(CONFIG_FILE, CONFIG_SECTION)
    private_key_path = configurator.private_key_path
    password = getpass.getpass()
    decryptor = JournalDecryptor(None, private_key_path, password)
    journal = decryptor.decrypt_journal_from_file(configurator.default_journal, '.journal')
    print journal.identifier

    os.chdir(path)

    for file in glob.glob('*.entry'):
        entry = decryptor.decrypt_entry_from_file('', file)
        if entry.journal_identifier == journal.identifier:
            journal.add_entry(entry)

    print journal.__str__()


if __name__ == "__main__":
    main()
