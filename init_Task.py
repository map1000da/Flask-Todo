from app import db, Task
import datetime

db.create_all()

task1 = Task("add", datetime.date(2023, 5, 21))
task2 = Task("push", datetime.date(2023, 5, 23))

db.session.add_all([task1, task2])

db.session.commit()