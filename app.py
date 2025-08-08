from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from resources.user import UserResource
from resources.task import TaskResource, UserTasksResource
from resources.register import RegisterResource
from resources.login import LoginResource
from resources.logout import LogoutResource
from blocklist import BLOCKLIST

app = Flask(__name__)
CORS(app, origins=[
    'http://localhost:3000',  # local dev frontend URL
    'https://task-manager-frontend-5er9.vercel.app',  # your deployed frontend URL here
], supports_credentials=True)
app.config.from_object(Config)

# Add a secret key for JWT (set this in your Config)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key_here'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

jwt = JWTManager(app)

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Add blocklist check callback
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLOCKLIST

api.add_resource(UserResource, '/api/users')
api.add_resource(TaskResource, '/api/tasks', endpoint='tasks')
api.add_resource(TaskResource, '/api/tasks/<int:task_id>', endpoint='task_by_id')
api.add_resource(UserTasksResource, '/api/users/<int:user_id>/tasks')
api.add_resource(RegisterResource, '/api/register')
api.add_resource(LoginResource, '/api/login')
api.add_resource(LogoutResource, '/api/logout')

if __name__ == '__main__':
    app.run(debug=True)