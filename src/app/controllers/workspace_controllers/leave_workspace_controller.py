from app.controllers import *
from flask import request
from app.dao import workspaces_dao

class LeaveWorkspaceController(Controller):
    def get_path(self):
        return "/workspaces/<int:workspace_id>/leave/"
    
    def get_methods(self):
        return ["POST"]
    
    @authorize_user
    def content(self, workspace_id, **kwargs):
        user = kwargs.get("user")
        workspace = workspaces_dao.get_workspace_by_id(workspace_id)
        if not user in workspace.users:
            raise Exception("User not in Workspace")
        workspace = workspaces_dao.delete_user_from_workspace(workspace_id, user.id)
        return workspace.serialize()
