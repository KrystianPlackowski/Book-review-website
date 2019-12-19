import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv 

#engine = create_engine('postgresql://postgres:qwe@localhost/postgres')
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def read_csv(input_file):
    with open(input_file) as file:
        reader = csv.reader(file)
        next(reader)  # Skip header line
        i = 0
        for isbn, title, author, year in reader:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn":isbn, "title":title, "author":author, "year":year})
            print("Imported row number ", i)
            i += 1


# Check if table with given name already exists. If so - delete it
def check_del_table(table_name):
    if db.execute("SELECT to_regclass($${}$$)"
            .format(table_name)).fetchone()[0] != None:
        db.execute("DROP TABLE {}".format(table_name))
        print("Deleted already existing table \'{}\'".format(table_name))


"""
# Create a new table 'books'. Delete (if so) already existing one
check_del_table('books')
db.execute("CREATE TABLE books (id SERIAL PRIMARY KEY, isbn VARCHAR, title VARCHAR, author VARCHAR, year INTEGER)")
print("Created new table \'books\'")

# Import values from 'books.csv' to SQL table 'books'
read_csv("books.csv")
"""

# Create tables 'users' and 'reviews'
check_del_table('users')
check_del_table('reviews')

db.execute("CREATE TABLE users (id SERIAL PRIMARY KEY, login VARCHAR NOT NULL, password VARCHAR NOT NULL)")
print("Created new table \'users\'")

db.execute("CREATE TABLE reviews (id SERIAL PRIMARY KEY, book_id INTEGER REFERENCES books, login VARCHAR NOT NULL, rating FLOAT, text VARCHAR NOT NULL)")
print("Created new table \'reviews\'")

# Save changes
db.commit()
