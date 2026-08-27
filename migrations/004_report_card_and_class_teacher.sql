-- Final local-test migration: configurable report cards + class-teacher assignments
CREATE TABLE IF NOT EXISTS report_card_config (
  id INTEGER PRIMARY KEY, student_id INTEGER UNIQUE NOT NULL, academic_session VARCHAR(30) NOT NULL DEFAULT '2026-27',
  house VARCHAR(80) DEFAULT '', class_teacher_name VARCHAR(160) DEFAULT '', co_scholastic_json TEXT DEFAULT '{}', discipline_json TEXT DEFAULT '{}',
  health_json TEXT DEFAULT '{}', remarks TEXT DEFAULT '', principal_remarks TEXT DEFAULT '', date_result VARCHAR(80) DEFAULT '', next_academic_session VARCHAR(30) DEFAULT '',
  session_begins VARCHAR(40) DEFAULT '', summer_break_from VARCHAR(40) DEFAULT '', school_reopens VARCHAR(40) DEFAULT '', published BOOLEAN NOT NULL DEFAULT FALSE, updated_by VARCHAR(120) DEFAULT '', updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Fresh local DBs use the ORM model without a subject column in teacher_assignment.
