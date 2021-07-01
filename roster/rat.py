import json
import sqlite3

conn = sqlite3.connect('ratdb.sqlite')
curr = conn.cursor()

curr.executescript('''
DROP TABLE IF EXISTS USER;
DROP TABLE IF EXISTS COURSE;
DROP TABLE IF EXISTS MEMBER;

CREATE TABLE User(
    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
);

CREATE TABLE Course(
   id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
   title TEXT UNIQUE 
);

CREATE TABLE Member(
    user_id INTEGER,
    course_id INTEGER,
    role INTEGER,
    PRIMARY KEY(user_id,course_id)
)
'''
)

file = input('Enter file name: ')
if len(file) < 1:
    fp = 'roster_data.json'

str_data = open(fp).read()
json_data = json.loads(str_data)

for entry in json_data:
    name = entry[0]
    title = entry[1]
    role = entry[2]
    print((name,title,role))

    curr.execute('''INSERT OR IGNORE INTO User (name) VALUES (?)''',(name,))
    curr.execute('''SELECT id FROM User WHERE name = ?''',(name,))
    user_id = curr.fetchone()[0]

    curr.execute('''INSERT OR IGNORE INTO Course (title) VALUES (?)''',(title,))
    curr.execute('''SELECT id FROM Course WHERE title = ?''',(title,))
    course_id = curr.fetchone()[0]

    curr.execute('''INSERT OR REPLACE INTO Member(user_id,course_id,role) VALUES(?,?,?)''',(user_id,course_id,role))

    conn.commit()
