import bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy_mixins import AllFeaturesMixin

db = SQLAlchemy()

class BaseModel(db.Model, SerializerMixin):
    __abstract__ = True

class User(BaseModel):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    _password = db.Column('password', db.LargeBinary(128), nullable=False)

    tasks = db.relationship('Task', backref='user', lazy=True)

    def set_password(self, password):
        self._password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self._password)
    
    serialize_rules = ('-_password', 'tasks', '-tasks.user')
    
class Task(BaseModel):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    serialize_rules = ('-user',)
