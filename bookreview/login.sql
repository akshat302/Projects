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



CREATE TABLE review(
    book_id INTEGER REFERENCES books_info(id),
    comments VARCHAR NOT NULL,
    user_id  uuid REFERENCES userID(id)
);

CREATE TABLE user(
    id uuid NOT NULL DEFAULT gen_random_uuid PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);




