import os

from flask import Flask, session, render_template, request, json
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from help_functions import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Check for environment variable
if not os.getenv("BOOK_API_KEY"):
    raise RuntimeError("BOOK_API_KEY is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Set up api_key for Goodreads
api_key = os.getenv("BOOK_API_KEY")


@app.route('/')
def index():
    return "Welcome page"

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/search/results', methods=["POST"])
def results():
    query = request.form.get("search query")

    # Perform query for each typed word (separated by spaces) and return 
    # an UNION of all query results (results must contain ALL words somewhere), sorted by ID

    for single_query in query.split(' '):
        if single_query == query.split(' ')[0]:
            query_results = perform_search(db, single_query)
        else:
            query_results &= perform_search(db, single_query)

    return render_template("results.html", results=sorted(list(query_results)))

@app.route('/search/results/<int:book_id>')
def book_info(book_id):
    book = db.execute("SELECT * FROM books WHERE ID = :book_id"
            , {"book_id":book_id}).fetchone()

    if book == None:
        return render_template("error.html", message="No such book.")
    
    res = requests.get("https://www.goodreads.com/book/review_counts.json"
            , params={"key": api_key, "isbns": book.isbn})
    
    return render_template("book_info.html", book=book
            , res=res.json()['books'][0])
