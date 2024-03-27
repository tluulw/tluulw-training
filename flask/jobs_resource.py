import datetime

from flask import jsonify
from flask_restful import Resource, abort

from data import db_session
from data.users import User
from data.jobs import Jobs
from jobs_parser import parser


def abort_if_job_is_not_found(job_id):
    db_sess = db_session.create_session()
    if not db_sess.query(Jobs).filter(Jobs.id == job_id).first():
        abort(404, message=f"Job {job_id} is not found")


def fields_are_correct(data):
    db_sess = db_session.create_session()

    fields = ['job', 'team_leader', 'work_size', 'collaborators', 'is_finished']

    if len(data) < len(fields) or len(data) > len(fields):
        abort(404, message=f"Bad request")

    if db_sess.query(Jobs).filter(Jobs.job == data['job']).first():
        abort(404, message=f"Job {data['job']} already exists")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_is_not_found(job_id)

        db_sess = db_session.create_session()

        jobs = db_sess.query(Jobs).filter(Jobs.id == job_id).all()

        jobs = [item.to_dict() for item in jobs]

        for job in jobs:
            for user in db_sess.query(User).filter(User.id == job['team_leader']).all():
                job.update(
                    {'team_leader': [user.surname, user.name]}
                )

        return jsonify({'jobs': jobs})

    def delete(self, job_id):
        abort_if_job_is_not_found(job_id)

        db_sess = db_session.create_session()

        job = db_sess.query(Jobs).filter(Jobs.id == job_id).all()[0]

        db_sess.delete(job)

        if db_sess.query(Jobs).filter(Jobs.id == job_id + 1).first():
            for job in db_sess.query(Jobs).filter(Jobs.id > job_id).all():
                job.id = job.id - 1

        db_sess.commit()

        return jsonify({'success': 'DELETED'})

    def put(self, job_id):
        db_sess = db_session.create_session()

        data = parser.parse_args()

        abort_if_job_is_not_found(job_id)
        fields_are_correct(data)

        job = db_sess.query(Jobs).filter(Jobs.id == job_id).all()[0]

        job.job = data['job']
        job.team_leader = data['team_leader']
        job.work_size = data['work_size']
        job.collaborators = data['collaborators']
        job.start_date = datetime.datetime.now()
        job.end_date = datetime.datetime.now()
        job.is_finished = data['is_finished']

        db_sess.commit()

        return jsonify({'success': 'EDITED'})


class JobsListResource(Resource):
    def post(self):
        data = parser.parse_args()

        fields_are_correct(data)

        db_sess = db_session.create_session()

        job = Jobs(
            job=data['job'],
            team_leader=data['team_leader'],
            work_size=data['work_size'],
            collaborators=data['collaborators'],
            is_finished=data['is_finished'],
        )

        db_sess.add(job)
        db_sess.commit()

        return jsonify({'success': 'ADDED'})

    def get(self):
        db_sess = db_session.create_session()

        jobs = db_sess.query(Jobs).all()

        return jsonify(
            {
                'jobs':
                    [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished'))
                     for item in jobs]
            }
        )