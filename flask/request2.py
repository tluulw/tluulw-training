from data import db_session
from data.users import User
from data.jobs import Jobs


def main():
    db_session.global_init('db/database.db')
    db_sess = db_session.create_session()
    for job in db_sess.query(Jobs).filter(Jobs.work_size < 20, Jobs.is_finished == 0).all():
        print(repr(job))


if __name__ == '__main__':
    main()