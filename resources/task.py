from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Task, User

class TaskResource(Resource):
    @jwt_required()
    def post(self):
        data = request.get_json()
        title=data.get('title')
        description=data.get('description')
        completed=data.get('completed', False)
        # user_id=data.get('user_id')

        current_user_id = int(get_jwt_identity())

        if not title:
            return {"message": "Title are required."}, 400
        

        user = User.query.get(current_user_id)
        if not user:
            return {"message": f"User with id {current_user_id} does not exist."}, 400

        task = Task(
            title=title,
            description=description,
            completed=completed,
            user_id=current_user_id
        )

        db.session.add(task)
        db.session.commit()

        return task.to_dict(), 201

    @jwt_required()
    def patch(self, task_id):
        data = request.get_json()
        task = Task.query.get(task_id)

        if not task:
            return {'message': f'Task with id {task_id} not found'}, 404
        
        current_user_id = int(get_jwt_identity())
        if task.user_id != current_user_id:
            return {'message': 'Access denied'}, 403
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'completed' in data:
            task.completed = data['completed']

        db.session.commit()

        return task.to_dict(), 200

    @jwt_required()   
    def delete(self, task_id):
        task = Task.query.get(task_id)

        if not task:
            return {'message': f'Task with id {task_id} not found.'}, 404
        
        current_user_id = int(get_jwt_identity())
        if task.user_id != current_user_id:
            return {'message': 'Access denied'}, 403
        
        db.session.delete(task)
        db.session.commit()
        return {'message': f'Task {task_id} deleted successfully.'}, 200
    
class UserTasksResource(Resource):
    @jwt_required()
    def get(self, user_id):
        current_user_id = int(get_jwt_identity())
        if current_user_id != int(user_id):
            return {'message': 'Access denied'}, 400
        user = User.query.get_or_404(user_id)
        return [task.to_dict() for task in user.tasks], 200

