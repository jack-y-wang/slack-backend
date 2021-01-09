from app.controllers import *
from flask import request
from app.dao import users_dao

class GetUserDMsController(Controller):
    def get_path(self):
        return "/users/<int:user_id>/workspaces/<int:workspace_id>/dms/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self, user_id, workspace_id):
        dms = users_dao.get_dms_of_user(user_id, workspace_id)
        return [dm.serialize() for dm in dms]
