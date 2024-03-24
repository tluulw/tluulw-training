import datetime

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.user import RegisterForm, LoginForm, AddJobForm
import jobs_api

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
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/')
def works_log():
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = AddJobForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Jobs).filter(Jobs.job == form.job_title.data).first():
            return render_template('add_job.html', title='Adding a job',
                                   form=form,
                                   message="Работа с таким названием уже существует", h='Adding a Job')
        job = Jobs(
            job=form.job_title.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Adding a job', form=form, h='Adding a Job')


@app.route('/edit_job/<int:id>', methods=['GET', 'POST'])
def edit_job(id):
    form = AddJobForm()
    db_sess = db_session.create_session()

    for job in db_sess.query(Jobs).filter(Jobs.id == id).all():
        if current_user.id != 1 and current_user.id != job.team_leader:
            return redirect('/')

    if form.validate_on_submit():
        print(form.job_title.data)
        if db_sess.query(Jobs).filter(Jobs.job == form.job_title.data).first():
            return render_template('add_job.html', title='Editing a job',
                                   form=form,
                                   message="Работа с таким названием уже существует", h='Editing a Job')

        job = db_sess.query(Jobs).filter(Jobs.id == id).all()[0]
        job.job = form.job_title.data
        job.team_leader = form.team_leader.data
        job.work_size = form.work_size.data
        job.collaborators = form.collaborators.data
        job.start_date = datetime.datetime.now()
        job.end_date = datetime.datetime.now()
        job.is_finished = form.is_finished.data

        db_sess.commit()

        return redirect('/')

    for job in db_sess.query(Jobs).filter(Jobs.id == id).all():
        form.job_title.data = job.job
        form.team_leader.data = job.team_leader
        form.work_size.data = job.work_size
        form.collaborators.data = job.collaborators
        form.is_finished.data = job.is_finished
    return render_template('add_job.html', title='Editing a job', form=form, h='Editing a Job')


@app.route('/delete_job/<int:id>', methods=['DELETE'])
def delete_job(id):
    db_sess = db_session.create_session()

    job = db_sess.query(Jobs).filter(Jobs.id == id).all()[0]

    if current_user.id != 1 and current_user.id != job.team_leader:
        return redirect('/')

    db_sess.delete(job)

    if db_sess.query(Jobs).filter(Jobs.id == id + 1).first():
        for job in db_sess.query(Jobs).filter(Jobs.id > id).all():
            job.id = job.id - 1

    db_sess.commit()

    return redirect('/')


def main():
    db_session.global_init('db/database.db')
    app.register_blueprint(jobs_api.blueprint)
    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    main()