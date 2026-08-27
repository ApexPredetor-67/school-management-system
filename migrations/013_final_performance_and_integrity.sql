-- Final V11 performance indexes; safe on the existing PostgreSQL schema.
CREATE INDEX IF NOT EXISTS ix_student_active_class_section_roll ON public.student (active, class_name, section, roll_number, name);
CREATE INDEX IF NOT EXISTS ix_student_active_admission ON public.student (active, admission_number);
CREATE INDEX IF NOT EXISTS ix_parent_student_student_parent ON public.parent_student (student_id, parent_id);
CREATE INDEX IF NOT EXISTS ix_parent_student_parent_student ON public.parent_student (parent_id, student_id);
CREATE INDEX IF NOT EXISTS ix_teacher_account_active ON public.teacher (account_id, active);
CREATE INDEX IF NOT EXISTS ix_teacher_assignment_teacher_class_section ON public.teacher_assignment (teacher_id, class_name, section);
CREATE INDEX IF NOT EXISTS ix_teacher_subject_teacher_subject ON public.teacher_subject_assignment (teacher_id, subject_code);
CREATE INDEX IF NOT EXISTS ix_mark_student_exam_subject ON public.mark (student_id, exam_id, subject_code);
CREATE INDEX IF NOT EXISTS ix_fee_invoice_student_session_title ON public.fee_invoice (student_id, academic_session, title, created_at DESC);
CREATE INDEX IF NOT EXISTS ix_fee_payment_invoice_paid_at ON public.fee_payment (invoice_id, paid_at DESC);
CREATE INDEX IF NOT EXISTS ix_announcement_parent_title ON public.announcement (parent_id, title);
