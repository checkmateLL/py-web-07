from faker import Faker
from sqlalchemy.orm import sessionmaker
from models import engine, Student, Group, Teacher, Subject, Grade
import random
from datetime import datetime, date
from random import randint, choice, uniform

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
fake = Faker('uk_UA') 

def create_database():
    # Clear existing data
    session.query(Grade).delete()
    session.query(Student).delete()
    session.query(Subject).delete()
    session.query(Teacher).delete()
    session.query(Group).delete()
    session.commit()

    # Create groups
    groups = [Group(name=f"Група {i}") for i in range(1, 4)]
    session.add_all(groups)
    session.commit()

    # Create teachers 
    teachers = [Teacher(name=fake.name()) for _ in range(randint(3, 5))]
    session.add_all(teachers)
    session.commit()

    # Create subjects
    subject_names = [
        "Вища математика",
        "Фізика",
        "Програмування",
        "Англійська мова",
        "Історія України",
        "Бази даних",
        "Веб-розробка",
        "Комп'ютерні мережі"
    ]
    subjects = []
    for name in subject_names[:randint(5, 8)]:
        subject = Subject(name=name, teacher=choice(teachers))
        subjects.append(subject)
    session.add_all(subjects)
    session.commit()

    # Create students
    students = [
        Student(name=fake.name(), group=choice(groups))
        for _ in range(randint(30, 50))
    ]
    session.add_all(students)
    session.commit()

    # Create grades
    for student in students:
        for subject in subjects:
            # Generate 1-20 grades
            num_grades = randint(1, 20)
            for _ in range(num_grades):
                grade = Grade(
                    student=student,
                    subject=subject,
                    grade=uniform(60.0, 100.0),
                    date_received=fake.date_between(
                        start_date=date(2023, 9, 1),
                        end_date=date(2024, 6, 30)
                    )
                )
                session.add(grade)

    session.commit()

if __name__ == "__main__":
    create_database()
    session.close()