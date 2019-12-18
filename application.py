import os

from flask import Flask, session, render_template, request, json
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route('/')
def index():
    return "Welcome page"

@app.route('/search')
def search():
    return render_template("search.html")


def perform_search(query_type, query):
    if query_type == 'isbn':
        return db.execute("SELECT * FROM books WHERE isbn LIKE :query", {"query":'%'+query+'%'}).fetchall()
    
    if query_type == 'title':
        return db.execute("SELECT * FROM books WHERE title LIKE :query", {"query":'%'+query+'%'}).fetchall()

    if query_type == 'author':
        return db.execute("SELECT * FROM books WHERE author LIKE :query", {"query":'%'+query+'%'}).fetchall()

    if query_type == 'year':
        return db.execute("SELECT * FROM books WHERE year = :query", {"query":int(query)}).fetchall()


@app.route('/search/results', methods=["POST"])
def results():
    query = request.form.get("search query")
    query_type = request.form.get("query type")

    # Perform query for each typed word (separated by spaces) and return 
    # sum of query results (without repeatings), sorted by ID

    query_results = set()
    for single_query in query.split(' '):
        list_of_proxy = perform_search(query_type, single_query)

        # Can't hash using sqlAlchemy's 'tuplelike' type, so convert to tuples

        list_of_tuples = [tuple(list(i)) for i in list_of_proxy] 
        query_results |= set(list_of_tuples)

    #return json.dumps(query.split(' '))
    return render_template("results.html", results=sorted(list(query_results)))
