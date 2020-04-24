import os 
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URL = "postgresql://postgres:password@localhost/book_review"

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind = engine))

def main():
    f = open("books.csv")
    books = csv.reader(f)

    for isbn, title, author, year in books:
        db.execute("INSERT INTO books_info(isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
            {"isbn":isbn, "title":title, "author":author, "year":year})
        print(f"ISBN Number: {isbn} Book Name: {title} Author: {author} Year: {year}")
    db.commit()

if __name__ == "__main__":
    main()
