from app.controllers import *
from flask import request
from app.dao import users_dao

class GetWorkspacesOfUserController(Controller):
    def get_path(self):
        return "/users/<int:user_id>/workspaces/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, user_id):
        workspaces = users_dao.get_workspaces_of_user(user_id)
        return [w.serialize() for w in workspaces]
        