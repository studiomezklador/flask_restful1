#!/usr/bin/env python3
import sys
import string
import os
import re
import moment
import bcrypt
from base64 import b64encode, b64decode

from flask.ext.script import Manager, Command, Option, prompt, prompt_bool
from api.__init__ import app, ai


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
    """ Generate a secret hard Key, based on bcrypt + base64 """
    def __init__(self):
        self.enc_value = moment.utcnow().timezone('Europe/Paris').format('YYYY-M-D H:m').encode('utf-8')
        self.hashed = b64encode(bcrypt.hashpw(self.enc_value, bcrypt.gensalt(10)))
        self.root_path = app.root_path 
        self.config_file = os.path.join(self.root_path, '__init__.py')


    def run(self):
        enc_key = self.hashed
        if prompt_bool("Overwrite app.secret_key?"):
            app_secret_key = "app.config['SECRET_KEY']"
            nu_line = "{} = '{}'\n".format(app_secret_key, enc_key.decode())
            with open (self.config_file, 'r') as origin:
                old_data = origin.read()
            nu_content = old_data + '\n\n' + nu_line
            with open(self.config_file, 'w') as modified:
                modified.write(nu_content)
            print("New secret key inserted into app.config!", end='\n\n')
        print("Secret key (encrypted): {}\nSecret key (decoded): {}".format(enc_key,b64decode(enc_key)))

manager.add_command('info', Info())
manager.add_command('fuck', Fuck())
manager.add_command('secret', SecretKey())

if __name__ == '__main__':
    manager.run()
