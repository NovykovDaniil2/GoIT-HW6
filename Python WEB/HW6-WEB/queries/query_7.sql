--Знайти оцінки студентів у окремій групі з певного предмета.
SELECT s.fullname AS student, g.grade
FROM [grades] g 
JOIN students s ON s.id = g.student_id
WHERE g.subject_id = ? AND s.group_id = ?
ORDER BY s.fullname;
