import datetime

from flask import jsonify
from flask_restful import Resource, abort

from data import db_session
from data.users import User
from users_parser import parser


def abort_if_user_is_not_found(user_id):
    db_sess = db_session.create_session()
    if not db_sess.query(User).filter(User.id == user_id).first():
        abort(404, message=f"User {user_id} not found")


def fields_are_correct(data):
    db_sess = db_session.create_session()

    fields = ['email', 'password', 'password_again', 'surname', 'name', 'age', 'position', 'speciality', 'address']

    if len(data) < len(fields) or len(data) > len(fields):
        abort(404, message="Incorrect request")

    if data['password'] != data['password_again']:
        abort(404, message="Passwords are not the same")

    if db_sess.query(User).filter(User.email == data['email']).first():
        abort(404, message="User with this email is already registered")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_is_not_found(user_id)

        db_sess = db_session.create_session()

        user = db_sess.query(User).filter(User.id == user_id).all()

        return jsonify(
            {
                'user':
                    [item.to_dict(only=('name', 'surname'))
                     for item in user]
            }
        )

    def delete(self, user_id):
        abort_if_user_is_not_found(user_id)

        db_sess = db_session.create_session()

        user = db_sess.query(User).filter(User.id == user_id).all()[0]

        db_sess.delete(user)

        if db_sess.query(User).filter(User.id == user_id + 1).first():
            for user in db_sess.query(User).filter(User.id > user_id).all():
                user.id -= 1

        db_sess.commit()

        return jsonify({'success': 'DELETED'})

    def put(self, user_id):
        db_sess = db_session.create_session()

        data = parser.parse_args()
        abort_if_user_is_not_found(user_id)
        fields_are_correct(data)

        user = db_sess.query(User).filter(User.id == user_id).all()[0]

        user.surname = data['surname']
        user.name = data['name']
        user.age = data['age']
        user.position = data['position']
        user.speciality = data['speciality']
        user.address = data['address']
        user.email = data['email']
        user.modified_date = datetime.datetime.now()

        user.set_password(data['password'])

        db_sess.commit()

        return jsonify({'success': 'EDITED'})


class UsersListResource(Resource):
    def post(self):
        print('ok')
        data = parser.parse_args()

        fields_are_correct(data)

        db_sess = db_session.create_session()

        user = User(
            surname=data['surname'],
            name=data['name'],
            age=data['age'],
            position=data['position'],
            speciality=data['speciality'],
            address=data['address'],
            email=data['email'],
            modified_date=datetime.datetime.now()
        )
        user.set_password(data['password'])

        db_sess.add(user)
        db_sess.commit()

        return jsonify({'success': 'ADDED'})

    def get(self):
        db_sess = db_session.create_session()

        users = db_sess.query(User).all()

        return jsonify(
            {
                'users':
                    [item.to_dict(only=('name', 'surname'))
                     for item in users]
            }
        )