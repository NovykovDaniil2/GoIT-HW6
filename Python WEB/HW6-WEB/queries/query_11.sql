--Середній бал, який певний викладач ставить певному студентові.
SELECT t.fullname AS teacher,st.fullname AS student, ROUND(AVG(g.grade), 2) AS average_grade
FROM grades g 
JOIN subjects s ON s.id = g.subject_id 
JOIN teachers t ON t.id = s.teacher_id
JOIN students st ON st.id = g.student_id 
WHERE s.teacher_id = ? AND g.student_id = ?;