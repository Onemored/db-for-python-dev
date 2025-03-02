import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Course, Homework

# Cессия
DSN = f"postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

course1 = Course(name='Python')
course2 = Course(name='Java')

session.add_all([course1, course2])

print(course1)

hw1 = Homework(number=1, description='Простая домашняя работа', course=course1)
hw2 = Homework(number=2, description='Сложная домашняя работа', course=course1)
# hw3 = Homework(number=2, description='Простая домашняя работа', course=course2)
# hw4 = Homework(number=1, description='Сложная домашняя работа', course=course2)
session.add_all([hw1, hw2])

for c in session.query(Homework).all():
    print(c)
# С фильтром
for c in session.query(Homework).filter(Homework.number > 1).all():
    print(f'С фильтром > 1: {c}')

for c in session.query(Homework).filter(Homework.description.like('%ложная%')).all():
    print(f'С фильтром LIKE: {c}')

# Объеденение таблиц.
for c in session.query(Course).join(Homework.course).all():
    print(c)

# Подзапрос
subq = session.query(Homework).filter(Homework.description.like('%остая%')).subquery()
for c in session.query(Course).join(subq, Course.id == subq.c.course_id).all():
    print(f'Подзапрос: {c}')



# Поиск обьектов
session.query(Course).filter(Course.name == 'Java').update({'name': 'JavaScript'})

session.query(Course).filter(Course.name == 'JavaScript').delete()

for c in session.query(Course).all():
    print(c)


session.close()