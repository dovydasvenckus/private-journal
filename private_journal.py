#!/usr/bin/python

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

    config.set(CONFIG_SECTION, 'private_key', private_path)
    config.set(CONFIG_SECTION, 'public_key', public_path)
    config.set(CONFIG_SECTION, 'default_journal', 'journal')

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

            if len(argv) == 2:
                if argv[1] == "add":
                    add()
                if argv[1] == "list":
                    list()
            elif len(argv) == 3:
                if argv[1] == "list":
                    list(argv[2])

            halt = True

        else:
            first_init()


def list(path=None):
    configurator = Configurator(CONFIG_FILE, CONFIG_SECTION)
    private_key_path = configurator.private_key_path
    password = getpass.getpass()
    decryptor = JournalDecryptor(None, private_key_path, password)

    if path is None:
        path = configurator.default_journal

    journal = decryptor.decrypt_journal_from_file(path, '.journal')
    print journal.identifier

    os.chdir(path)

    for file in glob.glob('*.entry'):
        entry = decryptor.decrypt_entry_from_file('', file)
        if entry.journal_identifier == journal.identifier:
            journal.add_entry(entry)

    print journal.__str__()


def add():
    configurator = Configurator(CONFIG_FILE, CONFIG_SECTION)
    public_key_path = configurator.public_key_path
    encryptor = JournalEncryptor(None, public_key_path)
    decryptor = JournalDecryptor(None, configurator.private_key_path, getpass.getpass())

    journal = decryptor.decrypt_journal_from_file(configurator.default_journal, '.journal')
    body = editor.raw_input_editor()

    if len(body) > 0:
        entry = Entry(body, datetime.datetime.now(), journal.identifier)
        entry.journal_identifier = journal.identifier
        encryptor.encrypt_entry_to_file(entry, configurator.default_journal)
    else:
        print('Entry should not be empty')

if __name__ == "__main__":
    main()
