--Знайти студента із найвищим середнім балом з певного предмета.
SELECT sbj.name AS subject, s.fullname AS student, ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g 
JOIN students s ON s.id = g.student_id 
JOIN subjects sbj ON sbj.id = g.subject_id 
WHERE sbj.id = ?
GROUP BY s.fullname 
ORDER BY average_grade DESC
LIMIT 1;