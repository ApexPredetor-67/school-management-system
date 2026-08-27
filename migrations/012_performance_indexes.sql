-- Performance indexes for common V11 school-management queries.
CREATE INDEX IF NOT EXISTS ix_student_class_section_roll_name
  ON public.student (class_name, section, roll_number, name);
CREATE INDEX IF NOT EXISTS ix_attendance_student_date_status
  ON public.attendance (student_id, date, status);
CREATE INDEX IF NOT EXISTS ix_attendance_date_student
  ON public.attendance (date, student_id);
CREATE INDEX IF NOT EXISTS ix_teacher_assignment_class_section
  ON public.teacher_assignment (class_name, section, teacher_id);
CREATE INDEX IF NOT EXISTS ix_teacher_subject_assignment_teacher_subject
  ON public.teacher_subject_assignment (teacher_id, subject_code);
CREATE INDEX IF NOT EXISTS ix_mark_student_subject_exam
  ON public.mark (student_id, subject_code, exam_id);
CREATE INDEX IF NOT EXISTS ix_announcement_audience_published_at
  ON public.announcement (audience, published, published_at DESC);
CREATE INDEX IF NOT EXISTS ix_announcement_parent_created
  ON public.announcement (parent_id, created_at DESC);
CREATE INDEX IF NOT EXISTS ix_fee_invoice_student_session_status
  ON public.fee_invoice (student_id, academic_session, status);
CREATE INDEX IF NOT EXISTS ix_fee_payment_invoice_paid_at
  ON public.fee_payment (invoice_id, paid_at DESC);
CREATE INDEX IF NOT EXISTS ix_fee_structure_session_group
  ON public.fee_structure (academic_session, class_group);
CREATE INDEX IF NOT EXISTS ix_fee_window_session_start
  ON public.fee_payment_window (academic_session, payment_start);
