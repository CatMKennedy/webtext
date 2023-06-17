import nltk
from nltk.corpus import gutenberg
from nltk.corpus import wordnet as wn
from nltk.text import Text
nltk.download("gutenberg")

from flask import (
    Blueprint, flash, session, g, redirect, render_template, request, url_for
)

from appfiles.auth import login
from appfiles.db import get_db


bp = Blueprint('options', __name__)


# Utility functions - used by views

# For each entry, find the full text if available and count the occurrences of "user word",
# then add a new field to the entry called "word count" (set to 0 if word count could not be found)
def addWordCount(entries, userWord):
    for entry in entries:
        if entry["corpusID"] == "Gutenberg":
            fileID = entry["fileID"]
            textWords = Text(nltk.corpus.gutenberg.words(fileID))
            resultString = f'occurrences of \"{userWord}\" = {str(textWords.count(userWord))}'
            entry["wordcount"] = resultString
        else:
            entry["wordcount"] = 0


# Return all entries that match title or author
def queryDB(titleStr, authorStr):	
    db = get_db()
    cur = db.execute('select * from entries where title = ? or author = ?',[titleStr, authorStr])    #request.form['author']])
    entries = [dict(title=row[1], author=row[2], genre=row[3], corpusID=row[4], fileID=row[5], url=row[6]) for row in cur.fetchall()] 
    return entries


# Views

@bp.route('/', methods=['GET', 'POST'])
def start_page():
    if not session.get("user_id"):
        #flash("not logged in")
        return render_template('layout.html')
    else:
        #flash("logged in")
        return render_template('layout.html')
     

@bp.route('/list_all')
def show_entries():
    db = get_db()
    cur = g.db.execute('select * from entries order by id desc')  #execute sql statement
    entries = [dict(title=row[1], author=row[2], genre=row[3], corpusID=row[4], fileID=row[5], url=row[6]) 
    				for row in cur.fetchall()]
    return render_template('options/show_entries.html', entries=entries)


# Respond to selection "Database query", and process subsequent form submission
@bp.route('/database_query', methods=['GET', 'POST'])
def database_query(): 
    if request.method == 'POST':     # on form submission
        title = request.form['title']
        author = request.form['author']
        entries = queryDB(title, author)
        return render_template('options/show_entries.html', entries=entries)
    
    return render_template('options/database_query_form.html') # get form
   
  
# If logged in, respond to selection "Add new", and process subsequent form submission
@bp.route('/add_new', methods=['GET', 'POST'])
def add_entry():
    if not session.get('user_id'):   
        flash("You need to be logged in to add an entry") 
        return render_template('layout.html')   
           
    if request.method == 'POST':     # on form submission
        db = get_db()
        g.db.execute('insert into entries (title, author, genre, corpusID, fileID, url) values (?, ?, ?, ?, ?, ?)',
                 [request.form['title'], request.form['author'], request.form['genre'], 
                 request.form['corpusID'], request.form['fileID'], request.form['url']])
        g.db.commit()
        flash('New entry was successfully inserted')
        return redirect(url_for('options.show_entries'))
    
    return render_template('options/add_new.html') # get form


#Responds to selection of "analyse text" from the "options" page
@bp.route('/analyse_text')
def analyse_text():
    return render_template('options/analyse.html')


#Responds to form input from "analyse.html"
@bp.route('/count_words', methods=['POST'])
def count_words():
    entries = queryDB(request.form['title'], request.form['author'])	
    addWordCount(entries, request.form["word"])  
	 	
    #Show entries with word counts
    flash('Text analysis results ')
    return render_template('options/show_wordcount_entries.html', entries=entries, userWord=request.form["word"])
   

