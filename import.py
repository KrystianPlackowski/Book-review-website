import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv 

#engine = create_engine('postgresql://postgres:qwe@localhost/postgres')
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def read_csv_1(input_file):
    with open(input_file) as file:
        reader = csv.reader(file)
        next(reader)  # Skip header line
        i = 0
        for isbn, title, author, year in reader:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn":isbn, "title":title, "author":author, "year":year})
            print("Imported row number ", i)
            i += 1


def read_csv_2(input_file):
    with open(input_file) as file:
        data = []
        reader = csv.reader(file)
        next(reader)  # Skip header line
        for isbn, title, author, year in reader:
            data.append({"isbn":isbn, "title":title, "author":author, "year":year})
    db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", data)
    print("Inserted all rows into table \'books\'")


# Check if table 'books' already exists. If so - delete it
if db.execute("SELECT to_regclass('books')").fetchone()[0] != None:
    db.execute("DROP TABLE books")
    print("Deleted already existing table \'books\'")
    
# Create table 'books'
db.execute("CREATE TABLE books (id SERIAL PRIMARY KEY, isbn VARCHAR, title VARCHAR, author VARCHAR, year INTEGER)")
print("Created new table \'books\'")

# Import values from 'books.csv' to SQL table 'books'
read_csv_1("books.csv")

# Save changes
db.commit()
