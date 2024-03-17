from data import db_session
from data.departments import Department
from data.jobs import Jobs
from data.users import User


def main():
    db_session.global_init('db/database.db')
    db_sess = db_session.create_session()

    members = db_sess.query(Department).filter(Department.id == 1).first().members.split(", ")

    for member in members:
        sum_hours = 0
        for job in db_sess.query(Jobs).all():
            if str(member) in job.collaborators:
                sum_hours += job.work_size
        if sum_hours > 25:
            user = db_sess.query(User).filter(User.id == int(member)).first()
            print(user.name, user.surname)


main()