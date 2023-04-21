--Знайти список курсів, які відвідує студент.
SELECT s.name
FROM grades g
JOIN subjects s ON s.id = g.subject_id 
WHERE g.student_id = ?
GROUP BY s.name;
