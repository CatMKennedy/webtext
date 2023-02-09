# Webtext
This project explores the Python web framework Flask for simple text analysis. The user can:
- add or query texts in a literature database (currently just classics, mostly from the Gutenberg project) 
- do text analysis on the full-text (if available) of selected entries. Currently it only does word-counts.

The app has been built quickly using the Flask quickstart tutorial at: http://flask.readthedocs.org/en/0.3.1/. 

To run the app (Unix/Linux command line):

1. Initialise the database (from "webtext" directory):

In python interpreter:
from webtext import init_db
init_db()


2. Start the application:

$webtext> python3 webtext.py


3. Point browser to: http://127.0.0.1:5000/
