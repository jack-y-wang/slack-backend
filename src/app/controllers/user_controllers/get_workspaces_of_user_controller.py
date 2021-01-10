from app.controllers import *
from flask import request
from app.dao import users_dao

class GetWorkspacesOfUserController(Controller):
    def get_path(self):
        return "/user/workspaces/"
    
    def get_methods(self):
        return ["GET"]
    
    @authorize_user
    def content(self, **kwargs):
        user = kwargs.get("user")
        workspaces = users_dao.get_workspaces_of_user(user.id)
        return [w.serialize() for w in workspaces]
        