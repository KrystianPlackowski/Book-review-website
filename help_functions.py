# Convert sqlAlchemy's proxy object to tuple object, so it can be hashed

def convert_to_set(list_of_proxy):
    return set([tuple(list(i)) for i in list_of_proxy])

# Check if string is a valid int

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# For a single word perform searches in 4 different columns of SQL table
# and return a SUM of all possible matches (without repeatings).
# That means if user typed 'Black' then both books containing 'Black' in
# the title, aswell as containing it in author's name will be returned.

def perform_search(db, query):
    query_result = set()

    query_result |= convert_to_set(db.execute(
        "SELECT * FROM books WHERE isbn LIKE :query", {"query":'%'+query+'%'}).fetchall())
    
    query_result |= convert_to_set(db.execute(
        "SELECT * FROM books WHERE title LIKE :query", {"query":'%'+query+'%'}).fetchall())

    query_result |= convert_to_set(db.execute(
        "SELECT * FROM books WHERE author LIKE :query", {"query":'%'+query+'%'}).fetchall())

    if RepresentsInt(query):
        query_result |= convert_to_set(db.execute(
            "SELECT * FROM books WHERE year = :query", {"query":int(query)}).fetchall())

    return query_result
