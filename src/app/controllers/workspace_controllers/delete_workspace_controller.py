from app.controllers import *
from flask import request
from app.dao import workspaces_dao

class DeleteWorkspaceController(Controller):
    def get_path(self):
        return "/workspaces/workspace_id/"
    
    def get_methods(self):
        return ["DELETE"]
    
    def content(self):
        workspace_id = int(request.view_args["workspace_id"])
        workspace = workspaces_dao.delete_workspace_by_id(workspace_id)
        return workspace.serialize()
        