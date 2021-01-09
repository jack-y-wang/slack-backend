from app.controllers import *
from flask import request
from app.dao import workspaces_dao

class DeleteWorkspaceController(Controller):
    def get_name(self):
        return "delete-workspace"

    def get_path(self):
        return "/workspaces/delete/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        data = request.get_json()
        workspace_id = data.get("workspace_id")
        workspace = workspaces_dao.delete_workspace_by_id(workspace_id)
        return workspace.serialize()
        