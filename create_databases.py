import sqlite3

conn = sqlite3.connect('data.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Teachers;
DROP TABLE IF EXISTS Classes;
DROP TABLE IF EXISTS Subjects;
DROP TABLE IF EXISTS Students_Classes;
DROP TABLE IF EXISTS Marks;

CREATE TABLE Students (
    id  INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    fullname TEXT UNIQUE,
    class_id INTEGER,
    login TEXT UNIQUE,
    password TEXT
);

CREATE TABLE Teachers (
    id  INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    fullname TEXT UNIQUE,
    login TEXT UNIQUE,
    password TEXT,
    subject_id1 INTEGER,
    subject_id2 INTEGER,
    subject_id3 INTEGER,
    subject_id4 INTEGER
);

CREATE TABLE Classes (
    id  INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    title   TEXT UNIQUE
);

CREATE TABLE Subjects (
    id  INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    class_id1 INTEGER,
    class_id2 INTEGER,
    class_id3 INTEGER,
    class_id4 INTEGER
);

CREATE TABLE Marks (
    subject_id INTEGER,
    teacher_id INTEGER,
    student_id INTEGER,
    class_id INTEGER,
    dating TEXT,
    mark INTEGER 
);
''')
conn.commit()