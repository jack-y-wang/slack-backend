from app.controllers import *
from flask import request
from app.dao import dms_dao

class CreateDMGroupController(Controller):
    def get_name(self):
        return "create-dm-group"
        
    def get_path(self):
        return "/workspaces/<int:workspace_id>/dms/"
    
    def get_methods(self):
        return ["POST"]
    
    @authorize_user
    def content(self, workspace_id, **kwargs):
        user = kwargs.get("user")
        data = request.get_json()
        users = data.get("users")
        users.append({
            "user_id": user.id
        })
        dm_group = dms_dao.create_dm_group(workspace_id, users)
        return dm_group.serialize()
        