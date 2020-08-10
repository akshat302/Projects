CREATE TABLE userID(
    id uuid NOT NULL DEFAULT gen_random_uuid PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL
);



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




