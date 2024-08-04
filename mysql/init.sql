GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '1234' WITH GRANT OPTION;
FLUSH PRIVILEGES;



-- jmedu 데이터베이스 생성
CREATE DATABASE IF NOT EXISTS jmedu;

SHOW WARNINGS;

USE jmedu;

-- 학교 테이블
CREATE TABLE school (
    school_pk INT AUTO_INCREMENT,
    name VARCHAR(30),
    is_elementary BOOL,
    is_middle BOOL,
    is_high BOOL,
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    deleted_at DATETIME DEFAULT NULL,
    PRIMARY KEY(school_pk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;

-- 학생 테이블
CREATE TABLE student (
    student_pk CHAR(36) NOT NULL,
    name VARCHAR(20) NULL, /*이름*/
    sex_ism BOOL DEFAULT true, /*성별*/
    grade INT DEFAULT 0, /*예비 1학년은 0으로 설정, 1, 2, 3학년*/
    birthday DATE DEFAULT '2000-01-01', /*생일*/
    contact VARCHAR(20) DEFAULT '01000000000', /*연락처*/
    contact_parent VARCHAR(20) DEFAULT '01000000000', /*부모연락처*/
    school INT DEFAULT 1, /*소속학교*/
    payday INT DEFAULT 0, /*결제일*/
    firstreg DATE DEFAULT '2000-01-01', /*최초등록일*/
    is_enable BOOL DEFAULT true, /*활성화 여부*/
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    deleted_at DATETIME DEFAULT NULL,
    PRIMARY KEY(student_pk),
    FOREIGN KEY (school) REFERENCES school(school_pk) /*외부키 설정*/
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;



-- 교사 테이블
CREATE TABLE teacher (
    teacher_pk CHAR(36),
    name VARCHAR(20),
    sex_ism BOOL,
    birthday DATE,
    contact VARCHAR(20),
    id VARCHAR(20),
    pwd VARCHAR(255),
    admin_level INT, /* 0 : 가입 대기, 1 : 일반 강사, 2 : 관리 강사, 3 : 원장 */
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    deleted_at DATETIME DEFAULT NULL,
    PRIMARY KEY(teacher_pk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;



-- 등하원 로그 테이블(구형)
CREATE TABLE attend_log (
    attend_log_pk INT AUTO_INCREMENT,
    student CHAR(36),
    time DATETIME,
    is_attend BOOL, /*true는 등원, false는 하원*/
    is_late BOOL DEFAULT NULL,
    PRIMARY KEY(attend_log_pk),
    FOREIGN KEY (student) REFERENCES student(student_pk) /*외부키 설정*/
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;

-- 등하원 로그 테이블(신형)
CREATE TABLE attendance_log (
    attendance_log_pk INT AUTO_INCREMENT,
    student CHAR(36),/*student 테이블의 student_pk*/
    is_attend BOOL, /*true는 등원, false는 하원이 아닌 출석 여부를 나타냄*/
    attend_time DATETIME, /*출석 시간*/
    leave_time DATETIME DEFAULT NULL, /*하원 시간, 하원하지 않았다면 NULL*/
    PRIMARY KEY(attendance_log_pk),
    FOREIGN KEY (student) REFERENCES student(student_pk), /*외부키 설정*/
    sms_sent BOOL DEFAULT FALSE,
     sms_sent_time DATETIME DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;

-- 교사 출퇴근 로그 테이블
CREATE TABLE teacher_attend_log (
    teacher_attend_log_pk INT AUTO_INCREMENT,
    teacher CHAR(36),
    time DATETIME,
    is_attend BOOL,
    PRIMARY KEY(teacher_attend_log_pk),
    FOREIGN KEY (teacher) REFERENCES teacher(teacher_pk) /*외부키 설정*/
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;

-- 과목 테이블
CREATE TABLE subject (
    subject_pk INT AUTO_INCREMENT,/*과목코드*/
    name VARCHAR(20),/*과목이름*/
    teacher CHAR(36),/*담당강사(외부키)*/
    school INT,/*대상학교(외부키)*/
    grade INT,/*대상학년*/
    is_personal BOOL,/*1대1 과외식 수업 여부*/
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    deleted_at DATETIME DEFAULT NULL,
    PRIMARY KEY(subject_pk),/*주키설정*/
    FOREIGN KEY (teacher) REFERENCES teacher(teacher_pk),/*외부키 설정*/
    FOREIGN KEY (school) REFERENCES school(school_pk)/*외부키 설정*/
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;

-- 시간표 테이블
CREATE TABLE plan (
    plan_pk INT AUTO_INCREMENT,
    subject INT,
    week VARCHAR(3),/*요일(형식 : MON, TUE 등)*/
    starttime TIME,/*시작시간(형식 : 19시 30분의 경우 1930)*/
    endtime TIME,/*종료시간(형식 : 시작시간과 동일)*/
    room VARCHAR(20),/*강의실*/
    is_ended BOOL DEFAULT NULL,
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    deleted_at DATETIME DEFAULT NULL,
    PRIMARY KEY(plan_pk),
    FOREIGN KEY (subject) REFERENCES subject(subject_pk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;


-- 과목 수강날 기록 테이블
CREATE TABLE subject_executed (
    subject_executed_pk INT AUTO_INCREMENT,
    plan INT,
    teacher CHAR(36),
    started DATETIME,
    ended DATETIME DEFAULT NULL,
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    deleted_at DATETIME DEFAULT NULL,
    PRIMARY KEY(subject_executed_pk),
    FOREIGN KEY (plan) REFERENCES plan(plan_pk),
    FOREIGN KEY (teacher) REFERENCES teacher(teacher_pk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;

-- 과목별 수강 출석자 기록 테이블
CREATE TABLE subject_executed_attenders (
    subject_executed_attenders_pk INT AUTO_INCREMENT,
    subject_executed INT,
    student CHAR(36),
    is_attended BOOL,
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    deleted_at DATETIME DEFAULT NULL,
    PRIMARY KEY(subject_executed_attenders_pk),
    FOREIGN KEY (subject_executed) REFERENCES subject_executed(subject_executed_pk),
    FOREIGN KEY (student) REFERENCES student(student_pk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;

-- 시간 수강 테이블



-- 학생-과목 연결 테이블
CREATE TABLE student_subject (
    student_subject_pk INT AUTO_INCREMENT,
    student_id CHAR(36),
    subject_id INT,
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    deleted_at DATETIME DEFAULT NULL,
    PRIMARY KEY(student_subject_pk),
    FOREIGN KEY (student_id) REFERENCES student(student_pk),
    FOREIGN KEY (subject_id) REFERENCES subject(subject_pk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;

-- 관리자 로그 테이블
CREATE TABLE admin_log (
    admin_log_pk INT AUTO_INCREMENT,
    teacher CHAR(36),
    time DATETIME,
    log VARCHAR(255),
    PRIMARY KEY(admin_log_pk),
    FOREIGN KEY (teacher) REFERENCES teacher(teacher_pk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;


-- 권한 테이블
CREATE TABLE permissions (
    task_name VARCHAR(255),
    level INT,
    created_at DATETIME DEFAULT NOW(),
    updated_at DATETIME DEFAULT NOW(),
    deleted_at DATETIME DEFAULT NULL,
    PRIMARY KEY(task_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;




-- 권한 기본 세팅값
INSERT INTO permissions (task_name, level, created_at) VALUES 
('students_view', 1, NOW()),
('students_add', 1, NOW()),
('students_edit', 1, NOW()),
('students_search', 1, NOW()),
('students_view_detail', 1, NOW()),
('students_addPage', 1, NOW()),
('students_add_multiple', 1, NOW()),
('students_view_update', 1, NOW()),
('students_view_update_all', 1, NOW()),
('student_remove', 1, NOW()),
('plan', 1, NOW()),
('plan_add', 1, NOW()),
('plan_update', 1, NOW()),
('plan_remove', 1, NOW()),
('schools_view', 1, NOW()),
('school_add', 1, NOW()),
('school_update', 1, NOW()),
('school_remove', 1, NOW()),
("schools_view_detail", 1, NOW()),
("schools_search", 1, NOW()),
('subject_add', 1, NOW()),
('subject_remove', 1, NOW()),
('subject_update', 1, NOW()),
('subject_student_add', 1, NOW()),
('teacher_view', 1, NOW()),
('teacher_update', 1, NOW()),
('admin_permissions', 3, NOW()),
('conditional_note', 1, NOW());




-- 설정 테이블
CREATE TABLE serverconf (
    config_pk INT,
    logout_time INT,/*자동 로그아웃 시간 설정(분단위)*/
    payday_prenote_toggle BOOL,
    payday_prenote INT,
    payday_notemsg VARCHAR(255),
    PRIMARY KEY(config_pk)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;



DELIMITER $$

CREATE TRIGGER before_insert_student_school
BEFORE INSERT ON student
FOR EACH ROW
BEGIN
    DECLARE school_id INT;

    -- school 테이블에서 name이 NEW.school인 school_pk를 찾습니다.
    SELECT school_pk INTO school_id FROM school WHERE name = NEW.school;

    -- school_id가 NULL이 아닐 경우에만 NEW.school에 school_id를 할당합니다.
    IF school_id IS NOT NULL THEN
        SET NEW.school = school_id;
    ELSE
        SET NEW.school = NULL;
    END IF;
END $$

-- 학교 지정이 없으면 1 삽입
CREATE TRIGGER trg_before_insert_student
BEFORE INSERT ON student
FOR EACH ROW
BEGIN
    IF NEW.school IS NULL THEN
        SET NEW.school = 1;
    END IF;
END $$

-- 학교 테이블 업데이트 트리거
CREATE TRIGGER before_school_update
BEFORE UPDATE ON school
FOR EACH ROW
BEGIN
    SET NEW.updated_at = NOW();
END $$

-- 학생 테이블 업데이트 트리거
CREATE TRIGGER before_student_update
BEFORE UPDATE ON student
FOR EACH ROW
BEGIN
    SET NEW.updated_at = NOW();
END $$

-- 교사 테이블 업데이트 트리거
CREATE TRIGGER before_teacher_update
BEFORE UPDATE ON teacher
FOR EACH ROW
BEGIN
    SET NEW.updated_at = NOW();
END $$

-- 과목 테이블 업데이트 트리거
CREATE TRIGGER before_subject_update
BEFORE UPDATE ON subject
FOR EACH ROW
BEGIN
    SET NEW.updated_at = NOW();
END $$

-- 시간표 테이블 업데이트 트리거
CREATE TRIGGER before_plan_update
BEFORE UPDATE ON plan
FOR EACH ROW
BEGIN
    SET NEW.updated_at = NOW();
END $$

-- 과목 수강날 기록 테이블 업데이트 트리거
CREATE TRIGGER before_subject_executed_update
BEFORE UPDATE ON subject_executed
FOR EACH ROW
BEGIN
    SET NEW.updated_at = NOW();
END $$

-- 과목별 수강 출석자 기록 테이블 업데이트 트리거
CREATE TRIGGER before_subject_executed_attenders_update
BEFORE UPDATE ON subject_executed_attenders
FOR EACH ROW
BEGIN
    SET NEW.updated_at = NOW();
END $$

-- 학생-과목 연결 테이블 업데이트 트리거
CREATE TRIGGER before_student_subject_update
BEFORE UPDATE ON student_subject
FOR EACH ROW
BEGIN
    SET NEW.updated_at = NOW();
END $$

-- 등/하원 기록 및 결과 반환 프로시저
CREATE PROCEDURE RecordAttendance (
    IN studentPK CHAR(36)
)
BEGIN
    DECLARE vContactParent VARCHAR(20);
    DECLARE vName VARCHAR(20);
    DECLARE vStatus VARCHAR(10);
    DECLARE vCurrentTime DATETIME;
    DECLARE vAttendID INT;
    DECLARE vAttendTime DATETIME;
    DECLARE vLeaveTime DATETIME;

    -- 현재 시간 설정
    SET vCurrentTime = NOW();

    -- 학생의 contact_parent와 name 조회
    SELECT contact_parent, name INTO vContactParent, vName
    FROM student
    WHERE student_pk = studentPK;

    -- 금일 해당 학생의 출석 기록 조회
    SELECT attendance_log_pk, attend_time, leave_time INTO vAttendID, vAttendTime, vLeaveTime
    FROM attendance_log
    WHERE student = studentPK AND DATE(attend_time) = CURDATE();

    -- 출석 기록이 없는 경우
    IF vAttendID IS NULL THEN
        INSERT INTO attendance_log(student, is_attend, attend_time)
        VALUES (studentPK, TRUE, vCurrentTime);
        SET vStatus = 'attend';
    -- 출석 기록이 있고, 하원 기록이 없으나 출석 시간과 현재 시간의 차이가 5분 미만인 경우
    ELSEIF TIMESTAMPDIFF(MINUTE, vAttendTime, vCurrentTime) < 5 THEN
        SET vStatus = 'wait';
    -- 출석 기록이 있지만, 하원 기록이 이미 있는 경우
    ELSEIF vLeaveTime IS NOT NULL THEN
        SET vStatus = 'leave';
    -- 출석 기록이 있고, 하원 기록이 없으며 출석 시간과 현재 시간 차이가 5분 이상인 경우
    ELSE
        UPDATE attendance_log
        SET leave_time = vCurrentTime, sms_sent = TRUE, sms_sent_time = vCurrentTime
        WHERE attendance_log_pk = vAttendID;
        SET vStatus = 'already';
    END IF;
    -- 결과 반환
    SELECT vContactParent AS contact_parent, vName AS name, vStatus AS status;
END $$

DELIMITER ;




-- 설정 기본값 삽입(설정 데이터가 없는 경우)
INSERT INTO serverconf (config_pk, logout_time, payday_prenote_toggle, payday_prenote, payday_notemsg) SELECT 0, 60, false, 3, "{student} 학생 학부모님 안녕하세요? 학생의 등록비 납부일이 {remain}일 남았습니다. " FROM DUAL WHERE NOT EXISTS (SELECT * FROM serverconf);

-- 테스트용 쿼리



INSERT INTO school (name, is_elementary, is_middle, is_high) VALUES ('학교 미설정', true, false, false);
