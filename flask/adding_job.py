from flask import Flask, render_template, redirect
from flask_login import LoginManager, current_user

from data import db_session
from data.jobs import Jobs
from data.news import News
from data.users import User
from forms.user import AddJobForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True))
    else:
        news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


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


@app.route('/addjob', methods=['GET', 'POST'])
def add_job():
    form = AddJobForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if db_sess.query(Jobs).filter(Jobs.job == form.job_title.data).first():
            return render_template('add_job.html', title='Adding a job',
                                   form=form,
                                   message="Работа с таким названием уже существует")
        job = Jobs(
            job=form.job_title.data,
            team_leader=form.team_leader.data,
            work_size=form.work_size.data,
            collaborators=form.collaborators.data,
            is_finished=form.is_finished.data,
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/works_log')
    return render_template('add_job.html', title='Adding a job', form=form)


def main():
    db_session.global_init('db/database.db')
    app.run(port=8000, host='127.0.0.1')


if __name__ == '__main__':
    main()
