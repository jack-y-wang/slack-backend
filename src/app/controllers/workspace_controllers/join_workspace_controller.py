from app.controllers import *
from flask import request
from app.dao import workspaces_dao

class JoinWorkspaceController(Controller):
    def get_path(self):
        return "/workspaces/<int:workspace_id>/join/"
    
    def get_methods(self):
        return ["POST"]
    
    @authorize_user
    def content(self, workspace_id, **kwargs):
        user = kwargs.get("user")
        workspace = workspaces_dao.add_user_to_workspace(user.id, workspace_id)
        return workspace.serialize()