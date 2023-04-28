from sqlalchemy import func, desc, select, and_

from src.models import Teacher, Student, Subject, Grade, Group
from src.db import session


#Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
def select_1():
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
        .select_from(Grade).join(Student).group_by(Student.id).order_by(desc('avg_grade')).limit(5).all()
    return result

#Знайти студента із найвищим середнім балом з певного предмета.
def select_2(subject_id):
    result = session.query(Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
    .select_from(Grade).join(Student).where(Grade.subject_id == subject_id).group_by(Student.id) \
    .order_by(desc('avg_grade')).limit(1).all()
    return result

#Знайти середній бал у групах з певного предмета.
def select_3(group_id, subject_id):
    result = session.query(Group.name, Subject.name, func.round(func.avg(Grade.grade), 2)) \
    .select_from(Grade).join(Subject).join(Student).join(Group).filter(and_(Student.group_id == group_id, Grade.subject_id == subject_id)) \
    .group_by(Subject.name, Group.name).all()
    return result

#Знайти середній бал на потоці (по всій таблиці оцінок).
def select_4():
    result = session.query(func.round(func.avg(Grade.grade)).label('avg_grade')).select_from(Grade).all()
    return result

#Знайти які курси читає певний викладач.
def select_5(teacher_id):
    result = session.query(Subject.name).select_from(Subject).where(Subject.teacher_id == teacher_id).all()
    return result

#Знайти список студентів у певній групі.
def select_6(group_id):
    result = session.query(Student.fullname).select_from(Student).filter(Student.group_id == group_id).all()
    return result

#Знайти оцінки студентів у окремій групі з певного предмета.
def select_7(group_id, subject_id):
    result = session.query(Student.fullname, Grade.grade).select_from(Grade).join(Student) \
    .filter(and_(Student.group_id == group_id, Grade.subject_id == subject_id)).order_by(desc(Grade.grade)).all()
    return result

#Знайти середній бал, який ставить певний викладач зі своїх предметів.
def select_8(teacher_id):
    result = session.query(Subject.name, func.round(func.avg(Grade.grade), 2)).select_from(Grade).join(Subject) \
    .filter(Subject.teacher_id == teacher_id).group_by(Subject.name).all()
    return result

#Знайти список курсів, які відвідує певний студент.
def select_9(student_id):
    result = session.query(Subject.name).select_from(Grade).join(Subject).filter(Grade.student_id == student_id) \
    .group_by(Subject.name).all()
    return result

#Список курсів, які певному студенту читає певний викладач.
def select_10(teacher_id, student_id):
    result = session.query(Subject.name).select_from(Grade).join(Subject) \
    .filter(and_(Grade.student_id == student_id, Subject.teacher_id == teacher_id)).group_by(Subject.name).all()
    return result 

#Середній бал, який певний викладач ставить певному студентові.
def select_11(teacher_id, student_id):
    result = session.query(Teacher.fullname, Student.fullname, func.round(func.avg(Grade.grade), 2).label('avg_grade')) \
    .select_from(Grade).join(Student).join(Subject).join(Teacher).filter(and_(Subject.teacher_id == teacher_id, Grade.student_id == student_id)) \
    .group_by(Teacher.fullname, Student.fullname).all()
    return result

#Оцінки студентів у певній групі з певного предмета на останньому занятті.
def select_12(group_id, subject_id):
    max_date = session.query(func.max(Grade.date)).select_from(Grade).one()[0]
    result = session.query(Student.fullname, Grade.grade).select_from(Grade).join(Student).join(Subject) \
    .filter(and_(Student.group_id == group_id, Subject.id == subject_id, Grade.date == max_date)) \
    .group_by(Student.fullname, Grade.grade).order_by(desc(Grade.grade)).all()
    return result


if __name__ == '__main__':
   print(select_12(1, 3))

