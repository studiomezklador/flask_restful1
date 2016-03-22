#!/usr/bin/env python3
import sys
import string
from flask.ext.script import Manager, Command, Option, prompt, prompt_bool
from api.__init__ import app, ai


manager = Manager(app)

manager.help_args = ('-?', '--help')

class Info(Command):
    """ Display Python Version used by this API. """
    def __init__(self):
        self.py_version = ".".join(map(str, sys.version_info[:3]))
        self.intro = '- FLASK CLI Manager: running with Python {} -'.format(self.py_version)
        self.heads = "-" * len(self.intro)

    def run(self):
        print(self.heads, self.intro, self.heads, sep='\n', end='\n')


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


class Selector(Command):
    """ Just to test prompts...  """
    def run(self):
        if prompt_bool("Do you want to continue?"):
            project_name = prompt("Name of your project?")
            if project_name:
                print("Writing directories & files for {}".format(project_name))
                return
            print("Cancelled...")
            return


manager.add_command('info', Info())
manager.add_command('fuck', Fuck())
manager.add_command('project', Selector())

if __name__ == '__main__':
    manager.run()
