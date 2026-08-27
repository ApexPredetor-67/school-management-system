# DAV PS KKP — Final Exhibition School Management

V11-based school management system with the existing UI preserved and a refined backend for administration, teachers, students, parents, attendance, academics, report cards, announcements, calendar, and manual fee verification.

### Existing main demo areas
- Admin
- Teacher
- Student registration
- Parent linking
- Attendance
- Academics
- Report cards
- Announcements
- School calendar

### Attendance scanner
Direct route only: `/attendance/scan`

The scanner is intentionally hidden from normal navigation. It keeps the existing seven-frame recognition UI/workflow, adds conservative ambiguity rejection, calendar/time-window enforcement, and duplicate-safe attendance recording.

### Fees
The fee backend preserves the supplied 2026–27 structure and payment windows. It does **not** generate invoices automatically. Payment verification is manual.

### AI
`POST /api/ai` provides a local, scope-limited school-data assistant. It uses only the students visible to the logged-in account and does not depend on an external API quota.

## Local HTTPS / phone access
Set `LOCAL_HTTPS=true` in `.env.local`. With `SSL_ADHOC=true`, the app will serve an HTTPS development certificate on `https://<YOUR-LAN-IP>:5000`. A phone on the same Wi-Fi can reach it using the laptop's LAN IP; the browser may show a certificate warning because it is a development certificate. For Render, leave `LOCAL_HTTPS=false`; Render should terminate HTTPS at its proxy.
