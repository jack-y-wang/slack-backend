from app.controllers import *
from flask import request
from app.dao import users_dao

class CreateUserController(Controller):
    def get_name(self):
        return "create-user"
        
    def get_path(self):
        return "/users/"
    
    def get_methods(self):
        return ["POST"]
    
    def content(self):
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        username = data.get('username')
        profile_img = data.get('image')

        user = users_dao.create_user(name, email, username, profile_img)
        return user.serialize()
