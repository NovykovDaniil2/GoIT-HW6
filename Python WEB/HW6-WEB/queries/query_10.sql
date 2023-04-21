--Список курсів, які певному студенту читає певний викладач.
SELECT sbj.name
FROM grades g 
JOIN subjects sbj ON sbj.id = g.subject_id 
WHERE g.student_id = ? AND sbj.teacher_id = ?
GROUP BY sbj.name;