from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.user import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/works_log")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/works_log")


def main():
    db_session.global_init('db/database.db')
    app.run(port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()
