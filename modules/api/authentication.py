from flask_restful import Resource
from flask import request
from models.User import User
from database import db
from flask_jwt_extended import create_access_token

class Authentication(Resource):

    def post(self, function):
        if function == "register":
            username = request.form.get("username")
            password = request.form.get("password")
            response = self.register_user(username, password)
            return response
        
        elif function == "login":
            username = request.form.get("username")
            password = request.form.get("password")
            response = self.login_user(username, password)
            return response

    def register_user(self, username, password):

        if not (username or password):
            return {"message": "Username or Password not provided"}, 400
        
        user_obj = User.query.filter_by(username=username).first()
        if user_obj:
            return {"message": "User already exists"}, 400

        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return {"message": f"User with username:{username} created successfully!"}, 200
    
    def login_user(self, username, password):
        
        user_obj = User.query.filter_by(username=username).first()
        if user_obj and user_obj.check_password(password):
            jwt_access_token = create_access_token(user_obj.id)
            return {"access_token":jwt_access_token},200
        
        elif not user_obj:
            return {"message": "User doesn't exist. Please register first."}, 400

        return {"message": "Incorrect credentials"}, 401
