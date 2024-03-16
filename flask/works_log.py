from flask import Flask, render_template

from data import db_session
from data.jobs import Jobs
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/works_log')
def works_log():
    db_session.global_init('db/database.db')
    db_sess = db_session.create_session()

    jobs = []

    for elem in db_sess.query(Jobs).all():
        jobs.append({'job': elem.job,
                     'leader': elem.team_leader,
                     'dur': elem.work_size,
                     'cols': elem.collaborators,
                     'fin': elem.is_finished})

    for job in jobs:
        for user in db_sess.query(User).filter(User.id == job['leader']).all():
            job.update(
                {'leader': [user.surname, user.name]}
            )

    return render_template('works_log.html', jobs=jobs)


def main():
    db_session.global_init('db/database.db')
    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    main()
