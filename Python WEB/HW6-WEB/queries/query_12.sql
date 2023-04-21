--Оцінки студентів у певній групі з певного предмета на останньому занятті.
SELECT s.fullname, sbj.name , g.grade 
FROM grades g
JOIN students s ON s.id = g.student_id 
JOIN subjects sbj ON sbj.id = g.subject_id 
WHERE (
	s.group_id = ? AND
	g.subject_id = ? AND
	g.date_of = (SELECT g.date_of
				FROM grades g
				ORDER BY g.date_of DESC
				LIMIT 1)
	);