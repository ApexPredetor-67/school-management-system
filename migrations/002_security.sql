-- Optional defense-in-depth for Supabase Data API access.
-- The Flask app primarily uses the private Postgres connection; do not expose these tables through the Data API unless you have reviewed the policies.
DO $$ DECLARE t text; BEGIN
  FOREACH t IN ARRAY ARRAY['account','student','parent','parent_student','teacher','teacher_assignment','subject','exam','mark','assessment_component','attendance','school_calendar','announcement','result_publication','audit_event','school_setting','published_report','fee_invoice','fee_payment'] LOOP
    EXECUTE format('alter table if exists public.%I enable row level security', t);
  END LOOP;
END $$;

-- Keep audit_event effectively private to Data API roles by not granting access.
REVOKE ALL ON TABLE public.audit_event FROM anon, authenticated;
