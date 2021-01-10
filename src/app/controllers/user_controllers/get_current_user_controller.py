from app.controllers import *
from flask import request
from app.dao import users_dao
from app.dao import sessions_dao

class GetCurrentUserController(Controller):
    def get_path(self):
        return "/user/"
    
    def get_methods(self):
        return ["GET"]
    
    @authorize_user
    def content(self, **kwargs):
        user = kwargs.get("user")
        return user.serialize()
