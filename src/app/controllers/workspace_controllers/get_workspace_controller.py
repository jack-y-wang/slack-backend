from app.controllers import *
from flask import request
from app.dao import workspaces_dao

class GetWorkspaceController(Controller):
    def get_path(self):
        return "/workspaces/<workspace_id>/"
    
    def get_methods(self):
        return ["GET"]
    
    def content(self):
        workspace_id = int(request.view_args["workspace_id"])
        workspace = workspaces_dao.get_workspace_by_id(workspace_id)
        return workspace.serialize()
