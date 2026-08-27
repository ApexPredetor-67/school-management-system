from datetime import datetime, date, time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint, Index


db = SQLAlchemy()


def now_local():
    return datetime.utcnow()


class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, index=True)  # admin/teacher/student/parent
    display_name = db.Column(db.String(160), nullable=False)
    must_change_password = db.Column(db.Boolean, default=True, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=now_local, nullable=False)
    last_login = db.Column(db.DateTime)
    profile_picture_path = db.Column(db.String(255))


class Student(db.Model):
    __tablename__ = 'student'
    id = db.Column(db.Integer, primary_key=True)
    admission_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    roll_number = db.Column(db.String(30), index=True)
    name = db.Column(db.String(160), nullable=False, index=True)
    class_name = db.Column(db.String(10), nullable=False, index=True)
    section = db.Column(db.String(10), nullable=False, default='')
    second_language = db.Column(db.String(30))
    third_language = db.Column(db.String(30))
    date_of_birth = db.Column(db.Date)
    mother_name = db.Column(db.String(160))
    father_name = db.Column(db.String(160))
    address = db.Column(db.Text)
    phone = db.Column(db.String(40))
    email = db.Column(db.String(160))
    previous_school = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), unique=True)
    face_encoding_json = db.Column(db.Text)
    face_trained = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=now_local, nullable=False)
    account = db.relationship('Account', foreign_keys=[account_id])
    __table_args__ = (Index('ix_student_class_section_roll_name','class_name','section','roll_number','name'),)


class Parent(db.Model):
    __tablename__ = 'parent'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False)
    phone = db.Column(db.String(40))
    email = db.Column(db.String(160))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), unique=True)
    account = db.relationship('Account', foreign_keys=[account_id])


class ParentStudent(db.Model):
    __tablename__ = 'parent_student'
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id', ondelete='CASCADE'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
    __table_args__ = (UniqueConstraint('parent_id', 'student_id', name='uq_parent_student'), Index('ix_parent_student_parent','parent_id'), Index('ix_parent_student_student','student_id'))


class Teacher(db.Model):
    __tablename__ = 'teacher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(160), nullable=False, index=True)
    email = db.Column(db.String(160))
    phone = db.Column(db.String(40))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), unique=True)
    signature_data = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True, nullable=False, index=True)
    account = db.relationship('Account', foreign_keys=[account_id])


class TeacherAssignment(db.Model):
    __tablename__ = 'teacher_assignment'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), nullable=False)
    class_name = db.Column(db.String(10), nullable=False, index=True)
    section = db.Column(db.String(10), nullable=False, default='')
    __table_args__ = (UniqueConstraint('class_name', 'section', name='uq_class_section_teacher'), Index('ix_teacher_assignment_teacher','teacher_id'), Index('ix_teacher_assignment_class_section','class_name','section','teacher_id'))

class TeacherSubjectAssignment(db.Model):
    __tablename__ = 'teacher_subject_assignment'
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id', ondelete='CASCADE'), nullable=False, index=True)
    subject_code = db.Column(db.String(50), nullable=False, index=True)
    __table_args__ = (UniqueConstraint('teacher_id','subject_code', name='uq_teacher_subject_assignment'),)


class ReportCardConfig(db.Model):
    __tablename__ = 'report_card_config'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    academic_session = db.Column(db.String(30), nullable=False, default='2026-27')
    house = db.Column(db.String(80), default='')
    class_teacher_name = db.Column(db.String(160), default='')
    co_scholastic_json = db.Column(db.Text, default='{}')
    discipline_json = db.Column(db.Text, default='{}')
    health_json = db.Column(db.Text, default='{}')
    remarks = db.Column(db.Text, default='')
    principal_remarks = db.Column(db.Text, default='')
    date_result = db.Column(db.String(80), default='')
    next_academic_session = db.Column(db.String(30), default='')
    session_begins = db.Column(db.String(40), default='')
    summer_break_from = db.Column(db.String(40), default='')
    school_reopens = db.Column(db.String(40), default='')
    published = db.Column(db.Boolean, default=False, nullable=False)
    updated_by = db.Column(db.String(120), default='')
    updated_at = db.Column(db.DateTime, default=now_local, onupdate=now_local, nullable=False)
    layout_json = db.Column(db.Text, default='{}')


