from app.controllers import *
from flask import request
from app.dao import users_dao

class GetUserDMsController(Controller):
    def get_path(self):
        return "/user/workspaces/<int:workspace_id>/dms/"
    
    def get_methods(self):
        return ["GET"]
    
    @authorize_user
    def content(self, workspace_id, **kwargs):
        user = kwargs.get("user")
        dms = users_dao.get_dms_of_user(user.id, workspace_id)
        return [dm.serialize() for dm in dms]
