from flask_restful import Resource
from flask import request
from flask_jwt_extended import create_access_token
from models import db, User

class LoginResource(Resource):
    def post(self):

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return {'message': 'Username and password are required'}, 400
        
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            return {
                'message': 'Login successful',
                'access_token': access_token,
                'user': user.to_dict()    
            }, 200
        else:
            return {'message': 'Invalid username or password.'}, 401