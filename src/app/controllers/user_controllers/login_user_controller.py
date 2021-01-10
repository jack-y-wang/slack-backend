from app.controllers import *
from flask import request
from app.dao import users_dao
from app.dao import sessions_dao

class LoginUserController(Controller):
    def get_path(self):
        return "/login/"
    
    def get_methods(self):
        return ["POST"]
    
    def content(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get('password')

        if not password or not email:
            raise Exception("missing password or email")
            
        success, user = users_dao.verify_credentials(email, username, password)
        if not success:
            raise Exception("Email or Password are incorrect")

        return user.serialize_session()
