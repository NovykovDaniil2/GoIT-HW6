--Знайти середній бал у групах з певного предмета.
SELECT sbj.name AS subject, gr.name AS group_name, ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g 
JOIN students s ON s.id = g.student_id 
JOIN subjects sbj ON sbj.id = g.subject_id 
JOIN [groups] gr ON gr.id = s.group_id
WHERE sbj.id = ?
GROUP BY gr.name, sbj.name 
ORDER BY average_grade DESC;