class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    class_band = db.Column(db.String(20), nullable=False, index=True)
    language_group = db.Column(db.String(20))
    active = db.Column(db.Boolean, default=True, nullable=False)


class Exam(db.Model):
    __tablename__ = 'exam'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    max_marks = db.Column(db.Integer, nullable=False)
    order_index = db.Column(db.Integer, nullable=False)
    is_final = db.Column(db.Boolean, default=False, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)


class Mark(db.Model):
    __tablename__ = 'mark'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
    subject_code = db.Column(db.String(50), nullable=False, index=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id', ondelete='CASCADE'), nullable=False)
    marks = db.Column(db.Float)
    max_marks = db.Column(db.Integer, nullable=False)
    updated_by = db.Column(db.String(120))
    updated_at = db.Column(db.DateTime, default=now_local, onupdate=now_local, nullable=False)
    locked = db.Column(db.Boolean, default=False, nullable=False)
    __table_args__ = (UniqueConstraint('student_id', 'subject_code', 'exam_id', name='uq_mark'), Index('ix_mark_student_exam','student_id','exam_id'))


class AssessmentComponent(db.Model):
    __tablename__ = 'assessment_component'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False)
    subject_code = db.Column(db.String(50), nullable=False, index=True)
    multiple_assessment = db.Column(db.Float, default=0)
    subject_enrichment = db.Column(db.Float, default=0)
    portfolio = db.Column(db.Float, default=0)
    internal_assessment = db.Column(db.Float)  # /20, school-configurable; can be reviewed before locking
    annual_exam = db.Column(db.Float)          # /80 = Final examination mirror
    remarks = db.Column(db.String(500))
    __table_args__ = (UniqueConstraint('student_id','subject_code', name='uq_assessment_component'),)


class Attendance(db.Model):
    __tablename__ = 'attendance'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default='present')
    time_in = db.Column(db.Time)
    source = db.Column(db.String(20), nullable=False, default='face')
    marked_by = db.Column(db.String(120))
    note = db.Column(db.String(500))
    student = db.relationship('Student')
    __table_args__ = (UniqueConstraint('student_id','date', name='uq_attendance'), Index('ix_attendance_date_status','date','status'), Index('ix_attendance_student_date','student_id','date'), Index('ix_attendance_student_date_status','student_id','date','status'), Index('ix_attendance_date_student','date','student_id'))


class SchoolCalendar(db.Model):
    __tablename__ = 'school_calendar'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False, index=True)
    is_working = db.Column(db.Boolean, default=True, nullable=False)
    reason = db.Column(db.String(255))


class Announcement(db.Model):
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    message = db.Column(db.Text, nullable=False)
    audience = db.Column(db.String(30), default='all', nullable=False)
    published = db.Column(db.Boolean, default=False, nullable=False)
    created_by = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=now_local, nullable=False)
    published_at = db.Column(db.DateTime)
    parent_id = db.Column(db.Integer, db.ForeignKey('parent.id', ondelete='CASCADE'))
    parent = db.relationship('Parent', foreign_keys=[parent_id])
    __table_args__ = (Index('ix_announcement_audience_published','audience','published'), Index('ix_announcement_created_at','created_at'), Index('ix_announcement_parent','parent_id','published'), Index('ix_announcement_audience_published_at','audience','published','published_at'), Index('ix_announcement_parent_created','parent_id','created_at'))


class ResultPublication(db.Model):
    __tablename__ = 'result_publication'
    id = db.Column(db.Integer, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id', ondelete='CASCADE'), nullable=False)
    class_name = db.Column(db.String(10), nullable=False)
    section = db.Column(db.String(10), nullable=False, default='')
    published = db.Column(db.Boolean, default=False, nullable=False)
    published_at = db.Column(db.DateTime)
    published_by = db.Column(db.String(120))
    __table_args__ = (UniqueConstraint('exam_id','class_name','section', name='uq_result_publication'),)


class AuditEvent(db.Model):
    __tablename__ = 'audit_event'
    id = db.Column(db.Integer, primary_key=True)
    occurred_at = db.Column(db.DateTime, default=now_local, nullable=False, index=True)
    actor_username = db.Column(db.String(120), nullable=False)
    actor_role = db.Column(db.String(30), nullable=False)
    action = db.Column(db.String(120), nullable=False)
    target_type = db.Column(db.String(80))
    target_id = db.Column(db.String(80))
    ip_address = db.Column(db.String(64))
    user_agent = db.Column(db.Text)
    metadata_json = db.Column(db.Text)
    previous_hash = db.Column(db.String(64))
    event_hash = db.Column(db.String(64), nullable=False, index=True)


class SchoolClock(db.Model):
    __tablename__ = 'school_clock'
    id = db.Column(db.Integer, primary_key=True)
    override_time = db.Column(db.String(10))
    updated_at = db.Column(db.DateTime, default=now_local, onupdate=now_local, nullable=False)


class SchoolSetting(db.Model):
    __tablename__ = 'school_setting'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=now_local, onupdate=now_local, nullable=False)


