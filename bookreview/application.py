import os
from flask import Flask, render_template, request,session

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import crypt
from werkzeug.utils import redirect
from flask.helpers import url_for
from passlib.hash import sha256_crypt
import requests

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] ="filesystem"
app.secret_key = "abadabbajabba"

DATABASE_URL = "postgresql://postgres:password@localhost/book_review"

engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind = engine))

@app.route("/")
def index():
    return render_template("signin.html")

@app.route("/signup", methods=["GET", "POST"])
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

        return render_template("signin.html", success_msg = "User successfully registered. Please login now.")


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
            session["username"] = email_id
            return redirect(url_for('books'))

@app.route("/books", methods=["POST","GET"])
def books(): 
    if "username" in session:
        if request.method == "GET":
            return render_template("books.html", user=session["username"])
        if request.method == "POST":
            category = request.form.get("category", "").lower()
            search_query = request.form.get("search", "")

            if not category or not search_query:
                return render_template("books.html", data=None, category=category)

            query = "SELECT title, author, isbn FROM books_info WHERE {} LIKE '%{}%'".format(category, search_query)
            books_by_category = db.execute(query).fetchall()
            
            
            response = {
                "books": books_by_category,
                "status": 200
            }
            return render_template("books.html", data=response)
    
    return render_template("error.html")

@app.route("/books/<string:isbn>", methods=["GET", "POST"])
def about(isbn):
    if "username" in session:

        book_info = db.execute("SELECT * FROM books_info WHERE isbn=:isbn",{"isbn":isbn}).fetchall()
        user_id = db.execute("SELECT id FROM userID WHERE email=:email", {"email":session["username"]}).fetchone()
        
        
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "tmV6xHdc8pj0QLF2idR4hw", "isbns": str(isbn)})
        info = res.json()
        ratings = info['books'][0]['average_rating']    
        ratings_count = info['books'][0]['work_ratings_count']
        fetch_info = [ratings, ratings_count]

        if request.method == "GET":
            return render_template("about.html", data=book_info[0], fetch_info=fetch_info)

        if request.method == "POST":
            comment = request.form.get("comments")
            uid = user_id[0]
            book_id = book_info[0][0]
            query = db.execute("SELECT COUNT(comments) FROM review WHERE book_id=:book_id AND user_id=:user_id",
                                {"book_id":book_id, "user_id":uid}).fetchone()
            print(query)
            if query[0] >= 1:
                return render_template("error1.html")

            db.execute("INSERT INTO review(book_id, comments, user_id) VALUES (:book_id, :comments, :user_id)", {"book_id":book_id, "comments":comment, "user_id":uid})
            db.commit()
            return render_template("about.html", message = True, data=book_info[0], fetch_info=fetch_info)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for('signin'))
