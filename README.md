# Book-review-website

This is a solution for the second problem from `CS50 course` conducted at Harvard University. The course is accessible through edX platform: https://www.edx.org/

## Description

A backend project of a simple website with ability to login/register (with special cases handling exceptions), searching for books and writing reviews. Additionally, provides API responses when entering a specified route. The preview showing all functionalities is available as `screencast.mp4` or via link https://www.youtube.com/watch?v=IYnApJ4M8sM

## Setting

The details page uses `Goodreads Review Data API`, so a key obtained at https://www.goodreads.com/api needs to be set as an enviromental variable named `BOOK_API_KEY`. Secondly, one needs to set `DATABASE_URL` enviromental variable as URI of an SQL database of own choice. Another variable `FLASK_APP` should be set to "`application`".

## Running

First run file `import.py` once. That will initiate 3 SQL tables and fill one of them with values from `books.csv` file. If database is stored online, import can take few minutes to complete. Then whenever want to run application type `flask run` in terminal window. 
