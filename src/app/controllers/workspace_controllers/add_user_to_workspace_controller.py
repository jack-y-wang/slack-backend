from app.controllers import *
from flask import request
from app.dao import workspaces_dao

class AddUserToWorkspaceController(Controller):
    def get_path(self):
        return "/workspaces/<int:workspace_id>/users/"
    
    def get_methods(self):
        return ["POST"]
    
    def content(self, workspace_id):
        data = request.get_json()
        user_id = data.get("user_id")
        workspace = workspaces_dao.add_user_to_workspace(user_id, workspace_id)
        return workspace.serialize()