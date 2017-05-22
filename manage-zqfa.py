#!/usr/bin/env python2

from flask.ext.script import Manager
from zqfa import create_app

manager = Manager(create_app)

if __name__ == '__main__':
    manager.run()
