# Project 1

This is solution for second problem from `CS50 course` conducted at Harvard University. The course is accessible through edX platform: https://www.edx.org/

# Description

A backend project of a simple website providing ability to register and log in (with special cases handling exceptions) for users, performing search for books, viewing details page for a selected book and writing reviews. Additionally, provides API responses when entering a specified route.

The details page uses `Goodreads Review Data API`, so a key obtained at https://www.goodreads.com/api needs to be set as an enviromental variable named `BOOK_API_KEY`. Secondly, one needs to set `DATABASE_URL` enviromental variable as URI of a SQL database of own choice.

After setting `DATABASE_URL` variable, file `import.py` should be run once, to initiate 3 SQL tables and fill one of them with values from `books.csv` file. If database is stored online, it can take few minutes to complete.

The preview is available in `screencast.mp4`. To run application type `flask run` in terminal window. `FLASK_APP` should be set to `application`.
