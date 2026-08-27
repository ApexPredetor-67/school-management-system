# DAV PS KKP — Final V11 Backend Refinement

This build preserves the existing V11 UI/templates and focuses on backend routing, data integrity, permissions, attendance, announcements, calendar, fees, and local AI functionality.

## Main fixes
- Added every backend endpoint referenced by the existing templates: student/teacher/parent edit/delete, assignment edit/delete, result publishing, and Test Time Clock.
- Kept `/attendance/scan` as the scanner path but did not add it to normal navigation.
- Scanner now rejects ambiguous face matches, selects the closest enrolled match through the existing best-match routine, respects school calendar and Test Time Clock, and never overwrites an existing Present/Late scan.
- Manual attendance rejects future dates and remains available to authorized staff.
- Announcement visibility is role-aware; parents can receive parent-targeted announcements; administrators can delete announcements.
- Added a portable calendar text/PDF/image import helper while preserving the existing calendar UI.
- Repaired the announcement `parent_id` schema compatibility issue.
- Added fee routes using the supplied 2026–27 fee table and payment windows; no automatic invoice generation is performed.
- Fee ledger supports admission/admin number, name, class, section, and roll filters. Payment verification remains manual.
- Fee reminders are idempotent and only generated for existing fee obligations after the configured fine date; they do not create invoices.
- Added a local, scope-limited AI endpoint that answers from the logged-in account's accessible student data without an external API quota.
- Added `academic_session` to the fee invoice model for compatibility with the database migration.
- Added idempotent application bootstrap for local SQLite and explicitly enabled production schema/seed settings.
- Fixed legacy teacher account backfill code that referenced a nonexistent `Teacher.username` model field.
- Kept account deletions as deactivation so attendance, academic, and audit history are preserved.

## Migration
Run `migrations/011_final_backend_compat.sql` after the existing V11 migrations. It is safe to run after migrations 001–010.

## Scanner UI rule
The existing `templates/attendance_scan.html` is intentionally untouched. The scanner remains reachable directly at `/attendance/scan`, but the normal navigation contains no Scan Attendance link.


## V5 fixes
- Fixed `/admin/accounts` 500 caused by the misspelled `sstudent_order(...)` call.
- Parent fee reminder announcements are now parent-targeted; generic `parents` announcements are only role-wide when `parent_id` is NULL.
- Added renewable CSRF tokens with `/api/csrf`, background refresh, previous-token grace, and automatic retry for stale AJAX tokens.
- Added JWT access/refresh token endpoints: `/api/auth/login` and `/api/auth/refresh`; access tokens carry `type=access`, refresh tokens carry `type=refresh`.
- Added CSRF token response headers and a template meta token for scanner/AJAX compatibility.
- Fixed Account & Security password eye control by allowing the global password-toggle helper there.
- Hardened `/api/school-day` so calendar lookup failures fall back to the normal weekday rule instead of disabling the scanner.
- Kept the scanner outside People & Accounts navigation and management.
