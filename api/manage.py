#!/usr/bin/env python3
# from importlib.machinery import SourceFileLoader
import sys
import string
import os
import re
# import moment
from flask.ext.script import (Manager,
                              Command,
                              Option,
                              prompt,
                              prompt_bool)
from flask.ext.migrate import Migrate, MigrateCommand
# from api.bootstrap import app, ai
from app import (db as database,
                 app,
                 ai)
from tools.krypt import rnd
# from models.auth import User, Role

migrate = Migrate(app, database)
manager = Manager(app)

manager.help_args = ('-?', '--help')


def _make_context():
    """
    Return context dict for shell session.
    Easy access to app, db & other things to insert (like Models)...
    """
    return dict(app=app, db=database)


class Info(Command):
    """ Display Python Version used by this API. """

    invite_msg = "FLASK CLI Manager: running with Python {}"

    def __init__(self):
        self.py_version = ".".join(map(str, sys.version_info[:3]))
        self.intro = self.invite_msg.format(self.py_version)
        self.root = app.root_path
        # self.heads = "-" * len(self.intro)

    def run(self):
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
        self.default_val = default_val

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
        self.root_path = app.root_path
        self.config_file = os.path.join(self.root_path, 'common', 'config.py')

    def get_options(self):
        return [
                Option('--length', '-l',
                       dest='length',
                       default='32',
                       help="Length of the alphanum key (default: 32)"),
        ]

    def run(self, length):
        if prompt_bool("Overwrite app.secret_key?"):
            app_secret_key = "SECRET_KEY"
            hashed = rnd(int(length))
            nu_line = "{} = '{}'\n".format(app_secret_key, hashed)

            with open(self.config_file, 'r') as origin:
                old_data = origin.readlines()

            nu_content = ''.join(self.overwriteSecretKey(old_data))
            nu_content += '\n\n' + nu_line

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
            matchObj = re.match(r'^SECRET_KEY\s\=\s(.*)$', line, re.M | re.I)
            if matchObj:
                input_list.pop(index)
        return input_list


class DbCreator(Command):
    """ Create Sqlite file for database.  """
    def __init__(self, db_name='db'):
        self.db_path = os.path.join(app.root_path, 'store')
        self.all_dbs = [f for f in os.listdir(self.db_path) if os.path.isfile(
            os.path.join(self.db_path, f))]
        self.db_name = db_name
        self.config_file = os.path.join(app.root_path, 'common', 'config.py')

    def get_options(self):
            return [
                    Option('--name', '-n',
                           dest='dbname',
                           default=self.db_name,
                           help="Sqlite's file name (default: db.sqlite)."),
            ]

    def run(self, dbname):
        dbn = dbname + '.sqlite'
        if dbn in self.all_dbs:
            print("{} already exists!".format(dbname))
            return False
        print("-" * 5, "Creating {0} at {1}".format(dbn, self.db_path),
              sep='\n')
        self.overwriteDbFileValue(dbn)
        print("-" * 5, "Overwriting db_file in common/config.py...",
              sep='\n')
        database.create_all()
        print("-" * 5, "Sqlite's file {} is now created!".format(dbn),
              "*" * 5,
              sep='\n')
        return True

    def overwriteDbFileValue(self, dbfilename):
        with(open(self.config_file, 'r')) as cfile:
            cfile_data = cfile.readlines()

        for i, li in enumerate(cfile_data):
            gMatch = re.match(r'^db_file\s=\s(.*)', li, re.I | re.U)
            if gMatch:
                nu_li = gMatch.group().split('=')
                cfile_data[i] = "{0} = '{1}'\n".format(nu_li[0].rstrip(),
                                                       dbfilename)

        nu_content = "".join(cfile_data)

        with(open(self.config_file, 'w')) as mfile:
            mfile.write(nu_content)

        return True


manager.add_command('info', Info())
manager.add_command('fuck', Fuck())
manager.add_command('createdb', DbCreator())
manager.add_command('secretkey', SecretKey())
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