class PublishedReport(db.Model):
    __tablename__ = 'published_report'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False, index=True)
    session_name = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(20), default='draft', nullable=False)
    pdf_path = db.Column(db.String(255))
    published_at = db.Column(db.DateTime)
    published_by = db.Column(db.String(120))
    __table_args__ = (UniqueConstraint('student_id','session_name', name='uq_published_report'),)


class FeeStructure(db.Model):
    __tablename__ = 'fee_structure'
    id = db.Column(db.Integer, primary_key=True)
    academic_session = db.Column(db.String(30), nullable=False, index=True)
    class_group = db.Column(db.String(80), nullable=False)
    term_i = db.Column(db.Float, nullable=False, default=0)
    term_ii = db.Column(db.Float, nullable=False, default=0)
    term_iii = db.Column(db.Float, nullable=False, default=0)
    term_iv = db.Column(db.Float, nullable=False, default=0)
    total = db.Column(db.Float, nullable=False, default=0)
    updated_at = db.Column(db.DateTime, default=now_local, onupdate=now_local, nullable=False)
    updated_by = db.Column(db.String(120), default='')
    __table_args__ = (UniqueConstraint('academic_session','class_group', name='uq_fee_structure_session_group'), Index('ix_fee_structure_session_group','academic_session','class_group'))


class FeePaymentWindow(db.Model):
    __tablename__ = 'fee_payment_window'
    id = db.Column(db.Integer, primary_key=True)
    academic_session = db.Column(db.String(30), nullable=False, index=True)
    term_key = db.Column(db.String(30), nullable=False)
    term_label = db.Column(db.String(60), nullable=False)
    payment_start = db.Column(db.Date, nullable=False)
    payment_end = db.Column(db.Date, nullable=False)
    fine_from = db.Column(db.Date, nullable=False)
    updated_at = db.Column(db.DateTime, default=now_local, onupdate=now_local, nullable=False)
    updated_by = db.Column(db.String(120), default='')
    __table_args__ = (UniqueConstraint('academic_session','term_key', name='uq_fee_payment_window_session_term'), Index('ix_fee_window_session_start','academic_session','payment_start'))


class FeeStructureDocument(db.Model):
    __tablename__ = 'fee_structure_document'
    id = db.Column(db.Integer, primary_key=True)
    academic_session = db.Column(db.String(30), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    mimetype = db.Column(db.String(120), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=now_local, nullable=False)
    uploaded_by = db.Column(db.String(120), default='')


class FeeInvoice(db.Model):
    __tablename__ = 'fee_invoice'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id', ondelete='CASCADE'), nullable=False, index=True)
    academic_session = db.Column(db.String(30), index=True)
    title = db.Column(db.String(160), nullable=False)
    amount_due = db.Column(db.Float, nullable=False, default=0)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, default=now_local, nullable=False)
    student = db.relationship('Student')
    __table_args__ = (Index('ix_fee_invoice_student_session_status','student_id','academic_session','status'),)


class FeePayment(db.Model):
    __tablename__ = 'fee_payment'
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('fee_invoice.id', ondelete='CASCADE'), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(40), nullable=False, default='offline')
    receipt_no = db.Column(db.String(80), unique=True, nullable=False)
    paid_at = db.Column(db.DateTime, default=now_local, nullable=False)
    received_by = db.Column(db.String(120))
    invoice = db.relationship('FeeInvoice', backref='payments')
    __table_args__ = (Index('ix_fee_payment_invoice_paid_at','invoice_id','paid_at'),)
