from app.controllers import *
from flask import request
from app.dao import workspaces_dao

class DeleteWorkspaceController(Controller):
    def get_name(self):
        return "delete-workspace"

    def get_path(self):
        return "/workspaces/<int:workspace_id>/"
    
    def get_methods(self):
        return ["DELETE"]
    
    @authorize_user
    def content(self, **kwargs):
        user = kwargs.get("user")
        in_workspace, _ = workspaces_dao.is_user_in_workspace(user.id, workspace_id)
        if not in_workspace:
            raise Exception("User not in workspace")

        workspace = workspaces_dao.delete_workspace_by_id(workspace_id)
        return workspace.serialize()
        