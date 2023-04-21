--Знайти які курси читає певний викладач.
SELECT t.fullname AS teacher, s.name AS subject
FROM subjects s
JOIN teachers t ON t.id = s.teacher_id
WHERE t.id = ?;