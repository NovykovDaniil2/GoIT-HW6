--Знайти середній бал, який ставить певний викладач зі своїх предметів.
SELECT s.name AS subject, ROUND(AVG(g.grade), 2) AS average_teacher_grade
FROM grades g 
JOIN subjects s ON s.id = g.subject_id 
WHERE s.teacher_id  = ?
GROUP BY s.name; 