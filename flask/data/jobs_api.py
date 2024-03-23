import json

from flask import Blueprint

from . import db_session
from .jobs import Jobs

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_news():
    db_session.global_init('db/database.db')
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