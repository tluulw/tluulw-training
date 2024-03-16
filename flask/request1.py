from flask import Flask

from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init('db/database.db')
    db_sess = db_session.create_session()
    for user in db_sess.query(User).filter((User.position.like('%middle%')) | (User.position.like('%chief%'))).all():
        print(user)


if __name__ == '__main__':
    main()