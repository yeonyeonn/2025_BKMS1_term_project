Create DATABASE student_record;
\c student_record;

-- Student
CREATE TABLE student (
    student_id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date DATE,
    grade INTEGER,
    class INTEGER,
    number INTEGER,
    gender TEXT,
    enrollment_year INTEGER
);

-- Club
CREATE TABLE club (
    club_id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    teacher TEXT,
    description TEXT
);

-- Activity
CREATE TYPE activity_type_enum AS ENUM ('자율', '동아리', '진로', '특기적성');

CREATE TABLE activity (
    activity_id UUID PRIMARY KEY,
    student_id UUID REFERENCES student(student_id),
    activity_type activity_type_enum,
    title TEXT,
    description TEXT,
    activity_date DATE,
    end_date DATE,
    club_id UUID REFERENCES club(club_id)
);

-- Award
CREATE TYPE award_level_enum AS ENUM ('교내', '교외');

CREATE TABLE award (
    award_id UUID PRIMARY KEY,
    student_id UUID REFERENCES student(student_id),
    award_name TEXT,
    awarding_body TEXT,
    award_level award_level_enum,
    award_date DATE,
    description TEXT
);

-- Grade
CREATE TYPE semester_enum AS ENUM ('1학기', '2학기');

CREATE TABLE grade (
    grade_id UUID PRIMARY KEY,
    student_id UUID REFERENCES student(student_id),
    semester semester_enum,
    year INTEGER,
    subject TEXT,
    score TEXT,
    description TEXT
);

CREATE TYPE category_enum AS ENUM ('독서', '수행평가', '발표', '활동');

-- subject_detail (각 과목 디테일)
CREATE TABLE subject_detail (
    detail_id UUID PRIMARY KEY,  -- 직접 UUID 입력
    student_id UUID NOT NULL REFERENCES student(student_id),
    grade_id UUID REFERENCES grade(grade_id), 
    subject TEXT NOT NULL,
    semester semester_enum NOT NULL,
    year INTEGER NOT NULL,
    category category_enum NOT NULL,
    description TEXT
);

-- Volunteer
CREATE TABLE volunteer (
    volunteer_id UUID PRIMARY KEY,
    student_id UUID REFERENCES student(student_id),
    organization TEXT,
    description TEXT,
    volunteer_date DATE,
    hours FLOAT
);
