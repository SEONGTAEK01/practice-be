create TABLE IF NOT EXISTS users (
id serial PRIMARY KEY,
email VARCHAR (255) UNIQUE NOT NULL,
hashed_password VARCHAR (50) NOT NULL,
is_active BOOL default TRUE
);

--INSERT INTO users VALUES (1, 'hongseongtaek@gmail.com', 'not-hashed-password');

create TABLE IF NOT EXISTS items (
id serial PRIMARY KEY,
title VARCHAR (50) NOT NULL,
description VARCHAR (255),
owner_id INTEGER REFERENCES users(id)
);

--INSERT INTO items VALUES (1, '수저', '방짜유기 수저', 1);
