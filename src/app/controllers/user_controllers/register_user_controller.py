from app.controllers import *
from flask import request
from app.dao import users_dao
from app.dao import sessions_dao

class RegisterUserController(Controller):
    def get_name(self):
        return "register-user"
        
    def get_path(self):
        return "/register/"
    
    def get_methods(self):
        return ["POST"]
    
    def content(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        username = data.get('username')
        password = data.get('password')
        profile_img = data.get('image')

        user = users_dao.create_user(name, email, username, password, profile_img)
        session = sessions_dao.create_session(user.id)

        return session.serialize_session()
