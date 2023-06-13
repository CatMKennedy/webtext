import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# OLD
# def connect_db():
#   return sqlite3.connect(current_app.config['DATABASE'])

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:     
        db.cursor().executescript(f.read().decode('utf8')) 

        db.execute('insert into entries (title, author, genre, corpusID, fileID, url) values (?, ?, ?, ?, ?, ?)',
            ['Emma', 'Jane Austen', 'classics', 'Gutenberg', 'austen-emma.txt', 'none'])
        db.execute('insert into entries (title, author, genre, corpusID, fileID, url) values (?, ?, ?, ?, ? ,?)',
            ['Moby Dick', 'Herman Melville', 'classics', 'Gutenberg', 'melville-moby_dick.txt', 'none'])
        db.execute('insert into entries (title, author, genre, corpusID, fileID, url) values (?, ?, ?, ?, ? ,?)',
            ['The Man Who Was Thursday', 'G. K. Chesterton', 'classics', 'Gutenberg', 'chesterton-thursday.txt', 'none'])           
        db.execute('insert into entries (title, author, genre, corpusID, fileID, url) values (?, ?, ?, ?, ?, ?)',
            ['Hamlet', 'William Shakespeare', 'classics', 'Gutenberg', 'shakespeare-hamlet.txt', 'none'])       
        db.commit()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


