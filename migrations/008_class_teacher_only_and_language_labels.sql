-- V10: class-teacher-only academics + explicit 2nd/3rd language labels.
-- Subject-level teacher assignments are no longer required by the application.
UPDATE public.subject
SET name = CASE code
    WHEN 'lang2_telugu' THEN 'Telugu (2nd Language)'
    WHEN 'lang2_hindi' THEN 'Hindi (2nd Language)'
    WHEN 'lang2_sanskrit' THEN 'Sanskrit (2nd Language)'
    WHEN 'lang3_telugu' THEN 'Telugu (3rd Language)'
    WHEN 'lang3_hindi' THEN 'Hindi (3rd Language)'
    WHEN 'lang3_sanskrit' THEN 'Sanskrit (3rd Language)'
    ELSE name
END
WHERE code IN (
    'lang2_telugu','lang2_hindi','lang2_sanskrit',
    'lang3_telugu','lang3_hindi','lang3_sanskrit'
);
