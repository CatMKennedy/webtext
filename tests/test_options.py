# test options.py functions
from appfiles.options import queryDB 
from appfiles.db import get_db, init_db, close_db


def test_start_page(client, auth):
    pass
    # response = client.get('/')
    # assert b"Login" in response.data
    # assert b"Register" in response.data

    # auth.login()
    # response = client.get('/')
   #assert b'Logout' in response.data


def test_show_entries(client):
    pass
    #response = client.get('/list_all')

    # What does "response" need to contain?


def test_database_query(client):
    pass
    #response = client.get('/database_query')

    # Response to client.post?


def test_add_entry(client, auth):
    pass
    #response = client.get('/add_new')

    # test for login and logout
    # Should also test client.post - form submission


def test_analyse_text(client):
    pass
    #response = client.get('/analyse_text')

    # what should response contain?


def test_count_words(client):
    pass
    #response = client.post('/count_words')

    # what should response contain?


def test_search_page(client):
    pass
    #response = client.get('/search')

    # what should response contain?
    # should also test post.






      