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


@app.route('/', methods=["GET", "POST"])
def index():
    # Initiate global variable `login`
    if session.get("login") is None:
        session["login"] = None

    # If user already logged in
    if session["login"] != None:
        return render_template("index.html", login=session["login"])

    # If user not logged in and got to the page by typing url
    if request.method == "GET":
        return render_template("login.html", message=
                "In order to perform a search please log in.")

    # Otherwise check if provided credentials are correct
    # (method is "POST" and user not logged in)
    login = request.form.get("login")
    password = request.form.get("password")

    cred = db.execute("SELECT * FROM users WHERE login = :login "
            + "AND password = :password"
            , {"login":login, "password":password}).fetchone()
     
    # Credentials not found
    if cred == None:
        return render_template("login.html"
                , message="Wrong credentials. Please try again.")

    # Successful login!
    session["login"] = login
    return render_template("index.html", login=session["login"])


@app.route('/logout', methods=["POST"])
def logout():
    session["login"] = None
    return render_template("login.html", message="Successfully logged out.")


@app.route('/register', methods=["GET", "POST"])
def register():
    # If got to this page without providing credentials in form
    if request.method == "GET":
        return render_template("register.html"
                , message="Enter desired username and password.")
    
    # If after providing credentials in `register.html` form
    login = request.form.get("login")
    password = request.form.get("password")

    # If inccorect username or password
    if len(login) < 4 or len(password) < 4:
        return render_template("register.html",
                message="Invalid username or password! At least 4 characters needed for each.")
                    
    # If username already taken
    cred = db.execute("SELECT * FROM users WHERE login = :login"
            , {"login":login}).fetchone()
    if cred != None:
        return render_template("register.html"
                , message="Username already taken!")

    # If everything was OK
    db.execute("INSERT INTO users (login, password) "
    + "VALUES (:login, :password)", {"login":login, "password":password})
    db.commit()

    return render_template("login.html", message="Successfully registered. Please log in.")


@app.route('/search', methods=["POST"])
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
            , res=res.json()['books'][0], code=res.status_code)
