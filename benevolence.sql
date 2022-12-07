CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    fname VARCHAR(25) NOT NULL,
    lname VARCHAR(30) NOT NULL,
    email VARCHAR(30) NOT NULL
);

CREATE TABLE recipients(
    recipient_id SERIAL PRIMARY KEY,
    r_name VARCHAR(50),
    ranking INTEGER ,
    user_id INTEGER NOT NULL REFERENCES users
);
CREATE TABLE events(
    event_id SERIAL PRIMARY KEY,
    event_name VARCHAR(50) NOT NULL,
    event_date  DATE NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users,
    recipient_id INTEGER REFERENCES recipients,
    note_id INTEGER REFERENCES notes
);

CREATE TABLE notes(
    note_id SERIAL PRIMARY KEY,
    content TEXT,
    recipient_id INTEGER REFERENCES NOT NULL recipients,
    event_id INTEGER NOT NULL REFERENCES events
);

CREATE TABLE likes(
    like_id SERIAL PRIMARY KEY,
    like_name VARCHAR(40) NOT NULL,
    recipient_id INTEGER NOT NULL REFERENCES recipients
    prompt_id INTEGER NOT NULL REFERENCES prompts
);

CREATE TABLE prompts(
    prompt_id SERIAL PRIMARY KEY,
    prompt_name VARCHAR(100) NOT NULL
)