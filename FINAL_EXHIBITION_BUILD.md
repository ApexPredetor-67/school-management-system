# DAV PS KKP — Final Exhibition Build

This build is intentionally minimal for an exhibition demo.

## Included
- Admin dashboard
- Teacher dashboard
- Student registration and accounts
- Parent/student linking
- Student search and class/section segregation
- Attendance register with manual admin override
- Original-style 7-frame face scanner backend
- Today's scanner marklist and counts
- School calendar with weekly fallback
- Test school clock
- Class-teacher-only academics and marks entry
- Admin read-only marks
- Language distinction: 2nd vs 3rd language
- Configurable report card generation
- Teacher signature upload/drawing
- Announcements with role/public separation
- CSRF and JWT security

## Removed from the exhibition UI
- Fees
- AI
- Subject-teacher assignment workflow

## Scanner
The scanner is not shown in the main navigation. Direct route:
`/attendance/scan`

## Render environment
Required:
- DATABASE_URL
- SECRET_KEY
- JWT_SECRET_KEY
- INITIAL_ADMIN_USERNAME
- INITIAL_ADMIN_PASSWORD
- APP_TIMEZONE=Asia/Kolkata
- ATTENDANCE_PRESENT_FROM=07:30
- ATTENDANCE_LATE_AFTER=08:30
- ATTENDANCE_ABSENT_AFTER=09:00
- TRUST_PROXY_HEADERS=true
- SCANNER_ALLOWED_IPS= (leave empty while testing)

## Note
The attendance recognition algorithm is based on the user's original public repository workflow: HOG face detection, image-quality checks, multiple verification frames, best-match scoring, and duplicate-safe attendance marking.
