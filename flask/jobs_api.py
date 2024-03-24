from flask import Blueprint, render_template, request, jsonify, make_response

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.user import AddJobForm

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()

    jobs = db_sess.query(Jobs).all()

    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()

    if db_sess.query(Jobs).filter(Jobs.id == job_id).all():
        pass
    else:
        return f'Неверный id работы: {job_id}'

    jobs = []

    for elem in db_sess.query(Jobs).filter(Jobs.id == job_id).all():
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


@blueprint.route('/api/jobs/<path:job_path>', methods=['GET'])
def iskl(job_path):
    return f'Неверный id работы: {job_path}'


@blueprint.route('/api/jobs/add_job', methods=['POST'])
def add_job():
    form = AddJobForm()

    db_sess = db_session.create_session()

    data = request.json

    fields = ['job_title', 'team_leader', 'work_size', 'collaborators', 'is_finished']

    if len(data) < len(fields) or len(data) > len(fields):
        return 'нехорошо'

    if db_sess.query(Jobs).filter(Jobs.job == data['job_title']).first():
        return 'Работа с таким названием уже существует'

    job = Jobs(
        job=data['job_title'],
        team_leader=data['team_leader'],
        work_size=data['work_size'],
        collaborators=data['collaborators'],
        is_finished=data['is_finished'],
    )

    db_sess.add(job)
    db_sess.commit()
    return 'Работа была добавлена'


@blueprint.route('/api/jobs/delete_job/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()

    job = db_sess.query(Jobs).filter(Jobs.id == job_id).all()[0]

    if not job:
        return make_response(jsonify({'error': 'Not found'}), 404)

    db_sess.delete(job)

    if db_sess.query(Jobs).filter(Jobs.id == job_id + 1).first():
        for job in db_sess.query(Jobs).filter(Jobs.id > id).all():
            job.id = job.id - 1

    db_sess.commit()

    return make_response(jsonify({'status': 'job was deleted'}), 200)