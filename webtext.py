from __future__ import division
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

import nltk, re, pprint
from nltk.corpus import gutenberg
from nltk.corpus import wordnet as wn


# configuration
DATABASE = '/tmp/webtext.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create the app 
app = Flask(__name__)      #Flask application object
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())  

        db.execute('insert into entries (title, author, genre, corpusID, fileID, url) values (?, ?, ?, ?, ?, ?)',
            ['Emma', 'Jane Austen', 'classics', 'Gutenberg', 'austen-emma.txt', 'none'])
        db.execute('insert into entries (title, author, genre, corpusID, fileID, url) values (?, ?, ?, ?, ? ,?)',
            ['Moby Dick', 'Herman Melville', 'classics', 'Gutenberg', 'melville-moby_dick.txt', 'none'])
        db.execute('insert into entries (title, author, genre, corpusID, fileID, url) values (?, ?, ?, ?, ? ,?)',
            ['The Man Who Was Thursday', 'G. K. Chesterton', 'classics', 'Gutenberg', 'chesterton-thursday.txt', 'none'])           
        db.execute('insert into entries (title, author, genre, corpusID, fileID, url) values (?, ?, ?, ?, ?, ?)',
            ['Hamlet', 'William Shakespeare', 'classics', 'Gutenberg', 'shakespeare-hamlet.txt', 'none'])       
        db.commit()
        

#before, after and teardown are executed for each request - use object "g" which stores current request
@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
        
# App functions

#For each entry, find the full text if available and count the occurrences of "user word",
#then add a new field to the entry called "word count" (set to 0 if word count could not be found)
def addWordCount(entries, userWord):
	for entry in entries:
		if entry["corpusID"] == "Gutenberg":
			fileID = entry["fileID"]
			textWords = nltk.Text(nltk.corpus.gutenberg.words(fileID))
			resultString = "occurrences [\'" + userWord + "\'] = " + str(textWords.count(userWord))
			entry["wordcount"] = resultString
		else:
			entry["wordcount"] = 0
			
#Just a temporary way to access database - needs improving
def queryDB(titleStr, authorStr):	
	if not session.get('logged_in'):
		abort(401)
	cur = g.db.execute('select * from entries where title = ? or author = ?',[titleStr, authorStr])    #request.form['author']])
	entries = [dict(title=row[1], author=row[2], genre=row[3], corpusID=row[4], fileID=row[5], url=row[6]) 
					for row in cur.fetchall()] 
	return entries


#Views - each of these have a URL given by app.route

@app.route('/', methods=['GET', 'POST'])
def start_page():
	if session.get('logged_in'):
		return render_template('options.html')
	else:
		return render_template('login.html')


@app.route('/list_all')
def show_entries():
    cur = g.db.execute('select * from entries order by id desc')  #execute sql statement
    entries = [dict(title=row[1], author=row[2], genre=row[3], corpusID=row[4], fileID=row[5], url=row[6]) 
    				for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)


@app.route('/database_query', methods=['POST'])
def database_query():    
    entries = queryDB(request.form['title'], request.form['author'])
    flash('Query results')
    return render_template('show_entries.html', entries=entries)
    

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, author, genre, corpusID, fileID, url) values (?, ?, ?, ?, ?, ?)',
                 [request.form['title'], request.form['author'], request.form['genre'], 
                 request.form['corpusID'], request.form['fileID'], request.form['url']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


#Responds to selection of "analyse text" from the "options" page
@app.route('/analyse_text')
def analyse_text():
	return render_template('analyse.html')


#Responds to form input from "analyse.html"
@app.route('/count_words', methods=['POST'])
def count_words():
	entries = queryDB(request.form['title'], request.form['author'])	
	addWordCount(entries, request.form["word"])  
	 	
	#Show entries with word counts
	flash('Text analysis results ')
	return render_template('show_wordcount_entries.html', entries=entries, userWord=request.form["word"])
   
   
#Site search - not yet implemented		
@app.route('/search', methods=['GET', 'POST'])
def search_page():
	return render_template('search.html')

	
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            # flash('You are logged in')
            return render_template('options.html')
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You are logged out')
    return render_template('login.html')
    #return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
