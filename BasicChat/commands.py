import click
from flask.cli import with_appcontext

from BasicChat import db
from BasicChat.models import History

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()