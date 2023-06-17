# Webtext

This project explores the Python web framework Flask for simple text analysis. The user can:

- add or query texts in a literature database (currently just classics, mostly from the Gutenberg project)
- do text analysis on the full-text (if available) of selected entries. Currently it only does word-counts.

Directory contents:
appfiles/ - includes application code + static and templates subfolders.
tests/

To run the app (Unix/Linux command line):

flask --app appfiles run --debug

Point browser to: http://127.0.0.1:5000/
