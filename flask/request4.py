import datetime

from data import db_session
from data.users import User


def main():
    db_session.global_init('db/database.db')
    db_sess = db_session.create_session()

    for user in db_sess.query(User).filter(User.address == 'module_1', User.age < 21).all():
        user.address = 'module_3'
        user.modified_date = datetime.datetime.now()
        db_sess.commit()


if __name__ == '__main__':
    main()