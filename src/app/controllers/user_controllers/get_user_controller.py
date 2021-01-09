from app.controllers import *
from flask import request
from app.dao import users_dao

class GetUserController(Controller):
    def get_path(self):
        return "/users/<int:user_id>/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, user_id):
        user = users_dao.get_user_by_id(user_id)
        return user.serialize()
