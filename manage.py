#!/usr/bin/env python3
from importlib.machinery import SourceFileLoader
import sys
import string
import os
import re
import moment
from base64 import b64encode, b64decode

from flask.ext.script import Manager, Command, Option, prompt, prompt_bool
from api.__init__ import app, ai, parentdir
from api.app import db as database
from api.tools.krypt import rnd

manager = Manager(app)

manager.help_args = ('-?', '--help')

class Info(Command):
    """ Display Python Version used by this API. """
    def __init__(self):
        self.py_version = ".".join(map(str, sys.version_info[:3]))
        self.intro = 'FLASK CLI Manager: running with Python {}'.format(self.py_version)
        self.root = app.root_path
        # self.heads = "-" * len(self.intro)

    def run(self):
        
        # heads = "-" * len(self.root) if len(self.root) > len(self.intro) else "-" * len(self.intro)
        if len(self.root) > len(self.intro):
            self.root = '- ' + self.root + ' -'
            heads = "-" * len(self.root)
            intro_space = int(abs((len(self.root) - len(self.intro)) / 2)) - 1
            intro = '-' + ' ' * intro_space
            intro += self.intro + ' ' * intro_space
            intro += '-'
            r = self.root
        else:
            self.intro = '- ' + self.intro + ' -'
            heads = '-' * len(self.intro)
            root_space = int(abs((len(self.intro) - len(self.root)) / 2)) - 1
            r = '-' + ' ' * root_space
            r += self.root + ' ' * root_space
            r += '-'
            intro = self.intro
        print(heads, intro, r, heads, sep='\n', end='\n')


class Fuck(Command):
    """ Just fucking with [you]  """
    def __init__(self, default_val='you'):
        self.default_val=default_val

    def get_options(self):
        return [
                Option('--name', '-n', dest='name', default=self.default_val),
        ]
    
    
    def run(self, name):
        if name != 'you':
            print(string.capwords("fuck you {}!".format(name)), end='\n\n')
            return

        print(string.capwords("fuck you!"), end='\n\n')
        return

class SecretKey(Command):
    """ Generate SECRET_KEY in Flask's config file. """
    def __init__(self):
        self.root_path = parentdir 
        self.config_file = os.path.join(self.root_path, 'common', 'config.py')
    
    def get_options(self):
        return [
                Option('--length', '-l',
                    dest='length',
                    default='32',
                    help="Specify the length of the random AlphaNum Key (32 char long, by default)."),
        ]
 
    def run(self, length):
        if prompt_bool("Overwrite app.secret_key?"):
            app_secret_key = "SECRET_KEY"
            hashed = rnd(int(length))
            nu_line = "{} = '{}'\n".format(app_secret_key, hashed)
            
            with open (self.config_file, 'r') as origin:
                old_data = origin.readlines()
            
            nu_content = ''.join(self.overwriteSecretKey(old_data)) + '\n\n' + nu_line
            
            with open(self.config_file, 'w') as modified:
                modified.write(nu_content)
            
            print("*" * 5,
                    "New secret key inserted into {}".format(self.config_file),
                    sep='\n',
                    end='\n\n')

            print('-' * 5,
                    "Key value = {}".format(hashed),
                    sep='\n')
            
            return True
        
        print('No secret key generate. Cancelled.')
        return False

    def overwriteSecretKey(self, input_list):
        for index, line in enumerate(input_list):
            matchObj = re.match(r'^SECRET_KEY\s\=\s(.*)$', line, re.M|re.I)
            if matchObj:
                input_list.pop(index)
        return input_list


class DbCreator(Command):
    """ Create Sqlite file for database.  """
    def __init__(self, db_name='db'):
        self.db_path = os.path.join(parentdir, 'store')
        self.all_dbs = [f for f in os.listdir(self.db_path) if os.path.isfile(os.path.join(self.db_path, f))]
        self.db_name = db_name

    def get_options(self):
            return [
                    Option('--name', '-n',
                        dest='dbname',
                        default=self.db_name,
                        help="Filename of the Sqlite's file (default: db.sqlite)."),
            ]
        


    def run(self, dbname):
        import api.models.auth
        dbn = dbname + '.sqlite'
        if dbn in self.all_dbs:
            print("{} already exists!".format(dbname))
            return False
        print("Creating {0} at {1}".format(dbn, self.db_path))
        print(database, app.config['SQLALCHEMY_DATABASE_URI'])
        # database.create_all()
        return True



manager.add_command('info', Info())
manager.add_command('fuck', Fuck())
manager.add_command('createdb', DbCreator())
manager.add_command('secretkey', SecretKey())

if __name__ == '__main__':
    manager.run()
