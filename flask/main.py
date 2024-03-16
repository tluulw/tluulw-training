from flask import Flask, render_template, redirect
from flask_login import LoginManager

from data import db_session
from data.jobs import Jobs
from data.news import News
from data.users import User
from forms.user import Login2xForm, RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


profs = ['инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач', 'инженер по терраформированию',
         'климатолог', 'специалист по радиационной защите', 'астрогеолог', 'гляциолог',
         'инженер жизнеобеспечения', 'метеоролог', 'оператор марсохода', 'киберинженер', 'штурман',
         'пилот дронов']

anketa = {'title': 'Анкета', 'surname': 'Watny', 'name': "Mark", 'education': 'выше среднего',
          'profession': "штурман марсохода", 'sex': "male", 'motivation': "Всегда мечтал застрять на Марсе!",
          'ready': 'True'}


@app.route('/list_prof')
@app.route('/list_prof/<type>')
def list_prof(type=None):
    if type is None:
        return render_template('list.html', title='Заготовка', list=profs, type=type)
    if type == 'ul' or type == 'ol':
        return render_template('list.html', title='Заготовка', list=profs, type=type)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


@app.route('/answer')
@app.route('/auto_answer')
def auto_answer():
    return render_template('auto_answer.html',
                           title=anketa['title'],
                           surname=anketa['surname'],
                           name=anketa['name'],
                           education=anketa['education'],
                           profession=anketa['profession'],
                           sex=anketa['sex'],
                           motivation=anketa['motivation'],
                           ready=anketa['ready'],
                           )


@app.route('/training/<prof>')
def training(prof):
    if 'инженер' in prof or 'строитель' in prof:
        return render_template('training.html', prof='it')
    else:
        return render_template('training.html', prof='ns')


@app.route('/login')
def aut():
    form = Login2xForm()
    return render_template('2x_protection.html', form=form)


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
        return redirect('/')
    return render_template('register.html', title='Регистрация', form=form)


def main():
    db_session.global_init('db/database.db')
    app.run(port=5000, host='127.0.0.1')


if __name__ == '__main__':
    main()
