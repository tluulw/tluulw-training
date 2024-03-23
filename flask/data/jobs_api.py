import json

from flask import Blueprint, render_template

from . import db_session
from .jobs import Jobs
from .users import User

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()

    jobs = {}

    for elem in db_sess.query(Jobs).all():
        jobs['jobs'] = jobs.get('jobs', []) + [{'id': elem.id,
                                                'job': elem.job,
                                                'leader': elem.team_leader,
                                                'dur': elem.work_size,
                                                'cols': elem.collaborators,
                                                'fin': elem.is_finished}]

    return json.dumps(jobs)


@blueprint.route('/api/jobs/<int:job_id>')
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


@blueprint.route('/api/jobs/<path:job_path>')
def iskl(job_path):
    return f'Неверный id работы: {job_path}'