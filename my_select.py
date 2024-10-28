from sqlalchemy import func, and_
from sqlalchemy.orm import sessionmaker
from models import engine, Student, Grade, Subject, Teacher, Group

Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    return session.query(
        Student.name,
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).join(Grade).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).limit(5).all()

def select_2(subject_name):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    return session.query(
        Student.name,
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).join(Grade).join(Subject).filter(
        Subject.name == subject_name
    ).group_by(Student.id).order_by(func.avg(Grade.grade).desc()).first()

def select_3(subject_name):
    """Знайти середній бал у групах з певного предмета."""
    return session.query(
        Group.name,
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).select_from(Group).join(Student).join(Grade).join(Subject).filter(
        Subject.name == subject_name
    ).group_by(Group.name).all()

def select_4():
    """Знайти середній бал на потоці."""
    return session.query(
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).scalar()

def select_5(teacher_name):
    """Знайти які курси читає певний викладач."""
    return session.query(
        Subject.name
    ).join(Teacher).filter(
        Teacher.name == teacher_name
    ).all()

def select_6(group_name):
    """Знайти список студентів у певній групі."""
    return session.query(
        Student.name
    ).join(Group).filter(
        Group.name == group_name
    ).all()

def select_7(group_name, subject_name):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    return session.query(
        Student.name,
        Grade.grade,
        Grade.date_received
    ).join(Group).join(Grade).join(Subject).filter(
        and_(Group.name == group_name, Subject.name == subject_name)
    ).all()

def select_8(teacher_name):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    return session.query(
        func.round(func.avg(Grade.grade), 2).label('avg_grade')
    ).join(Subject).join(Teacher).filter(
        Teacher.name == teacher_name
    ).scalar()

def select_9(student_name):
    """Знайти список курсів, які відвідує певний студент."""
    return session.query(
        Subject.name
    ).join(Grade).join(Student).filter(
        Student.name == student_name
    ).distinct().all()

def select_10(student_name, teacher_name):
    """Список курсів, які певному студенту читає певний викладач."""
    return session.query(
        Subject.name
    ).join(Grade).join(Student).join(Teacher).filter(
        and_(Student.name == student_name, Teacher.name == teacher_name)
    ).distinct().all()

if __name__ == "__main__":
    
    print("Top 5 students by average grade:")
    print(select_1())
    
    print("\nBest student in 'Програмування':")
    print(select_2("Програмування"))
    