import os
from flask import Flask, render_template, request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import crypt
from werkzeug.utils import redirect
from flask.helpers import url_for
from passlib.hash import sha256_crypt


app = Flask(__name__)

DATABASE_URL = "postgresql://postgres:password@localhost/book_review"

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind = engine))

@app.route("/")
def index():
    return render_template("signin.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")

    if request.method == "POST":
        name = request.form.get("name")
        email_id = request.form.get("email","").lower()
        password = request.form.get("password")
        hash_password = sha256_crypt.encrypt(password)
        password_length = len(password)

        if not name or not email_id or not password:
            return render_template("signup.html", name=name, email=email_id, password=password)


        email_exists = db.execute("SELECT FROM userID WHERE email=:email", {"email":email_id}).fetchone()

        if email_exists != None:
            return render_template("signup.html", errormessage=True)

        db.execute("INSERT INTO userID (name, email, password) VALUES (:name, :email, :password)", {"name":name, "email":email_id, "password":hash_password})
        db.commit()
        
        return render_template("signup.html", message=True)


@app.route("/login", methods=["GET","POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    
    if request.method == "POST":
        email_id = request.form.get("email", "").lower()
        password = request.form.get("password")
        
        actual_password = db.execute("SELECT password FROM userID WHERE email=:email", {"email":email_id}).fetchone()
        
        if actual_password is None:
            return render_template("signin.html",message=True)

        verified_user = sha256_crypt.verify(password, actual_password[0])

        if verified_user is False:
            return render_template("signin.html", message=True)
        else:
            return redirect(url_for('books'))

@app.route("/books", methods=["POST","GET"])
def books():
    if request.method == "GET":
        return render_template("books.html")
    if request.method == "POST":
        category = request.form.get("category", "").lower()
        search_query = request.form.get("search", "")

        if not category or not search_query:
            return render_template("books.html", data=None, category=category)

        query = "SELECT title FROM books_info WHERE {} LIKE '%{}%'".format(category, search_query)
        books_by_category = db.execute(query).fetchall()
        books_by_category = [book[0] for book in books_by_category]
        response = {
            "books": books_by_category,
            "status": 200
        }
        return render_template("books.html", data=response)


