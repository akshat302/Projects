CREATE TABLE userID(
    id uuid NOT NULL DEFAULT gen_random_uuid PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);


INSERT INTO userID (name, email, password) VALUES ('bob', 'bob@test.com', digest('12345', 'sha256'));



crypt.crypt('password',password)}


email = akshat@test.com
password = akshat123

CREATE TABLE books_info(
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year INTEGER NOT NULL 
);


if request.method == "POST":
        category = request.form.get("category")
        if category == "ISBN":
            books_by_category = db.execute("SELECT isbn FROM books_info")
        if category == "Author":
            books_by_category = db.execute("SELECT author FROM books_info")
        if category == "Books":
            books_by_category = db.execute("SELECT books FROM books_info")
        return render_template("books.html", suggestions=books_by_category)
    