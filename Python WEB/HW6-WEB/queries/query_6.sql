--Знайти список студентів у певній групі.
SELECT s.fullname AS student_name
FROM students s
WHERE s.group_id = ?
ORDER BY s.fullname;