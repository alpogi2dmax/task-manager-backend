from flask_jwt_extended import jwt_required, get_jwt
from flask_restful import Resource
from blocklist import BLOCKLIST

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {'message': 'Successfully logged out'}, 200