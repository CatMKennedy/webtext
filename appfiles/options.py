import nltk, re, pprint
from nltk.corpus import gutenberg
from nltk.corpus import wordnet as wn

from flask import (
    Blueprint, flash, session, g, redirect, render_template, request, url_for
)
from flask_login import current_user


from werkzeug.exceptions import abort

from appfiles.auth import login
from appfiles.db import get_db


bp = Blueprint('options', __name__)
#login_manager = loginManager()

# Utility functios - used by views

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
    if not session.get('user_id'):
        abort(401)
    db = get_db()
    cur = db.execute('select * from entries where title = ? or author = ?',[titleStr, authorStr])    #request.form['author']])
    entries = [dict(title=row[1], author=row[2], genre=row[3], corpusID=row[4], fileID=row[5], url=row[6]) for row in cur.fetchall()] 
    return entries

# Views

@bp.route('/', methods=['GET', 'POST'])
def start_page():
    if not session.get("user_id"):
        flash("not logged in")
        return render_template('layout.html')
    else:
        flash("logged in")
        return render_template('layout.html')
   
   

@bp.route('/list_all')
def show_entries():
    db = get_db()
    cur = g.db.execute('select * from entries order by id desc')  #execute sql statement
    entries = [dict(title=row[1], author=row[2], genre=row[3], corpusID=row[4], fileID=row[5], url=row[6]) 
    				for row in cur.fetchall()]
    return render_template('options/show_entries.html', entries=entries)


@bp.route('/database_query', methods=['GET', 'POST'])
def database_query(): 
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        entries = queryDB(title, author)
        return render_template('options/show_entries.html', entries=entries)
    
    return render_template('options/options.html')
   
   # if request.method == 'POST':
   #     entries = queryDB(request.form['title'], request.form['author'])
   #     flash('Query results')
    #    return render_template('options/show_entries.html', entries=entries)
    #else:
    #    flash("No query results")
   #     return redirect(url_for('options.show_entries'))
    

@bp.route('/add', methods=['POST'])
def add_entry():
    if not session.get('user_id'):
        abort(401)
    g.db.execute('insert into entries (title, author, genre, corpusID, fileID, url) values (?, ?, ?, ?, ?, ?)',
                 [request.form['title'], request.form['author'], request.form['genre'], 
                 request.form['corpusID'], request.form['fileID'], request.form['url']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


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
   
   
#Site search - not yet implemented		
@bp.route('/search', methods=['GET', 'POST'])
def search_page():
    return render_template('options/search.html')
  

