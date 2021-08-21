# manage.py

import os
import unittest
import coverage

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/app.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()

from project.server.app import app, db
from project.server.dbmodel import studentModel, usermodel

from flask.cli import FlaskGroup
cli = FlaskGroup(app)


@cli.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'tmp/coverage')
        COV.html_report(directory=covdir)
        print('HTML version: file://%s/index.html' % covdir)
        COV.erase()
        return 0
    return 1


@cli.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@cli.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    cli()
