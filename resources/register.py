from flask_restful import Resource, reqparse
from flask import request
from models import db, User


# user_parser = reqparse.RequestParser()
# user_parser.add_argument('username', type=str, required=True)
# user_parser.add_argument('first_name', type=str, required=True)
# user_parser.add_argument('last_name', type=str, required=True)
# user_parser.add_argument('password', type=str, required=True)

class RegisterResource(Resource):
    def post(self):
        # args = user_parser.parse_args()

        data = request.get_json()
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        password = data.get('password')

        # simple manual validation
        if not all([username, first_name, last_name, password]):
            return {'message': 'Missing required fields'}, 400
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return {'message': 'Username already exists'}, 400

        user = User(username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return user.to_dict(), 201