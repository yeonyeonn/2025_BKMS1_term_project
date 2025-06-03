import sqlite3

conn = sqlite3.connect("student_record.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

schema = """
CREATE TABLE student (
    student_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date TEXT,
    grade INTEGER,
    class INTEGER,
    number INTEGER,
    gender TEXT,
    enrollment_year INTEGER
);

CREATE TABLE club (
    club_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    teacher TEXT,
    description TEXT
);

CREATE TABLE activity (
    activity_id TEXT PRIMARY KEY,
    student_id TEXT,
    activity_type TEXT CHECK (activity_type IN ('자율', '동아리', '진로', '특기적성')),
    title TEXT,
    description TEXT,
    activity_date TEXT,
    end_date TEXT,
    club_id TEXT,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (club_id) REFERENCES club(club_id)
);

CREATE TABLE award (
    award_id TEXT PRIMARY KEY,
    student_id TEXT,
    award_name TEXT,
    awarding_body TEXT,
    award_level TEXT CHECK (award_level IN ('교내', '교외')),
    award_date TEXT,
    description TEXT,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

CREATE TABLE grade (
    grade_id TEXT PRIMARY KEY,
    student_id TEXT,
    semester TEXT CHECK (semester IN ('1학기', '2학기')),
    year INTEGER,
    subject TEXT,
    score TEXT,
    description TEXT,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);

CREATE TABLE subject_detail (
    detail_id TEXT PRIMARY KEY,
    student_id TEXT NOT NULL,
    grade_id TEXT,
    subject TEXT NOT NULL,
    semester TEXT CHECK (semester IN ('1학기', '2학기')) NOT NULL,
    year INTEGER NOT NULL,
    category TEXT CHECK (category IN ('독서', '수행평가', '발표', '활동')) NOT NULL,
    description TEXT,
    FOREIGN KEY (student_id) REFERENCES student(student_id),
    FOREIGN KEY (grade_id) REFERENCES grade(grade_id)
);

CREATE TABLE volunteer (
    volunteer_id TEXT PRIMARY KEY,
    student_id TEXT,
    organization TEXT,
    description TEXT,
    volunteer_date TEXT,
    hours REAL,
    FOREIGN KEY (student_id) REFERENCES student(student_id)
);
"""

cursor.executescript(schema)
conn.commit()
conn.close()

print("SQLite 데이터베이스가 student_record.db로 생성됨")
