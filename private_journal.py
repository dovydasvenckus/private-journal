from journal import *
from entry import *
from sys import argv
from Crypto.PublicKey import RSA 
import editor
import os
import ConfigParser

CONFIG_FILE = '.config'
CONFIG_SECTION = '.config'


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
            config = ConfigParser.ConfigParser()
            config.read(CONFIG_FILE)
            print config.get(CONFIG_SECTION, 'private_key')
            
            if len(argv) == 2:
                if argv[1] == "add":
                    editor.raw_input_editor()              
            halt = True

        else:
            first_init()


if __name__ == "__main__":
    main()
