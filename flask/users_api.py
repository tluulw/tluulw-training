import datetime

from flask import Blueprint, request, jsonify, make_response

from data import db_session
from data.users import User

blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db_sess = db_session.create_session()

    users = db_sess.query(User).all()

    return jsonify(
        {
            'users':
                [item.to_dict()
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()

    if db_sess.query(User).filter(User.id == user_id).all():
        pass
    else:
        return make_response(jsonify({'error': f'Incorrect user id: user was not founded'}), 404)

    user = db_sess.query(User).filter(User.id == user_id).all()

    return jsonify(
        {
            'user':
                [item.to_dict()
                 for item in user]
        }
    )


@blueprint.route('/api/users/register', methods=['POST'])
def register():
    db_sess = db_session.create_session()

    data = request.json

    fields = ['email', 'password', 'password_again', 'surname', 'name', 'age', 'position', 'speciality', 'address']

    if len(data) < len(fields) or len(data) > len(fields):
        return make_response(jsonify({'error': 'Bad request'}), 404)

    if data['password'] != data['password_again']:
        return make_response(jsonify({'error': 'Passwords are not the same'}), 404)

    if db_sess.query(User).filter(User.email == data['email']).first():
        return make_response(jsonify({'error': 'User with this email is already registered'}), 404)

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

    return make_response(jsonify({'status': 'User was registered'}), 200)


@blueprint.route('/api/users/delete_user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db_sess = db_session.create_session()

    if not db_sess.query(User).filter(User.id == user_id).first():
        return make_response(jsonify({'error': f'Incorrect user id: {user_id}'}), 404)

    user = db_sess.query(User).filter(User.id == user_id).all()[0]

    db_sess.delete(user)

    if db_sess.query(User).filter(User.id == user_id + 1).first():
        for user in db_sess.query(User).filter(User.id > user_id).all():
            user.id -= 1

    db_sess.commit()

    return make_response(jsonify({'status': 'User was deleted'}), 200)


@blueprint.route('/api/users/edit_user/<int:user_id>', methods=['PUT'])
def edit_user(user_id):
    db_sess = db_session.create_session()

    data = request.json

    if not db_sess.query(User).filter(User.id == user_id).first():
        return make_response(jsonify({'error': f'Incorrect user id: {user_id}'}), 404)

    fields = ['email', 'password', 'password_again', 'surname', 'name', 'age', 'position', 'speciality', 'address']

    if len(data) < len(fields) or len(data) > len(fields):
        return make_response(jsonify({'error': 'Bad request'}), 404)

    if data['password'] != data['password_again']:
        return make_response(jsonify({'error': 'Passwords are not the same'}), 404)

    if db_sess.query(User).filter(User.email == data['email']).first():
        return make_response(jsonify({'error': 'User with this email is already registered'}), 404)

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

    return make_response(jsonify({'status': 'User was edited'}), 200)
